from __future__ import annotations

import json
from io import BytesIO
from unittest.mock import patch

import pytest

from motor.journal import journal_file, load_journal_entries, save_journal_entries
from motor.markdown.tree import parse_markdown_tree
from motor.narration import format_provider_failure, generate_reply, run_ollama
from motor.npc import normalize_name
from motor.settings import get_settings, reset_settings

@pytest.fixture(autouse=True)
def _ollama_preflight_passes(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("motor.narration._ollama_preflight_message", lambda _cfg: None)


SAMPLE_MARKDOWN = """---
id: test_npc
type: npc
---

# Test NPC

## Núcleo Permanente

- **Personalidade:** Calma.

## Estado Atual

| Campo | Valor |
| ----- | ----- |
| Humor | Neutro |
"""


def test_parse_markdown_tree_extracts_sections() -> None:
    tree = parse_markdown_tree(SAMPLE_MARKDOWN)
    assert tree["title"] == "Test NPC"
    sections = tree["sections"]
    assert len(sections) >= 2
    titles = [str(s["title"]) for s in sections]
    assert "Núcleo Permanente" in titles
    assert "Estado Atual" in titles


def test_journal_roundtrip(tmp_path, monkeypatch) -> None:
    journal_dir = tmp_path / "journal"
    journal_dir.mkdir()
    settings = reset_settings()
    monkeypatch.setattr(settings, "journal_dir", journal_dir)

    save_journal_entries(
        "test_char",
        [{"id": "e1", "timestamp": "01/01/2026", "text": "nota A"}],
        settings,
    )
    loaded = load_journal_entries("test_char", settings)
    assert len(loaded) == 1
    assert loaded[0]["text"] == "nota A"
    assert journal_file("test_char", settings).exists()


def test_format_provider_failure_ollama_connection() -> None:
    msg = format_provider_failure("ollama", ConnectionError("refused"))
    assert "Ollama indisponivel" in msg


def test_format_provider_failure_ollama_cuda() -> None:
    msg = format_provider_failure(
        "ollama",
        RuntimeError('Ollama HTTP 500: {"error":"CUDA error: unknown error"}'),
    )
    assert "Erro CUDA" in msg
    assert "OLLAMA_NUM_GPU" in msg


def test_run_ollama_retries_with_lower_gpu_on_cuda_error() -> None:
    calls: list[int | None] = []
    cuda_error = RuntimeError('Ollama HTTP 500: {"error":"CUDA error: unknown error"}')
    ok_payload = json.dumps({"response": "Cena local ok."}).encode("utf-8")

    def fake_generate_once(*_args, num_gpu=None, **_kwargs):
        calls.append(num_gpu)
        if num_gpu and num_gpu >= 28:
            raise cuda_error
        return "Cena local ok."

    with patch("motor.narration._ollama_generate_once", side_effect=fake_generate_once):
        settings = reset_settings()
        settings.ollama_num_gpu = 28
        text = run_ollama("prompt", settings)
    assert text == "Cena local ok."
    assert calls == [28, 14]


def test_run_ollama_parses_response() -> None:
    payload = json.dumps({"response": "Narrativa local."}).encode("utf-8")

    def fake_urlopen(request, timeout=600):
        assert request.full_url.endswith("/api/generate")
        body = json.loads(request.data.decode("utf-8"))
        assert body["stream"] is False
        return BytesIO(payload)

    with patch("motor.narration.urllib.request.urlopen", fake_urlopen):
        text = run_ollama("prompt de teste")
    assert text == "Narrativa local."


def test_generate_reply_none_provider_mestre_channel(monkeypatch) -> None:
    settings = get_settings()
    monkeypatch.setattr(settings, "provider", "none")
    reply = generate_reply("Pergunta off-game", mode="mestre", settings=settings, channel="mestre")
    assert "Canal Mestre off-game ativo" in reply


def test_update_proposals_disabled_for_ollama_by_default(monkeypatch) -> None:
    monkeypatch.setenv("NARRACAO_PROVIDER", "ollama")
    monkeypatch.delenv("UPDATE_PROPOSALS_ENABLED", raising=False)
    settings = reset_settings()
    assert settings.update_proposals_enabled is False


def test_generate_reply_ollama_provider(monkeypatch) -> None:
    settings = get_settings()
    monkeypatch.setattr(settings, "provider", "ollama")
    monkeypatch.setattr(settings, "quality_rescue_cloud_enabled", False)
    long_reply = (
        "O vento levanta po no acampamento enquanto os recrutas observam o perimetro em silencio."
    )
    with patch("motor.narration.run_ollama", return_value=long_reply):
        reply = generate_reply("Avanco na cena", mode="narrador", settings=settings)
    assert reply == long_reply


def test_normalize_name_strips_punctuation() -> None:
    assert normalize_name("Lena \"Valk\" Kane") == "lenavalkkane"