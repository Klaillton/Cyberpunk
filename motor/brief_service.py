from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

from motor.settings import Settings, get_settings

_SECTION_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_METADATA_RE = re.compile(r"\*\*([^*]+):\*\*\s*(.+)")
_DASHBOARD_SECTION_RE = re.compile(
    r"^##\s+(\d+\.\s+.+?)\s*\n(.*?)(?=^##\s+|\Z)",
    re.MULTILINE | re.DOTALL,
)
_SESSION_FILES = tuple(f"logs/sessao_resumo_{n:03d}.md" for n in range(99, 0, -1))


def _campaign_path(settings: Settings, rel_path: str) -> Path:
    return settings.campanha_root / rel_path


def _read_campaign_file(settings: Settings, rel_path: str) -> str:
    path = _campaign_path(settings, rel_path)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _extract_metadata(text: str, label: str) -> str:
    for match in _METADATA_RE.finditer(text):
        if match.group(1).strip().lower() == label.lower():
            return match.group(2).strip()
    return ""


def _find_section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*\n(.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def _dashboard_section(text: str, prefix: str) -> str:
    for match in _DASHBOARD_SECTION_RE.finditer(text):
        title = match.group(1).strip()
        if title.lower().startswith(prefix.lower()):
            return match.group(2).strip()
    return ""


def _bullet_lines(block: str, limit: int = 6) -> list[str]:
    lines: list[str] = []
    for raw in block.splitlines():
        line = raw.strip()
        if line.startswith("- "):
            lines.append(line[2:].strip())
        if len(lines) >= limit:
            break
    return lines


def _strip_inline_markdown(text: str) -> str:
    cleaned = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    cleaned = re.sub(r"\*([^*]+)\*", r"\1", cleaned)
    cleaned = re.sub(r"`([^`]+)`", r"\1", cleaned)
    return cleaned


def _teaser(text: str, max_len: int = 140) -> str:
    compact = re.sub(r"\s+", " ", _strip_inline_markdown(text)).strip()
    if len(compact) <= max_len:
        return compact
    cut = compact[: max_len - 1].rsplit(" ", 1)[0]
    return f"{cut}…"


def _latest_session_summary(settings: Settings) -> tuple[str, str]:
    for rel in _SESSION_FILES:
        text = _read_campaign_file(settings, rel)
        if not text.strip():
            continue
        events = _find_section(text, "Eventos Principais")
        if events:
            bullets = _bullet_lines(events, limit=4)
            detail = "\n".join(f"- {item}" for item in bullets) if bullets else events
            return rel, detail
        intro = "\n".join(line for line in text.splitlines()[:12] if line.strip() and not line.startswith("#"))
        return rel, intro.strip()
    return "", ""


def _opening_line(
    *,
    location: str,
    date: str,
    period: str,
    mission_teaser: str,
) -> str:
    parts: list[str] = []
    if period and date:
        parts.append(f"{period} — {date}.")
    elif date:
        parts.append(f"{date}.")
    if location:
        parts.append(location.rstrip(".") + ".")
    if mission_teaser:
        parts.append(mission_teaser.rstrip(".") + ".")
    parts.append("O canal de narração está aberto.")
    return " ".join(parts)


def _short_term_objective(event_text: str, board_text: str, dashboard_text: str) -> tuple[str, str, list[str]]:
    sources: list[str] = []
    high_events: list[str] = []
    for line in event_text.splitlines():
        if not line.startswith("| E"):
            continue
        cols = [col.strip() for col in line.strip("|").split("|")]
        if len(cols) < 5:
            continue
        _id, name, status, priority, prazo = cols[0], cols[1], cols[2], cols[3], cols[4]
        if status.lower() in {"resolvido", "concluído", "concluido"}:
            continue
        if "alta" in priority.lower() or "curto" in prazo.lower():
            if name not in high_events:
                high_events.append(name)

    projects = _find_section(board_text, "Missão Atual")
    pending_projects = [
        line[2:].strip()
        for line in projects.splitlines()
        if line.strip().startswith("- ") and "planejamento" in line.lower()
    ]

    dashboard_events = _dashboard_section(dashboard_text, "4. Eventos")
    bullets = _bullet_lines(dashboard_events, limit=5)

    detail_parts: list[str] = []
    if high_events:
        detail_parts.append("**Eventos prioritários (event queue):**\n" + "\n".join(f"- {e}" for e in high_events[:5]))
        sources.append("event_queue.md")
    if pending_projects:
        detail_parts.append("**Projetos em planejamento:**\n" + "\n".join(f"- {p}" for p in pending_projects))
        sources.append("board/board_campanha.md")
    if bullets:
        detail_parts.append("**Pendências do dashboard:**\n" + "\n".join(f"- {b}" for b in bullets))
        sources.append("sistema/dashboard_contexto.md")

    detail = "\n\n".join(detail_parts)
    teaser_items = high_events[:2] + pending_projects[:1]
    teaser = "; ".join(teaser_items) if teaser_items else _teaser(detail or "Sem pendências de curto prazo registradas.")
    return teaser, detail, sources


def build_campaign_brief(settings: Settings | None = None) -> dict:
    cfg = settings or get_settings()
    board = _read_campaign_file(cfg, "board/board_campanha.md")
    dashboard = _read_campaign_file(cfg, "sistema/dashboard_contexto.md")
    events = _read_campaign_file(cfg, "event_queue.md")
    heat = _read_campaign_file(cfg, "heat.md")

    location = _extract_metadata(board, "Local") or _extract_metadata(board, "Local Atual")
    date = _extract_metadata(board, "Data Atual")
    period = ""
    spatial = _dashboard_section(dashboard, "6. Localização")
    if spatial:
        period = _extract_metadata(spatial, "Período do dia") or _extract_metadata(spatial, "Periodo do dia")

    pack_section = _dashboard_section(dashboard, "1. Situação Atual com o Pack")
    pack_summary = _find_section(pack_section, "Resumo") if pack_section else ""
    if not pack_summary and pack_section:
        pack_summary = pack_section
    pack_bullets = _bullet_lines(pack_summary, limit=6)

    session_source, session_detail = _latest_session_summary(cfg)
    summary_detail_parts: list[str] = []
    summary_sources: list[str] = []
    if pack_bullets:
        summary_detail_parts.append("**Situação com o Pack:**\n" + "\n".join(f"- {b}" for b in pack_bullets))
        summary_sources.append("sistema/dashboard_contexto.md")
    if session_detail:
        summary_detail_parts.append(f"**Última sessão** (`{session_source}`):\n{session_detail}")
        summary_sources.append(session_source)
    confirmed = _find_section(board, "Pistas Confirmadas")
    if confirmed:
        summary_detail_parts.append("**Pistas confirmadas:**\n" + confirmed)
        summary_sources.append("board/board_campanha.md")

    summary_detail = "\n\n".join(summary_detail_parts)
    summary_teaser = _teaser("; ".join(pack_bullets[:2]) if pack_bullets else summary_detail)

    mission = _find_section(board, "Missão Atual")
    priority = ""
    for line in mission.splitlines():
        if "prioridade atual" in line.lower():
            priority = re.sub(r"\*\*", "", line).strip()
            break
    long_detail = mission.strip()
    long_sources = ["board/board_campanha.md"]
    if priority:
        long_teaser = _teaser(priority.replace("Prioridade atual:", "").strip())
    else:
        mission_bullets = _bullet_lines(mission, limit=2)
        long_teaser = _teaser("; ".join(mission_bullets) if mission_bullets else long_detail)

    short_teaser, short_detail, short_sources = _short_term_objective(events, board, dashboard)
    if heat:
        heat_summary = _find_section(heat, "Resumo") or _bullet_lines(heat, limit=3)
        if isinstance(heat_summary, list):
            heat_summary = "\n".join(f"- {h}" for h in heat_summary)
        if heat_summary:
            short_detail = f"{short_detail}\n\n**Heat:**\n{heat_summary}".strip()
            if "heat.md" not in short_sources:
                short_sources.append("heat.md")

    mission_line = priority or ( _bullet_lines(mission, limit=1)[0] if mission else "")
    opening = _opening_line(
        location=location,
        date=date,
        period=period,
        mission_teaser=mission_line,
    )

    updated_sources = [
        path
        for path, content in (
            ("board/board_campanha.md", board),
            ("sistema/dashboard_contexto.md", dashboard),
            ("event_queue.md", events),
        )
        if content.strip()
    ]

    return {
        "opening": opening,
        "meta": {
            "location": location,
            "date": date,
            "period": period,
            "updatedAt": datetime.now(timezone.utc).isoformat(),
            "sources": updated_sources,
        },
        "briefs": [
            {
                "id": "summary",
                "title": "Resumo Até Aqui",
                "teaser": summary_teaser or "Carregando resumo da campanha...",
                "detail": summary_detail or "Nenhum resumo disponível nos arquivos da campanha.",
                "sources": summary_sources,
            },
            {
                "id": "objective_long",
                "title": "Objetivo Atual (Médio/Longo Prazo)",
                "teaser": long_teaser or "Objetivo não definido no board.",
                "detail": long_detail or "Consulte board/board_campanha.md — seção Missão Atual.",
                "sources": long_sources,
            },
            {
                "id": "objective_short",
                "title": "Objetivo Secundário (Curto Prazo)",
                "teaser": short_teaser,
                "detail": short_detail or "Nenhuma pendência de curto prazo encontrada.",
                "sources": short_sources,
            },
        ],
    }