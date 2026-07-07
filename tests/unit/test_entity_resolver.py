from __future__ import annotations

from pathlib import Path

import pytest

from motor.entities.entity_resolver import EntityResolver
from motor.markdown.sync_engine import SyncEngine
from motor.settings import reset_settings


@pytest.fixture
def resolver(tmp_path: Path) -> EntityResolver:
    fichas = tmp_path / "fichas"
    fichas.mkdir(parents=True)
    (fichas / "nomad - lena_valk_kane.md").write_text('# Lena "Valk" Kane\n\nPilota.\n', encoding="utf-8")

    settings = reset_settings()
    settings.campanha_root = tmp_path
    settings.data_dir = tmp_path / "data"
    settings.db_path = settings.data_dir / "motor.db"
    settings.faiss_dir = settings.data_dir / "faiss"

    engine = SyncEngine(settings)
    engine.full_sync()
    return EntityResolver(engine.conn)


def test_entity_resolver_maps_valk_alias(resolver: EntityResolver) -> None:
    result = resolver.resolve("Vou falar com Valk sobre o Mule")
    assert "lena_valk_kane" in result.character_ids
    assert result.confidence >= 0.6
    assert any(alias.lower() == "valk" for alias in result.keywords)