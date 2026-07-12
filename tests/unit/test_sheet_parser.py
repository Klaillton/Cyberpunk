from __future__ import annotations

from pathlib import Path

from motor.character_creation.sheet_parser import parse_character_sheet
from motor.settings import reset_settings


def test_parse_ryan_stats_from_table() -> None:
    settings = reset_settings()
    path = settings.repo_root / "fichas" / "techie - ryan_wireghost_voss.md"
    sheet = parse_character_sheet(path, settings=settings)
    assert sheet["tier"] in {"protagonist", "npc_reference", "crew_full"}
    assert sheet["stats"].get("TECH") == 8
    assert sheet["stats"].get("INT") == 7


def test_parse_valk_skills_table() -> None:
    settings = reset_settings()
    path = settings.repo_root / "fichas" / "nomad - lena_valk_kane.md"
    sheet = parse_character_sheet(path, settings=settings)
    assert sheet["stats"].get("REF") == 8
    assert sheet["skills"].get("Drive Land Vehicle") == 6


def test_parse_rusty_reference_tier() -> None:
    settings = reset_settings()
    path = settings.repo_root / "fichas" / "npc" / "rusty.md"
    sheet = parse_character_sheet(path, settings=settings)
    assert sheet["tier"] == "npc_reference"
    assert sheet["layout"] == "cpr_reference"