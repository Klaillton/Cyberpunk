from __future__ import annotations

from fastapi import APIRouter, HTTPException

from motor.character_creation.faction_roster import roster_template_path, seed_faction_roster
from motor.settings import get_settings

router = APIRouter(tags=["factions"])


@router.post("/api/factions/{faction_id}/seed-roster")
def seed_roster(faction_id: str, dry_run: bool = False) -> dict:
    settings = get_settings()
    template = roster_template_path(faction_id, settings)
    if not template.exists():
        raise HTTPException(status_code=404, detail="Roster de facção não encontrado.")
    result = seed_faction_roster(faction_id, settings=settings, dry_run=dry_run)
    return {
        "faction_id": result.faction_id,
        "created": result.created,
        "skipped": result.skipped,
        "dry_run": dry_run,
    }