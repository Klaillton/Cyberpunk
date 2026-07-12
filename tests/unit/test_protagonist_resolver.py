from __future__ import annotations

from motor.character_creation.resolver import resolve_sheet_path
from motor.settings import reset_settings


def test_resolve_ryan_sheet() -> None:
    settings = reset_settings()
    path = resolve_sheet_path("ryan_wireghost_voss", settings)
    assert path is not None
    assert "ryan_wireghost_voss" in path.name


def test_resolve_alex_crew_sheet() -> None:
    settings = reset_settings()
    path = resolve_sheet_path("alex_specter_kane", settings)
    assert path is not None
    assert "alex_specter_kane" in path.name