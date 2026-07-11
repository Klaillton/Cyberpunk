from __future__ import annotations

import re
from pathlib import Path

from motor.markdown.campaign_paths import is_campaign_content_path
from motor.settings import Settings, get_settings

SUMMARY_COMMAND_MARKERS = (
    "resumo da sessão",
    "resumo da sessao",
    "criar resumo da sessão atual",
    "criar resumo da sessao atual",
    "finalizar sessão e gerar resumo",
    "finalizar sessao e gerar resumo",
)

FINALIZE_MARKERS = (
    "finalizar sessão e gerar resumo",
    "finalizar sessao e gerar resumo",
)


def _normalize_command_text(message: str) -> str:
    cleaned = message.strip().lower()
    if cleaned.startswith("[") and cleaned.endswith("]"):
        cleaned = cleaned[1:-1].strip()
    return cleaned


def detect_session_intent(message: str) -> str | None:
    normalized = _normalize_command_text(message)
    if any(marker in normalized for marker in SUMMARY_COMMAND_MARKERS):
        return "summary"
    if "passagem de tempo" in normalized or "pulso do mundo" in normalized:
        return "pulso"
    if "precisa ser atualizado" in normalized or "atualize o downtime" in normalized:
        return "update"
    if "análise completa" in normalized or "analise completa" in normalized:
        return "update"
    return None


def is_finalize_summary_command(message: str) -> bool:
    normalized = _normalize_command_text(message)
    return any(marker in normalized for marker in FINALIZE_MARKERS)


def next_session_log_rel(settings: Settings | None = None) -> str:
    cfg = settings or get_settings()
    logs_dir = cfg.campanha_root / "logs"
    numbers: list[int] = []
    if logs_dir.exists():
        for path in logs_dir.glob("sessao_resumo_*.md"):
            match = re.match(r"sessao_resumo_(\d{3})\.md$", path.name)
            if match:
                numbers.append(int(match.group(1)))
    next_num = max(numbers, default=0) + 1
    return f"logs/sessao_resumo_{next_num:03d}.md"


def latest_session_log_path(settings: Settings | None = None) -> Path | None:
    cfg = settings or get_settings()
    logs_dir = cfg.campanha_root / "logs"
    if not logs_dir.exists():
        return None
    candidates: list[tuple[int, Path]] = []
    for path in logs_dir.glob("sessao_resumo_*.md"):
        if not is_campaign_content_path(path.relative_to(cfg.campanha_root).as_posix()):
            continue
        match = re.match(r"sessao_resumo_(\d{3})\.md$", path.name)
        if match:
            candidates.append((int(match.group(1)), path))
    if not candidates:
        return None
    return max(candidates, key=lambda item: item[0])[1]


def session_summary_context_paths(settings: Settings | None = None) -> list[str]:
    cfg = settings or get_settings()
    paths = [
        "sistema/diretrizes_ia.md",
        "logs/sessao_resumo_template.md",
        "sistema/como_atualizar_arquivos.md",
        "board/board_campanha.md",
        "sistema/registro_arquivos.md",
    ]
    latest = latest_session_log_path(cfg)
    if latest is not None:
        rel = latest.relative_to(cfg.campanha_root).as_posix()
        if rel not in paths:
            paths.append(rel)
    return paths


_HISTORY_META_RE = re.compile(
    r"(?:LLM:\s*\S+|validacao:\s*\S+|tentativas:\s*\d+)"
    r"(?:\s*[·•]\s*(?:LLM:\s*\S+|validacao:\s*\S+|tentativas:\s*\d+))*",
    re.IGNORECASE,
)
_PLAYER_PREFIX_RE = re.compile(r"^\[[^\]]+\]\s*VOCE:\s*", re.IGNORECASE)
_NARRATOR_PREFIX_RE = re.compile(r"^NARRADOR\s*:\s*", re.IGNORECASE)


def normalize_history_entry(role: str, content: str, *, preserve_lines: bool = False) -> str:
    cleaned = str(content or "").strip()
    if preserve_lines:
        cleaned = re.sub(r"[ \t]+", " ", cleaned)
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    else:
        cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = _HISTORY_META_RE.sub("", cleaned).strip(" ·•")
    if role == "user":
        cleaned = _PLAYER_PREFIX_RE.sub("", cleaned).strip()
    else:
        cleaned = _NARRATOR_PREFIX_RE.sub("", cleaned).strip()
    return cleaned.strip()


def format_history_block(history: list[dict] | None, *, max_chars: int = 6000) -> str:
    if not history:
        return (
            "(Primeiro turno de chat nesta sessao — sem falas anteriores no feed. "
            "Use o resumo da cena/board e a acao do jogador; nao invente eventos passados. "
            "Nao mencione ao jogador que o historico esta vazio ou incompleto.)"
        )

    lines: list[str] = []
    for entry in history[-40:]:
        role = str(entry.get("role", "")).strip().lower()
        content = normalize_history_entry(role, str(entry.get("content", "")))
        if not content:
            continue
        label = "Jogador" if role == "user" else "Narrador/Sistema"
        lines.append(f"- **{label}:** {content}")

    if not lines:
        return "(Historico vazio apos normalizacao.)"

    block = "\n".join(lines)
    if len(block) <= max_chars:
        return block
    return block[: max_chars - 80] + "\n\n[...historico truncado...]"