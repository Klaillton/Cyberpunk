#!/usr/bin/env python3
"""
Motor de narracao para campanha solo: integridade de estado + contexto inteligente + chat.

Exemplos:
  python scripts/narracao_engine.py check
  python scripts/narracao_engine.py chat --message "Quais eventos estao pendentes?"
  python scripts/narracao_engine.py repl

Provider:
  - grok (padrao): usa GROK_BIN para responder
  - none: apenas gera prompt consolidado para uso manual
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SYSTEM_DIR = REPO_ROOT / "sistema"
CHAT_DIR = REPO_ROOT / ".chat-engine"
SESSIONS_DIR = CHAT_DIR / "sessions"

GROK_BIN = Path(os.environ.get("GROK_BIN", r"C:\Users\Dante\.grok\bin\grok.exe"))

# Arquivos minimos para operar com integridade de estado.
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

CORE_CONTEXT = [
    "sistema/registro_arquivos.md",
    "sistema/instrucoes_projeto.md",
    "sistema/dashboard_contexto.md",
    "board/board_campanha.md",
]

OLLAMA_SKIP_CONTEXT = frozenset(
    {
        "sistema/registro_arquivos.md",
        "sistema/instrucoes_projeto.md",
        "sistema/diretrizes_ia.md",
        "sistema/diretrizes_narrador.md",
    }
)

OLLAMA_FILE_PRIORITY = (
    "board/board_campanha.md",
    "heat.md",
    "reputacao.md",
    "economia.md",
    "event_queue.md",
    "consequencias/consequencias_persistentes.md",
    "relacionamentos/",
    "facoes/",
    "sistema/dashboard_contexto.md",
)

DEFAULT_OLLAMA_MAX_PROMPT_CHARS = 8000
DEFAULT_OLLAMA_MAX_CONTEXT_FILES = 5

INTENT_RULES: list[tuple[re.Pattern[str], list[str]]] = [
    (
        re.compile(r"\b(heat|exposicao|perseguicao|rastreamento)\b", re.IGNORECASE),
        ["heat.md", "event_queue.md", "consequencias/consequencias_persistentes.md"],
    ),
    (
        re.compile(r"\b(reputacao|faccao|fac[c|c]ao|faccoes)\b", re.IGNORECASE),
        ["reputacao.md", "relacionamentos/faccao_relacionamentos.md", "facoes/faccoes_geral.md"],
    ),
    (
        re.compile(r"\b(economia|grana|eddies|recursos|oficina|projeto)\b", re.IGNORECASE),
        ["economia.md", "logs/downtime_ryan.md"],
    ),
    (
        re.compile(r"\b(npc|reyes|valk|alex|reina|kaz|doc|jax|ryan)\b", re.IGNORECASE),
        [
            "relacionamentos/mapa_relacional_geral.md",
            "relacionamentos/ryan_relacionamentos.md",
            "relacionamentos/crew_relacionamentos.md",
        ],
    ),
    (
        re.compile(r"\b(pulso|off-screen|offscreen|dia in-game|dia ingame|downtime)\b", re.IGNORECASE),
        ["sistema/pulso_procedimento.md", "pulso_do_mundo/README.md"],
    ),
]


@dataclass
class ChatTurn:
    timestamp: str
    role: str
    message: str


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_dirs() -> None:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def resolve_paths(rel_paths: list[str]) -> list[Path]:
    out: list[Path] = []
    for rel in rel_paths:
        p = REPO_ROOT / rel
        if p.exists() and p.is_file():
            out.append(p)
    return out


def check_integrity() -> list[str]:
    missing: list[str] = []
    for rel in MANDATORY_FILES:
        if not (REPO_ROOT / rel).exists():
            missing.append(rel)
    return missing


def _ollama_path_priority(rel: str) -> tuple[int, int, str]:
    for index, prefix in enumerate(OLLAMA_FILE_PRIORITY):
        if rel == prefix or rel.startswith(prefix):
            return (0, index, rel)
    if rel.startswith("sistema/"):
        return (2, 0, rel)
    return (1, 0, rel)


def prioritize_paths_for_ollama(paths: list[Path]) -> list[Path]:
    return sorted(
        paths,
        key=lambda path: _ollama_path_priority(path.relative_to(REPO_ROOT).as_posix()),
    )


def select_context_files(user_message: str, max_files: int = 10, *, provider: str | None = None) -> list[Path]:
    effective_max = max_files
    if provider == "ollama" and max_files == 10:
        effective_max = DEFAULT_OLLAMA_MAX_CONTEXT_FILES

    selected = set(CORE_CONTEXT)
    for pattern, files in INTENT_RULES:
        if pattern.search(user_message):
            selected.update(files)

    # Sempre considerar estado mecanico basico se houver espaco.
    selected.update(["reputacao.md", "heat.md", "event_queue.md", "economia.md"])

    paths = resolve_paths(sorted(selected))
    if provider == "ollama":
        paths = [
            path
            for path in paths
            if path.relative_to(REPO_ROOT).as_posix() not in OLLAMA_SKIP_CONTEXT
        ]
        paths = prioritize_paths_for_ollama(paths)

    return paths[:effective_max]


def compact_content(path: Path, max_chars: int = 4000) -> str:
    text = read_text(path)
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[...conteudo truncado para caber no contexto...]\n"


def _ollama_mode_hint(mode: str) -> str:
    if mode == "narrador":
        return (
            "Modo NARRADOR: descreva apenas a cena atual em prosa e faca perguntas ao jogador. "
            "Nao controle acoes do protagonista."
        )
    return (
        "Modo GESTOR: responda com consistencia de estado. "
        "Nao altere arquivos nem proponha updates automaticos."
    )


def _ollama_file_budget(rel: str, context_budget: int, remaining_files: int) -> int:
    if remaining_files <= 0:
        return 0
    if rel == "board/board_campanha.md":
        return min(int(context_budget * 0.45), 2800)
    if rel == "heat.md":
        return min(int(context_budget * 0.25), 1400)
    if remaining_files == 1:
        return context_budget
    return min(max(context_budget // remaining_files, 400), 1200)


def _build_ollama_context_blocks(context_paths: list[Path], context_budget: int) -> list[str]:
    blocks: list[str] = []
    used = 0
    ordered = prioritize_paths_for_ollama(context_paths)

    for index, path in enumerate(ordered):
        remaining_files = len(ordered) - index
        remaining_budget = context_budget - used
        if remaining_budget < 200:
            break

        rel = path.relative_to(REPO_ROOT).as_posix()
        file_cap = min(_ollama_file_budget(rel, context_budget, remaining_files), remaining_budget)
        if file_cap < 200:
            continue

        content = compact_content(path, max_chars=file_cap)
        block = f"### {rel}\n\n{content}"
        blocks.append(block)
        used += len(block)

    return blocks


def _build_ollama_prompt(
    user_message: str,
    context_paths: list[Path],
    mode: str,
    *,
    max_prompt_chars: int,
) -> str:
    header_parts = [
        "Voce e o narrador de uma campanha Cyberpunk RED solo.",
        "",
        "## Regras",
        "- Use apenas fatos presentes no contexto abaixo. Nao invente NPCs, locais, eventos ou consequencias.",
        "- Nao cite caminhos de arquivos, JSON, blocos UPDATE_PROPOSALS nem meta-comentarios sobre o prompt.",
        "- Nao descreva alteracoes em arquivos da campanha; apenas narre ou pergunte.",
        "- Se faltar informacao canonica, faca uma pergunta objetiva em vez de assumir.",
        f"- {_ollama_mode_hint(mode)}",
        "",
        "## Pergunta do jogador",
        user_message,
        "",
        "## Contexto",
    ]
    header = "\n".join(header_parts)
    safety_margin = 64
    context_budget = max(max_prompt_chars - len(header) - safety_margin, 1200)
    context_blocks = _build_ollama_context_blocks(context_paths, context_budget)

    prompt = header
    if context_blocks:
        prompt = f"{header}\n\n" + "\n\n".join(context_blocks)

    if len(prompt) > max_prompt_chars:
        suffix = "\n\n[...prompt truncado para caber no limite do Ollama...]\n"
        keep = max(max_prompt_chars - len(suffix), 0)
        prompt = prompt[:keep] + suffix

    return prompt


def build_prompt(
    user_message: str,
    context_paths: list[Path],
    mode: str,
    *,
    provider: str | None = None,
    max_prompt_chars: int | None = None,
) -> str:
    if provider == "ollama":
        return _build_ollama_prompt(
            user_message,
            context_paths,
            mode,
            max_prompt_chars=max_prompt_chars or DEFAULT_OLLAMA_MAX_PROMPT_CHARS,
        )

    mode_hint = (
        "Modo NARRADOR: foque em proposta de cena e perguntas ao jogador sem controlar o protagonista."
        if mode == "narrador"
        else "Modo GESTOR: foque em consistencia de estado, arquivos a atualizar e rastreabilidade."
    )

    context_blocks: list[str] = []
    for p in context_paths:
        rel = p.relative_to(REPO_ROOT).as_posix()
        context_blocks.append(f"### Arquivo: {rel}\n\n{compact_content(p)}")

    return "\n\n".join(
        [
            "# Sistema de Narracao Solo - Prompt Orquestrado",
            "",
            "## Regras obrigatorias",
            "- Se nao estiver registrado nos arquivos, nao trate como fato canonico.",
            "- Cite quais arquivos sustentam cada decisao importante.",
            "- Se detectar lacuna de estado, proponha pergunta objetiva antes de assumir qualquer detalhe.",
            "",
            f"## Perfil de operacao\n{mode_hint}",
            "",
            f"## Pergunta do usuario\n{user_message}",
            "",
            "## Contexto carregado",
            *context_blocks,
        ]
    )


def run_grok(prompt: str) -> str:
    if not GROK_BIN.exists():
        raise FileNotFoundError(f"grok nao encontrado: {GROK_BIN}")

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
        capture_output=True,
        text=True,
        timeout=900,
    )
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "erro desconhecido")[-2000:]
        raise RuntimeError(f"grok falhou: {err}")
    return proc.stdout.strip()


def append_session_log(session_file: Path, turn: ChatTurn) -> None:
    with session_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(turn.__dict__, ensure_ascii=False) + "\n")


def get_session_file(session_name: str | None = None) -> Path:
    if session_name:
        return SESSIONS_DIR / f"{session_name}.jsonl"
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return SESSIONS_DIR / f"session-{ts}.jsonl"


def cmd_check() -> int:
    missing = check_integrity()
    if missing:
        print("Integridade: FALHA")
        for rel in missing:
            print(f"- Ausente: {rel}")
        return 2
    print("Integridade: OK")
    return 0


def cmd_chat(message: str, provider: str, mode: str, print_prompt: bool) -> int:
    missing = check_integrity()
    if missing:
        print("Nao foi possivel responder: faltam arquivos obrigatorios.")
        for rel in missing:
            print(f"- {rel}")
        return 2

    ensure_dirs()
    session_file = get_session_file()

    context_paths = select_context_files(message)
    prompt = build_prompt(message, context_paths, mode)

    if print_prompt or provider == "none":
        print("===== PROMPT ORQUESTRADO =====")
        print(prompt)
        print("===== FIM PROMPT =====")

    append_session_log(session_file, ChatTurn(utc_now(), "user", message))

    if provider == "none":
        answer = (
            "Provider desativado (none). Use o prompt acima em qualquer LLM e registre a resposta."
        )
    else:
        answer = run_grok(prompt)

    append_session_log(session_file, ChatTurn(utc_now(), "assistant", answer))

    print(answer)
    print(f"\n[session-log] {session_file.relative_to(REPO_ROOT).as_posix()}")
    return 0


def cmd_repl(provider: str, mode: str, print_prompt: bool) -> int:
    missing = check_integrity()
    if missing:
        print("Nao foi possivel iniciar REPL: faltam arquivos obrigatorios.")
        for rel in missing:
            print(f"- {rel}")
        return 2

    ensure_dirs()
    session_file = get_session_file()
    print("REPL iniciado. Digite 'sair' para encerrar.")

    while True:
        try:
            message = input("\nvoce> ").strip()
        except KeyboardInterrupt:
            print("\nEncerrado.")
            return 130

        if not message:
            continue
        if message.lower() in {"sair", "exit", "quit"}:
            print("Encerrando REPL.")
            return 0

        append_session_log(session_file, ChatTurn(utc_now(), "user", message))
        context_paths = select_context_files(message)
        prompt = build_prompt(message, context_paths, mode)

        if print_prompt:
            print("\n===== PROMPT ORQUESTRADO =====")
            print(prompt)
            print("===== FIM PROMPT =====")

        if provider == "none":
            answer = "Provider none: resposta automatica desativada para este turno."
        else:
            try:
                answer = run_grok(prompt)
            except Exception as exc:  # pragma: no cover - depende de ambiente externo
                answer = f"ERRO ao consultar provider: {exc}"

        append_session_log(session_file, ChatTurn(utc_now(), "assistant", answer))
        print(f"\nengine> {answer}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Motor de narracao solo com contexto inteligente")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("check", help="Valida integridade minima de arquivos")

    chat = sub.add_parser("chat", help="Executa um turno unico")
    chat.add_argument("--message", required=True, help="Mensagem do usuario")
    chat.add_argument("--provider", choices=["grok", "none"], default="grok")
    chat.add_argument("--mode", choices=["gestor", "narrador"], default="gestor")
    chat.add_argument("--print-prompt", action="store_true")

    repl = sub.add_parser("repl", help="Chat interativo")
    repl.add_argument("--provider", choices=["grok", "none"], default="grok")
    repl.add_argument("--mode", choices=["gestor", "narrador"], default="gestor")
    repl.add_argument("--print-prompt", action="store_true")

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.cmd == "check":
        return cmd_check()
    if args.cmd == "chat":
        return cmd_chat(args.message, args.provider, args.mode, args.print_prompt)
    if args.cmd == "repl":
        return cmd_repl(args.provider, args.mode, args.print_prompt)

    print(f"Comando invalido: {args.cmd}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
