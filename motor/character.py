from __future__ import annotations

from motor.markdown.tree import extract_references, parse_markdown_tree, render_section_tree
from motor.settings import Settings, get_settings


def build_character_profile(settings: Settings | None = None) -> dict:
    cfg = settings or get_settings()
    sheet_text = cfg.character_sheet.read_text(encoding="utf-8") if cfg.character_sheet.exists() else ""
    rel_text = (
        cfg.character_relationships.read_text(encoding="utf-8") if cfg.character_relationships.exists() else ""
    )

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

    return {
        "characterId": cfg.character_id,
        "hero": {
            "title": str(sheet_tree.get("title", "Ryan Wireghost Voss")).strip() or "Ryan Wireghost Voss",
            "introLines": [line for line in sheet_tree.get("introLines", []) if str(line).strip()],
        },
        "sourceSheet": "fichas/techie - ryan_wireghost_voss.md",
        "sourceRelationships": "relacionamentos/ryan_relacionamentos.md",
        "imageUrl": f"/api/character-image/{cfg.character_id}",
        "sections": profile_sections,
        "references": refs,
    }