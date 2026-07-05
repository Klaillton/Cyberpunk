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
import hashlib
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
PROPOSAL_DIR = SYNC_DIR / "proposals"
APPLIED_DIR = SYNC_DIR / "applied"
STATE_FILE = SYNC_DIR / "state.json"
RESULT_FILE = SYNC_DIR / "last_run_result.txt"
SOURCES_FILE = REPO_ROOT / "sistema" / "grok_sources.json"
PROMPT_TEMPLATE = REPO_ROOT / "scripts" / "prompts" / "atualizar-sessao.md"
PROPOSAL_TEMPLATE = REPO_ROOT / "scripts" / "prompts" / "propor-atualizacoes.md"
GROK_BIN = Path(os.environ.get("GROK_BIN", r"C:\Users\Dante\.grok\bin\grok.exe"))

MANDATORY_FILES = [
    "sistema/registro_arquivos.md",
    "sistema/instrucoes_projeto.md",
    "sistema/diretrizes_ia.md",
    "sistema/diretrizes_narrador.md",
    "sistema/dashboard_contexto.md",
    "board/board_campanha.md",
    "consequencias/consequencias_persistentes.md",
    "reputacao.md",
    "heat.md",
    "event_queue.md",
    "economia.md",
    "relacionamentos/mapa_relacional_geral.md",
]

RISK_LEVEL = {"low": 1, "medium": 2, "high": 3}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(msg: str) -> None:
    print(f"[sync] {msg}")


def ensure_dirs() -> None:
    for d in (SYNC_DIR, CACHE_DIR, DELTA_DIR, PROPOSAL_DIR, APPLIED_DIR):
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


def build_proposal_prompt(session_num: int) -> str:
    template = PROPOSAL_TEMPLATE.read_text(encoding="utf-8")
    next_num = f"{session_num + 1:03d}"
    session_str = f"{session_num:03d}"
    delta_files = "\n".join(f"- `.grok-sync/deltas/{p.name}`" for p in sorted(DELTA_DIR.glob("*.md")))
    return (
        template.replace("{SESSION_NUM}", session_str)
        .replace("{NEXT_SESSION_NUM}", next_num)
        + "\n\n## Arquivos delta\n\n"
        + (delta_files or "- (nenhum)")
    )


def extract_json_block(raw: str) -> str:
    fenced = re.search(r"```json\s*(\{[\s\S]*\})\s*```", raw)
    if fenced:
        return fenced.group(1)
    obj = re.search(r"(\{[\s\S]*\})", raw)
    if obj:
        return obj.group(1)
    raise ValueError("Nenhum JSON encontrado na resposta da IA")


