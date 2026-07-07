from __future__ import annotations

from pathlib import Path

import pytest

from motor.markdown.sync_engine import SyncEngine
from motor.settings import Settings, reset_settings


VALK_MD = """# Lena "Valk" Kane

## Nucleo

Pilota do The Mule e parceira de Ryan.
"""


@pytest.fixture
def indexed_campaign(tmp_path: Path) -> Settings:
    fichas = tmp_path / "fichas"
    fichas.mkdir(parents=True)
    (fichas / "nomad - lena_valk_kane.md").write_text(VALK_MD, encoding="utf-8")

    settings = reset_settings()
    settings.campanha_root = tmp_path
    settings.data_dir = tmp_path / "data"
    settings.db_path = settings.data_dir / "motor.db"
    settings.faiss_dir = settings.data_dir / "faiss"
    return settings


def test_sync_engine_writes_documents_and_aliases(indexed_campaign: Settings) -> None:
    engine = SyncEngine(indexed_campaign)
    report = engine.full_sync()

    assert report.documents_synced == 1
    assert report.chunks_written >= 1
    assert report.aliases_written >= 1

    row = engine.conn.execute(
        "SELECT entity_id, doc_type FROM documents WHERE path = ?",
        ("fichas/nomad - lena_valk_kane.md",),
    ).fetchone()
    assert row["entity_id"] == "lena_valk_kane"
    assert row["doc_type"] == "character"

    alias = engine.conn.execute(
        "SELECT alias FROM entity_aliases WHERE normalized = ?",
        ("valk",),
    ).fetchone()
    assert alias is not None
    assert alias["alias"] == "Valk"