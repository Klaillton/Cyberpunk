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


def select_context_files(user_message: str, max_files: int = 10) -> list[Path]:
    selected = set(CORE_CONTEXT)
    for pattern, files in INTENT_RULES:
        if pattern.search(user_message):
            selected.update(files)

    # Sempre considerar estado mecanico basico se houver espaco.
    selected.update(["reputacao.md", "heat.md", "event_queue.md", "economia.md"])

    paths = resolve_paths(sorted(selected))
    return paths[:max_files]


def compact_content(path: Path, max_chars: int = 4000) -> str:
    text = read_text(path)
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[...conteudo truncado para caber no contexto...]\n"


def build_prompt(user_message: str, context_paths: list[Path], mode: str) -> str:
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
