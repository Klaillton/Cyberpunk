from __future__ import annotations

from pathlib import Path

import pytest

import narracao_engine as engine
from motor.context_service import ContextService
from motor.settings import reset_settings


def test_context_service_merges_regex_paths(repo_root: Path) -> None:
    settings = reset_settings()
    service = ContextService(settings)
    selection = service.select(
        "Qual o heat e exposicao da crew?",
        provider="ollama",
        channel="narracao",
    )
    rel = {path.relative_to(repo_root).as_posix() for path in selection.paths}
    assert "heat.md" in rel
    assert selection.manifest.total_chars > 0


def test_context_service_skips_faiss_for_mestre_channel(repo_root: Path) -> None:
    settings = reset_settings()
    service = ContextService(settings)
    selection = service.select(
        "Tomas parece nervoso — o NPC ja se tornou traidor?",
        provider="ollama",
        channel="mestre",
    )
    assert selection.faiss_hits == 0
    rel = {path.relative_to(repo_root).as_posix() for path in selection.paths}
    assert "fichas/npc/tomas_recruit.md" in rel


def test_context_service_entity_paths_include_valk_message(repo_root: Path, monkeypatch) -> None:
    settings = reset_settings()
    service = ContextService(settings)

    def fake_search(self, query: str, top_k: int = 8, doc_types=None):
        from motor.search_service import SearchResult

        return SearchResult(hits=[], index_size=0)

    monkeypatch.setattr("motor.context_service.SearchService.search", fake_search)

    selection = service.select(
        "Quero falar com Valk sobre o acampamento",
        provider="ollama",
        channel="narracao",
    )
    rel = {path.relative_to(repo_root).as_posix() for path in selection.paths}
    assert any("valk" in item.lower() or "board" in item for item in rel)


def test_context_service_respects_ollama_max_files(repo_root: Path) -> None:
    settings = reset_settings()
    service = ContextService(settings)
    selection = service.select(
        "heat reputacao economia npc pulso valk reyes tomas",
        provider="ollama",
        channel="narracao",
    )
    assert len(selection.paths) <= engine.DEFAULT_OLLAMA_MAX_CONTEXT_FILES