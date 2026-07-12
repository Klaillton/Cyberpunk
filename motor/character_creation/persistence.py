from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from motor.character_creation.renderer import render_character_markdown
from motor.character_creation.resolver import resolve_sheet_path
from motor.journal import save_journal_entries
from motor.settings import Settings, get_settings


@dataclass
class CreatedCharacter:
    id: str
    sheet_path: str
    journal_path: str
    relationships_path: str


def _role_file_prefix(role: str) -> str:
    mapping = {
        "rockerboy": "rockerboy",
        "solo": "solo",
        "netrunner": "netrunner",
        "tech": "techie",
        "medtech": "medtech",
        "media": "media",
        "exec": "exec",
        "lawman": "lawman",
        "fixer": "fixer",
        "nomad": "nomad",
    }
    return mapping.get(role.strip().lower(), role.strip().lower() or "character")


def create_protagonist(draft: dict[str, Any], settings: Settings | None = None) -> CreatedCharacter:
    cfg = settings or get_settings()
    slug = str(draft.get("slug", "")).strip().lower()
    if not slug:
        raise ValueError("slug obrigatorio")

    existing = resolve_sheet_path(slug, cfg)
    if existing is not None:
        raise FileExistsError(f"Personagem '{slug}' ja existe.")

    role_prefix = _role_file_prefix(str(draft.get("role", "")))
    sheet_rel = f"fichas/{role_prefix} - {slug}.md"
    sheet_path = cfg.campanha_root / sheet_rel
    sheet_path.parent.mkdir(parents=True, exist_ok=True)
    sheet_path.write_text(render_character_markdown(draft), encoding="utf-8")

    save_journal_entries(slug, [], cfg)

    rel_path = cfg.campanha_root / "relacionamentos" / f"{slug}_relacionamentos.md"
    if not rel_path.exists():
        rel_path.write_text(
            f"# Relacionamentos — {draft.get('name', slug)}\n\n## Aliados\n\n- \n\n## Facções\n\n- \n",
            encoding="utf-8",
        )

    cfg.character_id = slug
    return CreatedCharacter(
        id=slug,
        sheet_path=sheet_rel,
        journal_path=f"logs/journal/{slug}.json",
        relationships_path=rel_path.relative_to(cfg.campanha_root).as_posix(),
    )


def append_frontmatter(path: Path, metadata: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        return
    lines = ["---"]
    for key, value in metadata.items():
        lines.append(f"{key}: {value}")
    lines.append("---")
    lines.append("")
    path.write_text("\n".join(lines) + text, encoding="utf-8")