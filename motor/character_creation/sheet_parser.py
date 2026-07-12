from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from motor.character_creation.tiers import normalize_tier, tier_for_slug
from motor.markdown.tree import parse_markdown_tree
from motor.settings import Settings, get_settings

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_STAT_ROW_RE = re.compile(
    r"^\s*(?:[-*]\s*)?(INT|REF|DEX|TECH|COOL|WILL|LUCK|MOVE|BODY|EMP)\b[^0-9]*(\d+)",
    re.IGNORECASE | re.MULTILINE,
)
_TABLE_STAT_RE = re.compile(
    r"\|\s*(INT|REF|DEX|TECH|COOL|WILL|LUCK|MOVE|BODY|EMP)[^|]*\|\s*(\d+)",
    re.IGNORECASE,
)
_SKILL_PAIR_RE = re.compile(r"^\s*[-*]?\s*([^:\n|]+?)\s*:\s*(\d+)\s*$", re.MULTILINE)
_SKILL_TABLE_RE = re.compile(r"\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|")


def parse_frontmatter(text: str) -> dict[str, Any]:
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}
    block = match.group(1)
    result: dict[str, Any] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, _, raw = line.partition(":")
        key = key.strip()
        value = raw.strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            result[key] = [part.strip().strip("'\"") for part in inner.split(",") if part.strip()]
        elif value.lower() in {"true", "false"}:
            result[key] = value.lower() == "true"
        else:
            result[key] = value.strip("'\"")
    return result


def strip_frontmatter(text: str) -> str:
    return _FRONTMATTER_RE.sub("", text, count=1)


def _section_map(sections: list[dict]) -> dict[str, str]:
    mapped: dict[str, str] = {}

    def walk(nodes: list[dict]) -> None:
        for node in nodes:
            title = str(node.get("title", "")).strip()
            content = str(node.get("content", "")).strip()
            if title:
                mapped[title.lower()] = content
            children = node.get("children") or []
            if isinstance(children, list):
                walk(children)

    walk(sections)
    return mapped


def _parse_horizontal_stat_table(blob: str) -> dict[str, int]:
    lines = [line.strip() for line in blob.splitlines() if "|" in line]
    if len(lines) < 2:
        return {}
    header_cells = [cell.strip().upper() for cell in lines[0].split("|") if cell.strip()]
    if not all(len(cell) <= 5 and cell.isalpha() for cell in header_cells):
        return {}
    for line in lines[1:]:
        if set(line.replace("|", "").replace("-", "").strip()) <= {" "}:
            continue
        values = [cell.strip() for cell in line.split("|") if cell.strip()]
        if len(values) != len(header_cells):
            continue
        parsed: dict[str, int] = {}
        for key, raw in zip(header_cells, values, strict=False):
            if raw.isdigit():
                parsed[key] = int(raw)
        if parsed:
            return parsed
    return {}


def extract_stats(text: str, sections: dict[str, str]) -> dict[str, int]:
    blobs = [
        sections.get("atributos (62 pontos)", ""),
        sections.get("atributos", ""),
        sections.get("estatísticas", ""),
        sections.get("estatisticas", ""),
        text,
    ]
    stats: dict[str, int] = {}
    for blob in blobs:
        if not blob:
            continue
        horizontal = _parse_horizontal_stat_table(blob)
        stats.update(horizontal)
        for match in _TABLE_STAT_RE.finditer(blob):
            stats[match.group(1).upper()] = int(match.group(2))
        for match in _STAT_ROW_RE.finditer(blob):
            stats[match.group(1).upper()] = int(match.group(2))
    emp_match = re.search(r"\*\*EMP:?\*\*\s*(\d+)", text, re.IGNORECASE)
    if emp_match:
        stats["EMP"] = int(emp_match.group(1))
    return stats


def extract_skills(sections: dict[str, str]) -> dict[str, int]:
    blob = (
        sections.get("skills principais", "")
        or sections.get("skills", "")
        or sections.get("role ability: maker", "")
    )
    skills: dict[str, int] = {}
    for match in _SKILL_TABLE_RE.finditer(blob):
        name = match.group(1).strip()
        if name.lower() in {"skill", "nível", "nivel", "---"}:
            continue
        skills[name] = int(match.group(2))
    for match in _SKILL_PAIR_RE.finditer(blob):
        name = match.group(1).strip().lstrip("-* ")
        if not name or name.lower().startswith("linguagens"):
            continue
        if "(" in name and ")" in name:
            continue
        try:
            skills[name] = int(match.group(2))
        except ValueError:
            continue
    return skills


def parse_character_sheet(
    path: Path | None = None,
    *,
    text: str | None = None,
    settings: Settings | None = None,
) -> dict[str, Any]:
    cfg = settings or get_settings()
    if text is None:
        if path is None:
            raise ValueError("path or text required")
        text = path.read_text(encoding="utf-8")

    frontmatter = parse_frontmatter(text)
    body = strip_frontmatter(text)
    tree = parse_markdown_tree(body)
    sections = _section_map(list(tree.get("sections", [])))

    rel = ""
    slug = str(frontmatter.get("id", "")).strip().lower()
    if path is not None:
        try:
            rel = path.relative_to(cfg.campanha_root).as_posix()
        except ValueError:
            rel = path.as_posix()
        if not slug:
            stem = path.stem
            if " - " in stem:
                slug = stem.split(" - ", 1)[1].strip().lower()
            else:
                slug = stem.strip().lower()

    tier = normalize_tier(str(frontmatter.get("tier", "")), slug=slug or None)
    if not frontmatter.get("tier") and slug:
        tier = tier_for_slug(slug)

    stats = extract_stats(body, sections)
    skills = extract_skills(sections)

    intro_lines = [str(line).strip() for line in tree.get("introLines", []) if str(line).strip()]

    return {
        "id": slug,
        "tier": tier,
        "title": str(tree.get("title", "")).strip(),
        "role": str(frontmatter.get("role", "")).strip(),
        "introLines": intro_lines,
        "stats": stats,
        "skills": skills,
        "sections": sections,
        "sourcePath": rel,
        "layout": _layout_for_tier(tier),
        "derived": _derive(stats),
    }


def _derive(stats: dict[str, int]) -> dict[str, Any]:
    body = stats.get("BODY", 0)
    will = stats.get("WILL", 0)
    emp = stats.get("EMP", 0)
    hp = (body + will) * 3 if body and will else None
    return {
        "hp": hp,
        "seriouslyWounded": hp // 2 if hp else None,
        "deathSave": body or None,
        "humanityBase": emp * 10 if emp else None,
    }


def _layout_for_tier(tier: str) -> str:
    if tier in {"protagonist", "crew_full"}:
        return "cpr_full"
    if tier == "npc_reference":
        return "cpr_reference"
    return "cpr_generic"