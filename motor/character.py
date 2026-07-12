from __future__ import annotations

from pathlib import Path

from motor.character_creation.resolver import resolve_sheet_path
from motor.markdown.tree import extract_references, parse_markdown_tree, render_section_tree
from motor.settings import Settings, get_settings


def _relative_campaign_path(path: Path, cfg: Settings) -> str:
    for root in (cfg.campanha_root, cfg.repo_root):
        try:
            return path.relative_to(root).as_posix()
        except ValueError:
            continue
    return path.as_posix()


def build_character_profile(
    character_id: str | None = None,
    settings: Settings | None = None,
) -> dict:
    cfg = settings or get_settings()
    char_id = (character_id or cfg.character_id).strip().lower()
    sheet_path = resolve_sheet_path(char_id, cfg) or cfg.character_sheet
    rel_path = cfg.character_relationships

    sheet_text = sheet_path.read_text(encoding="utf-8") if sheet_path.exists() else ""
    rel_text = rel_path.read_text(encoding="utf-8") if rel_path.exists() else ""

    sheet_tree = parse_markdown_tree(sheet_text)
    rel_tree = parse_markdown_tree(rel_text)
    profile_sections = render_section_tree(list(sheet_tree.get("sections", [])))
    if rel_tree.get("sections"):
        profile_sections.append(
            {
                "title": "Relacionamentos",
                "level": 2,
                "content": "",
                "children": render_section_tree(list(rel_tree.get("sections", []))),
            }
        )

    refs = extract_references(sheet_text + "\n" + rel_text)
    rel_posix = _relative_campaign_path(rel_path, cfg) if rel_path.exists() else ""
    sheet_posix = _relative_campaign_path(sheet_path, cfg) if sheet_path.exists() else sheet_path.as_posix()

    return {
        "characterId": char_id,
        "hero": {
            "title": str(sheet_tree.get("title", "Personagem")).strip() or "Personagem",
            "introLines": [line for line in sheet_tree.get("introLines", []) if str(line).strip()],
        },
        "sourceSheet": sheet_posix,
        "sourceRelationships": rel_posix,
        "imageUrl": f"/api/character-image/{char_id}",
        "sections": profile_sections,
        "references": refs,
    }