def run_grok_proposal(session_num: int) -> tuple[Path, dict]:
    if not GROK_BIN.exists():
        raise FileNotFoundError(f"grok não encontrado: {GROK_BIN}")

    prompt = build_proposal_prompt(session_num)
    raw_path = PROPOSAL_DIR / f"session_{session_num:03d}_raw.txt"
    out_path = PROPOSAL_DIR / f"session_{session_num:03d}.json"

    env = os.environ.copy()
    env.pop("GIT_ASKPASS", None)
    proc = subprocess.run(
        [
            str(GROK_BIN),
            "-p",
            prompt,
            "--cwd",
            str(REPO_ROOT),
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
        raise RuntimeError(f"grok falhou ao gerar proposta: {proc.stderr[-2000:] or proc.stdout[-2000:]}")

    raw = proc.stdout.strip()
    raw_path.write_text(raw, encoding="utf-8")

    data = json.loads(extract_json_block(raw))
    validate_proposal(data)
    save_json(out_path, data)
    return out_path, data


def validate_proposal(data: dict) -> None:
    if not isinstance(data, dict):
        raise ValueError("Proposta inválida: raiz deve ser objeto JSON")
    batches = data.get("batches")
    if not isinstance(batches, list) or not batches:
        raise ValueError("Proposta inválida: campo 'batches' ausente ou vazio")

    for batch in batches:
        risk = str(batch.get("risk", "medium")).lower()
        if risk not in RISK_LEVEL:
            raise ValueError(f"Risco inválido no lote: {risk}")
        items = batch.get("items")
        if not isinstance(items, list) or not items:
            raise ValueError("Lote sem itens")
        for item in items:
            action = item.get("action")
            rel = item.get("file_path")
            if action not in {"create", "update", "delete"}:
                raise ValueError(f"Ação inválida: {action}")
            if not isinstance(rel, str) or not rel.strip():
                raise ValueError("Item sem file_path válido")
            if action != "delete" and not isinstance(item.get("new_content"), str):
                raise ValueError("Item create/update sem new_content")


def resolve_safe_path(rel_path: str) -> Path:
    rel = rel_path.replace("\\", "/").lstrip("/")
    candidate = (REPO_ROOT / rel).resolve()
    root = REPO_ROOT.resolve()
    if not str(candidate).startswith(str(root)):
        raise ValueError(f"Caminho fora do repositório: {rel_path}")
    return candidate


def sha256_file(path: Path) -> str:
    if not path.exists():
        return ""
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def risk_allowed(risk: str, max_risk: str) -> bool:
    return RISK_LEVEL.get(risk, 2) <= RISK_LEVEL.get(max_risk, 2)


def show_proposal_summary(data: dict) -> None:
    batches = data.get("batches", [])
    log(f"Proposta: {len(batches)} lote(s)")
    for b in batches:
        bid = b.get("id", "sem-id")
        label = b.get("label", "sem-label")
        risk = b.get("risk", "medium")
        items = b.get("items", [])
        log(f"  - {bid} [{label}] risco={risk} itens={len(items)}")


def choose_batches(data: dict, *, auto_approve_low: bool, yes: bool, max_risk: str) -> list[str]:
    approved: list[str] = []
    for batch in data.get("batches", []):
        bid = str(batch.get("id", ""))
        risk = str(batch.get("risk", "medium")).lower()
        if not bid:
            continue
        if not risk_allowed(risk, max_risk):
            log(f"Lote {bid} ignorado: risco {risk} > max-risk {max_risk}")
            continue
        if yes:
            approved.append(bid)
            continue
        if auto_approve_low and risk == "low":
            approved.append(bid)
            continue
        answer = input(f"Aprovar lote {bid} (risco={risk})? [y/N]: ").strip().lower()
        if answer in {"y", "yes", "s", "sim"}:
            approved.append(bid)
    return approved


def apply_batch(batch: dict) -> list[str]:
    backups: dict[Path, bytes | None] = {}
    touched: list[str] = []
    try:
        for item in batch.get("items", []):
            rel = item["file_path"]
            action = item["action"]
            path = resolve_safe_path(rel)

            if path not in backups:
                backups[path] = path.read_bytes() if path.exists() else None

            expected = item.get("hash_before")
            if isinstance(expected, str) and expected:
                current = sha256_file(path)
                if current != expected:
                    raise RuntimeError(f"Hash divergente para {rel}; arquivo mudou desde a proposta")

            if action == "delete":
                if path.exists():
                    path.unlink()
                touched.append(rel)
                continue

            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(item["new_content"], encoding="utf-8")
            touched.append(rel)

        validate_mandatory_files()
        return touched
    except Exception:
        for p, content in backups.items():
            if content is None:
                if p.exists():
                    p.unlink()
            else:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(content)
        raise


def validate_mandatory_files() -> None:
    missing = [rel for rel in MANDATORY_FILES if not (REPO_ROOT / rel).exists()]
    if missing:
        raise RuntimeError(f"Integridade falhou; arquivos obrigatórios ausentes: {', '.join(missing)}")


def apply_approved_batches(data: dict, approved_ids: list[str], session_num: int) -> list[str]:
    changed: list[str] = []
    applied_info: list[dict] = []
    for batch in data.get("batches", []):
        bid = batch.get("id")
        if bid not in approved_ids:
            continue
        touched = apply_batch(batch)
        changed.extend(touched)
        applied_info.append(
            {
                "id": bid,
                "label": batch.get("label", ""),
                "risk": batch.get("risk", "medium"),
                "files": touched,
            }
        )

    audit_path = APPLIED_DIR / f"session_{session_num:03d}_applied.json"
    save_json(
        audit_path,
        {
            "session": f"{session_num:03d}",
            "applied_at": utc_now(),
            "batches": applied_info,
        },
    )
    return sorted(set(changed))


def process_shares(
    sources: dict,
    state: dict,
    *,
    bootstrap: bool = False,
    tail: int | None = None,
) -> tuple[list[Path], dict]:
    deltas: list[Path] = []
    api = sources["api_template"]

    last_key = sources["shares"][-1]["key"]

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
            if key != last_key:
                start = total
                log(f"  tail: ignorado (só exporta em {last_key})")
            else:
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
    parser.add_argument("--propose-only", action="store_true", help="Gera proposta JSON e encerra")
    parser.add_argument("--review-only", action="store_true", help="Exibe resumo da proposta e encerra")
    parser.add_argument("--apply-approved", action="store_true", help="Aplica lotes aprovados e continua para commit")
    parser.add_argument("--max-risk", choices=["low", "medium", "high"], default="medium")
    parser.add_argument("--auto-approve-low", action="store_true", help="Aprova automaticamente lotes de baixo risco")
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

    proposal_data: dict | None = None
    proposal_path = PROPOSAL_DIR / f"session_{session_num:03d}.json"

    if not args.skip_ai:
        proposal_path, proposal_data = run_grok_proposal(session_num)
        log(f"Proposta gerada: {proposal_path.relative_to(REPO_ROOT)}")

    if proposal_data is None:
        if not proposal_path.exists():
            raise FileNotFoundError("Proposta não encontrada; execute sem --skip-ai para gerar")
        proposal_data = load_json(proposal_path)
        validate_proposal(proposal_data)

    show_proposal_summary(proposal_data)

    if args.propose_only or args.review_only:
        return 0

    if not args.apply_approved:
        log("Proposta pronta. Rode novamente com --apply-approved para aplicar os lotes aprovados.")
        return 0

    approved_ids = choose_batches(
        proposal_data,
        auto_approve_low=args.auto_approve_low,
        yes=args.yes,
        max_risk=args.max_risk,
    )
    if not approved_ids:
        log("Nenhum lote aprovado; encerrando sem alterações.")
        return 0

    changed_files = apply_approved_batches(proposal_data, approved_ids, session_num)
    if not changed_files:
        log("Nenhuma alteração aplicada após aprovação.")
        return 0

    RESULT_FILE.write_text(f"DONE: {', '.join(changed_files)}\n", encoding="utf-8")
    log(f"Arquivos aplicados: {', '.join(changed_files)}")

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