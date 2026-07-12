from __future__ import annotations

from pathlib import Path
from typing import Any

from motor.character_creation.rules import STAT_KEYS
from motor.settings import get_settings


def _stat_table(stats: dict[str, int]) -> str:
    lines = [
        "## Atributos (62 Pontos)",
        "",
        "| Atributo | Valor | Modificador |",
        "| -------- | ----- | ----------- |",
    ]
    for key in STAT_KEYS:
        value = int(stats.get(key, 0))
        lines.append(f"| {key} | {value} | +{value} |")
    return "\n".join(lines)


def _skills_block(skills: dict[str, int]) -> str:
    lines = ["## Skills", ""]
    for name, level in sorted(skills.items(), key=lambda item: (-int(item[1]), item[0])):
        lines.append(f"- {name}: {int(level)}")
    return "\n".join(lines)


def render_character_markdown(draft: dict[str, Any]) -> str:
    name = str(draft.get("name", "Sem Nome")).strip()
    handle = str(draft.get("handle", "")).strip()
    title = f'{name} "{handle}"' if handle else name
    role = str(draft.get("role_label", draft.get("role", ""))).strip()
    concept = str(draft.get("concept", "")).strip()
    appearance = str(draft.get("appearance", "")).strip()
    background = str(draft.get("background", "")).strip()
    slug = str(draft.get("slug", "")).strip().lower()
    role_id = str(draft.get("role", "")).strip().lower()
    ability = str(draft.get("role_ability", "")).strip()
    ability_rank = int(draft.get("role_ability_rank", 4))

    frontmatter = "\n".join(
        [
            "---",
            f"id: {slug}",
            "type: character",
            "tier: protagonist",
            "cpr_method: complete_package",
            f"role: {role_id}",
            f"aliases: [{handle or name}]",
            "---",
            "",
        ]
    )

    parts = [
        frontmatter,
        f"# {title}",
        "",
        f"**Role:** {role}",
        f"**Conceito:** {concept}" if concept else "",
        "",
    ]
    if appearance:
        parts.extend(["## Aparência", "", appearance, ""])
    if background:
        parts.extend(["## Background", "", background, ""])
    parts.append(_stat_table(draft.get("stats") or {}))
    parts.append("")
    parts.append(_skills_block(draft.get("skills") or {}))
    if ability:
        parts.extend(["", f"## Role Ability: {ability}", "", f"- Rank inicial: {ability_rank}", ""])
    return "\n".join(part for part in parts if part is not None)


def load_pc_template() -> str:
    root = get_settings().repo_root
    path = root / "fichas" / "templates" / "cpr_protagonist.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""