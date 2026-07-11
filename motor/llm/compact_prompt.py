from __future__ import annotations

import re
from pathlib import Path

from motor.llm.types import ContextManifest
from motor.player_message import format_player_message_for_prompt, parse_player_message
from motor.session_command_handler import format_history_block, normalize_history_entry

_METADATA_RE = re.compile(r"\*\*([^*]+):\*\*\s*(.+)")
_SECTION_RE = re.compile(
    r"^##\s+(.+?)\s*\n(.*?)(?=^##\s+|\Z)",
    re.MULTILINE | re.DOTALL,
)
_TABLE_ROW_RE = re.compile(r"^\|\s*\*\*([^*|]+)\*\*\s*\|", re.MULTILINE)

_COMPACT_RULES = (
    "Voce e o narrador de uma campanha Cyberpunk RED solo.",
    "Responda com 1-2 paragrafos curtos (3-5 frases), apenas texto final.",
    "Narre consequencias NOVAS — nao repita a acao nem as falas do jogador.",
    "PROIBIDO controlar Ryan (nem 'Voce...' nem 'Ryan olha/assente/pergunta').",
    "NPCs RESPONDEM perguntas do jogador; nunca repetem a fala entre aspas dele.",
    "Falas de NPC: uma linha por fala — [NPC-M: Nome] \"texto\" ou [NPC-F: Nome] \"texto\".",
    "Mantenha hora do dia e local do resumo da cena.",
    "Sem prefixo NARRADOR:, sem menu A/B/C, sem 'o que voce faz'.",
    "Nao mencione historico vazio, resumo incompleto nem limitacoes do sistema.",
    "Priorize a acao do jogador AGORA sobre o board (ex: no Mule na estrada = narre no Mule, nao no acampamento).",
    "Use somente tags [NPC-M: Nome] ou [NPC-F: Nome] — nunca [Reyes-M: Reyes].",
)


def _strip_inline_markdown(text: str) -> str:
    cleaned = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    cleaned = re.sub(r"\*([^*]+)\*", r"\1", cleaned)
    return re.sub(r"`([^`]+)`", r"\1", cleaned)


def _teaser(text: str, max_len: int) -> str:
    compact = re.sub(r"\s+", " ", _strip_inline_markdown(text)).strip()
    if len(compact) <= max_len:
        return compact
    cut = compact[: max_len - 1].rsplit(" ", 1)[0]
    return f"{cut}…"


def _extract_metadata(text: str, label: str) -> str:
    for match in _METADATA_RE.finditer(text):
        if match.group(1).strip().lower() == label.lower():
            return _strip_inline_markdown(match.group(2).strip())
    return ""


def _find_section(text: str, heading: str) -> str:
    for match in _SECTION_RE.finditer(text):
        if match.group(1).strip().lower() == heading.lower():
            return match.group(2).strip()
    return ""


def _bullet_lines(block: str, limit: int = 4) -> list[str]:
    lines: list[str] = []
    for raw in block.splitlines():
        line = raw.strip()
        if line.startswith("- "):
            lines.append(_strip_inline_markdown(line[2:].strip()))
        if len(lines) >= limit:
            break
    return lines


def _last_narrator_text(history: list[dict] | None) -> str:
    if not history:
        return ""
    for entry in reversed(history):
        if str(entry.get("role", "")).lower() != "assistant":
            continue
        content = normalize_history_entry(
            "assistant",
            str(entry.get("content", "")),
            preserve_lines=True,
        )
        if not content:
            continue
        npc_match = re.search(r"\[NPC(?:-[MF])?:", content, flags=re.IGNORECASE)
        if npc_match:
            content = content[: npc_match.start()].strip()
        cleaned = re.sub(r"\s+", " ", content).strip()
        if cleaned:
            return cleaned
    return ""


