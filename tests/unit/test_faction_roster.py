from __future__ import annotations

from motor.character_creation.faction_roster import seed_faction_roster
from motor.settings import reset_settings


def test_seed_pack_roster_skips_existing() -> None:
    settings = reset_settings()
    result = seed_faction_roster("pack_badlands", settings=settings, dry_run=False)
    assert "reyes" in result.skipped
    assert "rusty" in result.skipped or "rusty" in result.created