from __future__ import annotations

from pathlib import Path

import pytest

from motor.index.embedder import TfidfEmbedder
from motor.index.faiss_index import FaissIndex
from motor.markdown.sync_engine import SyncEngine
from motor.settings import reset_settings


@pytest.fixture
def search_index(tmp_path: Path):
    fichas = tmp_path / "fichas"
    fichas.mkdir(parents=True)
    (fichas / "nomad - lena_valk_kane.md").write_text(
        '# Lena "Valk" Kane\n\n## Background\n\nMotorista estoica e confiavel do The Mule.\n',
        encoding="utf-8",
    )

    settings = reset_settings()
    settings.campanha_root = tmp_path
    settings.data_dir = tmp_path / "data"
    settings.db_path = settings.data_dir / "motor.db"
    settings.faiss_dir = settings.data_dir / "faiss"

    SyncEngine(settings).full_sync()
    vectors = FaissIndex(settings, embedder=TfidfEmbedder()).rebuild()
    assert vectors >= 1
    return settings


def test_faiss_search_returns_known_npc_chunk(search_index) -> None:
    index = FaissIndex(search_index, embedder=TfidfEmbedder())
    hits = index.search("Valk motorista The Mule", top_k=3)

    assert hits
    assert any("lena_valk_kane" in (hit.entity_id or "") for hit in hits)
    assert any("Motorista" in hit.preview for hit in hits)