def _board_scene_summary(board_text: str, *, max_chars: int = 900) -> str:
    if not board_text.strip():
        return "(Sem board carregado.)"
    parts: list[str] = []
    data = _extract_metadata(board_text, "Data Atual")
    local = _extract_metadata(board_text, "Local")
    if data:
        parts.append(f"- Data/hora: {data}")
    if local:
        parts.append(f"- Local: {local}")
    mission = _bullet_lines(_find_section(board_text, "Missão Atual"), limit=3)
    parts.extend(f"- {item}" for item in mission)
    npc_names = _TABLE_ROW_RE.findall(board_text)[:5]
    if npc_names:
        parts.append(f"- NPCs em foco: {', '.join(name.strip() for name in npc_names)}")
    block = "\n".join(parts)
    return _teaser(block, max_chars) if len(block) > max_chars else block


def _npc_personality_brief(path: Path, *, max_chars: int = 260) -> str | None:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    title = path.stem.replace("_recruit", "").replace("_", " ").replace(" - ", " — ")
    personality = _find_section(text, "Personalidade")
    narrator_notes = _find_section(text, "Notas para o narrador")
    voice = _find_section(text, "Aparência / voz (rápido)")
    chunks: list[str] = []
    if personality:
        chunks.extend(_bullet_lines(personality, limit=3))
    elif voice:
        chunks.append(_teaser(voice, 120))
    if narrator_notes:
        chunks.extend(_bullet_lines(narrator_notes, limit=2))
    if not chunks:
        role = _extract_metadata(text, "Role") or _extract_metadata(text, "Tipo")
        if role:
            chunks.append(role)
    if not chunks:
        return None
    body = "; ".join(chunks)
    return f"- **{title}:** {_teaser(body, max_chars)}"


def _collect_npc_briefs(
    context_paths: list[Path],
    repo_root: Path,
    *,
    max_npcs: int = 4,
    max_chars_each: int = 260,
) -> list[str]:
    briefs: list[str] = []
    seen: set[str] = set()
    ordered = sorted(
        context_paths,
        key=lambda path: (
            0 if "fichas/npc/" in path.relative_to(repo_root).as_posix() else 1,
            path.name,
        ),
    )
    for path in ordered:
        rel = path.relative_to(repo_root).as_posix()
        if not rel.startswith("fichas/"):
            continue
        if "template" in rel or "notas_narrador" in rel:
            continue
        if rel in seen:
            continue
        seen.add(rel)
        brief = _npc_personality_brief(path, max_chars=max_chars_each)
        if brief:
            briefs.append(brief)
        if len(briefs) >= max_npcs:
            break
    return briefs


def _truncate_block(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 24].rstrip() + "\n[...truncado...]"


def build_quality_rescue_prompt(
    *,
    message: str,
    history: list[dict] | None,
    manifest: ContextManifest,
    context_paths: list[Path],
    repo_root: Path,
    quality_details: str = "",
    max_chars: int = 4500,
) -> str:
    board_text = manifest.board_excerpt
    if not board_text.strip():
        board_path = repo_root / "board" / "board_campanha.md"
        if board_path.exists():
            board_text = board_path.read_text(encoding="utf-8", errors="replace")[:4000]

    scene = _board_scene_summary(board_text)
    history_block = format_history_block(history, max_chars=1400)
    last_narrator = _last_narrator_text(history) or "(primeira resposta da cena)"
    player_block = format_player_message_for_prompt(parse_player_message(message))
    npc_briefs = _collect_npc_briefs(context_paths, repo_root)

    parts = [
        "## Papel",
        *_COMPACT_RULES,
        "",
        "## Resumo da cena (canon)",
        scene,
        "",
        "## Historico recente",
        history_block,
        "",
        "## Ultima resposta do Narrador (NAO repetir)",
        _truncate_block(last_narrator, 700),
        "",
        "## Acao do jogador AGORA (ja executada)",
        player_block,
    ]
    if npc_briefs:
        parts.extend(["", "## NPCs envolvidos (voz/personalidade)", *npc_briefs])
    if quality_details.strip():
        parts.extend(
            [
                "",
                "## Falhas da validacao local (corrigir)",
                quality_details.strip(),
            ]
        )
    parts.extend(["", "## Sua resposta (somente narracao final)"])

    prompt = "\n".join(parts)
    return _truncate_block(prompt, max_chars)