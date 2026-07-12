from __future__ import annotations

import re
from pathlib import Path

from motor.npc import find_image_with_base, list_campaign_sheets
from motor.settings import Settings, get_settings


def _slug_from_stem(stem: str) -> str:
    if " - " in stem:
        return stem.split(" - ", 1)[1].strip().lower()
    return stem.strip().lower()


def resolve_sheet_path(character_id: str, settings: Settings | None = None) -> Path | None:
    cfg = settings or get_settings()
    target = character_id.strip().lower()
    if not target:
        return None

    matches: list[Path] = []
    for entry in list_campaign_sheets(cfg):
        slug = entry.get("slug", "").strip().lower()
        if slug == target:
            matches.append(cfg.campanha_root / entry["rel"])

    for root in (cfg.campanha_root, cfg.repo_root):
        fichas = root / "fichas"
        if not fichas.exists():
            continue
        for path in fichas.rglob("*.md"):
            if _slug_from_stem(path.stem) == target:
                matches.append(path)
        if matches:
            break

    if not matches:
        return None
    return sorted(matches, key=lambda p: len(p.name))[0]


def resolve_relationships_path(character_id: str, settings: Settings | None = None) -> Path:
    cfg = settings or get_settings()
    rel_dir = cfg.campanha_root / "relacionamentos"
    safe = re.sub(r"[^a-zA-Z0-9_-]", "_", character_id).lower()
    candidate = rel_dir / f"{safe}_relacionamentos.md"
    if candidate.exists():
        return candidate
    legacy = rel_dir / "ryan_relacionamentos.md"
    if character_id == cfg.character_id and legacy.exists():
        return legacy
    return candidate


def resolve_image_path(character_id: str, settings: Settings | None = None) -> Path | None:
    cfg = settings or get_settings()
    sheet = resolve_sheet_path(character_id, cfg)
    if sheet is None:
        return None
    base = sheet.stem
    found = find_image_with_base(base, token=False, settings=cfg)
    if found is not None:
        return found
    slug = _slug_from_stem(sheet.stem)
    for entry in list_campaign_sheets(cfg):
        if entry.get("slug", "").lower() == slug:
            role = entry.get("role", "")
            alt = find_image_with_base(f"{role} - {slug}", token=False, settings=cfg)
            if alt is not None:
                return alt
    return None