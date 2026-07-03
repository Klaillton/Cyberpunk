#!/usr/bin/env python3
"""
Sync campanha Cyberpunk: re-fetch Grok shares → delta → Grok headless → git commit/push.

Uso:
  python scripts/sync_campanha.py --bootstrap     # primeira vez: marca tudo como processado
  python scripts/sync_campanha.py --dry-run       # só fetch + relatório
  python scripts/sync_campanha.py                 # sync se houver mensagens novas
  python scripts/sync_campanha.py --tail 5 --apply -y   # teste: reprocessa últimas N msgs
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SYNC_DIR = REPO_ROOT / ".grok-sync"
CACHE_DIR = SYNC_DIR / "cache"
DELTA_DIR = SYNC_DIR / "deltas"
STATE_FILE = SYNC_DIR / "state.json"
RESULT_FILE = SYNC_DIR / "last_run_result.txt"
SOURCES_FILE = REPO_ROOT / "sistema" / "grok_sources.json"
PROMPT_TEMPLATE = REPO_ROOT / "scripts" / "prompts" / "atualizar-sessao.md"
GROK_BIN = Path(os.environ.get("GROK_BIN", r"C:\Users\Dante\.grok\bin\grok.exe"))


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(msg: str) -> None:
    print(f"[sync] {msg}")


def ensure_dirs() -> None:
    for d in (SYNC_DIR, CACHE_DIR, DELTA_DIR):
        d.mkdir(parents=True, exist_ok=True)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def load_sources() -> dict:
    return load_json(SOURCES_FILE)


def fetch_share(api_template: str, share_id: str) -> dict:
    url = api_template.format(share_id=share_id)
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "Cyberpunk-Campaign-Sync/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.load(resp)


def dialogue_messages(data: dict) -> list[dict]:
    messages = []
    for r in data.get("responses", []):
        msg = r.get("message")
        if not msg or not isinstance(msg, str) or r.get("isControl"):
            continue
        sender = (r.get("sender") or "?").lower()
        role = "USER" if sender == "human" else "GROK"
        messages.append(
            {
                "role": role,
                "time": (r.get("createTime") or "")[:10],
                "text": msg.strip(),
                "response_id": r.get("responseId", ""),
            }
        )
    return messages


def next_session_number() -> int:
    logs = REPO_ROOT / "logs"
    nums = []
    for p in logs.glob("sessao_resumo_*.md"):
        m = re.match(r"sessao_resumo_(\d{3})\.md$", p.name)
        if m:
            nums.append(int(m.group(1)))
    return max(nums, default=0) + 1


def load_state() -> dict | None:
    if STATE_FILE.exists():
        return load_json(STATE_FILE)
    return None


def default_state() -> dict:
    return {"shares": {}, "last_run": None, "bootstrapped": False}


def run_git(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env.pop("GIT_ASKPASS", None)
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=check,
    )


def git_pull() -> None:
    log("git pull...")
    proc = run_git(["pull", "--ff-only", "origin", "main"], check=False)
    if proc.returncode != 0:
        log(f"git pull falhou (continuando): {proc.stderr.strip() or proc.stdout.strip()}")


def git_push() -> None:
    log("git push...")
    token_proc = subprocess.run(
        ["gh", "auth", "token"],
        capture_output=True,
        text=True,
        check=True,
    )
    token = token_proc.stdout.strip()
    remote = f"https://x-access-token:{token}@github.com/Klaillton/Cyberpunk.git"
    env = os.environ.copy()
    env.pop("GIT_ASKPASS", None)
    proc = subprocess.run(
        ["git", "-c", "credential.helper=", "push", remote, "main"],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "git push failed")


def git_commit_and_push(message: str) -> bool:
    status = run_git(["status", "--porcelain"], check=True)
    if not status.stdout.strip():
        log("Nenhuma alteração para commit.")
        return False
    run_git(["add", "-A"], check=True)
    run_git(["commit", "-m", message], check=True)
    git_push()
    return True


def export_delta_md(share_key: str, label: str, messages: list[dict], start_idx: int) -> Path | None:
    slice_msgs = messages[start_idx:]
    if not slice_msgs:
        return None
    out = DELTA_DIR / f"{share_key}_delta.md"
    with out.open("w", encoding="utf-8") as f:
        f.write(f"# Delta — {label} ({share_key})\n\n")
        f.write(f"- Mensagens novas: {len(slice_msgs)} (índice {start_idx + 1} em diante)\n")
        f.write(f"- Gerado em: {utc_now()}\n\n---\n\n")
        for i, m in enumerate(slice_msgs, start=start_idx + 1):
            f.write(f"## [{i}] {m['role']} ({m['time']})\n\n")
            f.write(m["text"] + "\n\n---\n\n")
    return out


def build_grok_prompt(session_num: int) -> str:
    template = PROMPT_TEMPLATE.read_text(encoding="utf-8")
    next_num = f"{session_num + 1:03d}"
    session_str = f"{session_num:03d}"
    return (
        template.replace("{SESSION_NUM}", session_str)
        .replace("{NEXT_SESSION_NUM}", next_num)
        + "\n\n## Arquivos delta\n\n"
        + "\n".join(f"- `.grok-sync/deltas/{p.name}`" for p in sorted(DELTA_DIR.glob("*.md")))
    )


def run_grok_update(session_num: int) -> str:
    if not GROK_BIN.exists():
        raise FileNotFoundError(f"grok não encontrado: {GROK_BIN}")
    prompt = build_grok_prompt(session_num)
    prompt_file = SYNC_DIR / "prompt_last.txt"
    prompt_file.write_text(prompt, encoding="utf-8")
    if RESULT_FILE.exists():
        RESULT_FILE.unlink()

    log("Executando grok headless (pode levar alguns minutos)...")
    env = os.environ.copy()
    env.pop("GIT_ASKPASS", None)
    proc = subprocess.run(
        [
            str(GROK_BIN),
            "-p",
            prompt,
            "--cwd",
            str(REPO_ROOT),
            "--yolo",
            "--output-format",
            "plain",
        ],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=1800,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"grok falhou: {proc.stderr[-2000:] or proc.stdout[-2000:]}")
    if RESULT_FILE.exists():
        return RESULT_FILE.read_text(encoding="utf-8").strip()
    return proc.stdout.strip()[-500:]


def process_shares(
    sources: dict,
    state: dict,
    *,
    bootstrap: bool = False,
    tail: int | None = None,
) -> tuple[list[Path], dict]:
    deltas: list[Path] = []
    api = sources["api_template"]

    for share in sources["shares"]:
        key = share["key"]
        share_id = share["share_id"]
        label = share["label"]

        log(f"Fetch {key} ({share_id[:20]}...)")
        data = fetch_share(api, share_id)
        cache_path = CACHE_DIR / f"{key}.json"
        save_json(cache_path, data)

        messages = dialogue_messages(data)
        conv = data.get("conversation", {})
        modify_time = conv.get("modifyTime", "")
        total = len(messages)

        prev = state["shares"].get(key, {})
        processed = prev.get("processed_count", 0)

        if bootstrap:
            start = total
            log(f"  bootstrap: {total} mensagens marcadas como processadas")
        elif tail is not None:
            start = max(0, total - tail)
            log(f"  tail={tail}: exportando mensagens {start + 1}..{total}")
        else:
            start = processed
            if start > total:
                start = 0
            new_count = total - start
            log(f"  total={total}, processadas={processed}, novas={new_count}")

        delta_path = export_delta_md(key, label, messages, start)
        if delta_path:
            deltas.append(delta_path)

        state["shares"][key] = {
            "share_id": share_id,
            "processed_count": total,
            "modify_time": modify_time,
            "message_count": total,
            "last_response_id": messages[-1]["response_id"] if messages else "",
        }

    state["last_run"] = utc_now()
    state["bootstrapped"] = bootstrap or state.get("bootstrapped", False)
    return deltas, state


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync Grok shares → campanha → GitHub")
    parser.add_argument("--bootstrap", action="store_true", help="Primeira execução: baseline sem IA/commit")
    parser.add_argument("--dry-run", action="store_true", help="Só fetch e relatório")
    parser.add_argument("--apply", action="store_true", help="Forçar IA+commit mesmo sem mensagens novas (com --tail)")
    parser.add_argument("--tail", type=int, default=None, help="Reprocessar últimas N mensagens (teste)")
    parser.add_argument("--skip-pull", action="store_true")
    parser.add_argument("--skip-ai", action="store_true")
    parser.add_argument("--skip-commit", action="store_true")
    parser.add_argument("-y", "--yes", action="store_true", help="Não pedir confirmação")
    args = parser.parse_args()

    ensure_dirs()
    sources = load_sources()
    state = load_state() or default_state()

    if not args.skip_pull:
        git_pull()

    deltas, state = process_shares(
        sources,
        state,
        bootstrap=args.bootstrap,
        tail=args.tail,
    )
    save_json(STATE_FILE, state)

    if args.bootstrap:
        log("Bootstrap concluído. Próximas execuções só processam mensagens novas.")
        return 0

    has_delta = any(p.stat().st_size > 200 for p in deltas)
    if args.dry_run:
        log(f"Dry-run: {len(deltas)} arquivo(s) delta, conteúdo novo={'sim' if has_delta else 'não'}")
        for p in deltas:
            log(f"  - {p.relative_to(REPO_ROOT)} ({p.stat().st_size} bytes)")
        return 0

    if not has_delta and not (args.tail and args.apply):
        log("Sem mensagens novas. Nada a fazer.")
        return 0

    if args.tail and not args.apply:
        log("Use --apply com --tail para reprocessar mensagens antigas.")
        return 2

    session_num = next_session_number()
    log(f"Próximo resumo de sessão: {session_num:03d}")

    if not args.skip_ai:
        result = run_grok_update(session_num)
        log(f"Grok: {result[:300]}")
        if "SKIP:" in result:
            log("IA indicou skip — sem commit.")
            return 0

    if args.skip_commit:
        log("Commit ignorado (--skip-commit).")
        return 0

    committed = git_commit_and_push(
        f"docs(campanha): sync grok sessao {session_num:03d} e atualizacoes"
    )
    if committed:
        log("Commit e push concluídos.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        log("Interrompido.")
        sys.exit(130)
    except Exception as exc:
        log(f"ERRO: {exc}")
        sys.exit(1)