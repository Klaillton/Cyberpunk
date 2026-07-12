from __future__ import annotations

from unittest.mock import patch

import pytest

from motor.llm.types import QualityCheck, QualityReport
from motor.narration import generate_turn
from motor.settings import reset_settings


@pytest.fixture(autouse=True)
def _ollama_preflight_passes(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("motor.narration._ollama_preflight_message", lambda _cfg: None)


def test_generate_turn_logs_routing_and_returns_metadata(monkeypatch) -> None:
    settings = reset_settings()
    settings.provider = "ollama"
    settings.llm_routing_policy = "local_only"

    long_reply = (
        "Ryan permanece encostado no muro do acampamento, observando Elias na destilaria "
        "enquanto Tomas fuma mais afastado. O sol da manha ainda e baixo nas Badlands."
    )

    with patch("motor.narration.run_ollama", return_value=long_reply):
        turn = generate_turn(
            "Observo o acampamento e os recrutas.",
            mode="narrador",
            settings=settings,
            channel="narracao",
        )

    assert turn.reply == long_reply
    assert turn.routing_decision is not None
    assert turn.routing_decision.provider == "ollama"
    assert turn.quality_report is not None
    assert turn.quality_report.passed is True
    assert turn.attempts == 1
    assert turn.context_sources


def test_generate_turn_retries_on_quality_failure(monkeypatch) -> None:
    settings = reset_settings()
    settings.provider = "ollama"
    settings.llm_routing_policy = "local_only"
    settings.cloud_fallback_enabled = False

    bad_reply = "Curto."
    good_reply = (
        "O cheiro de solvente da destilaria corta o ar da manha nas Badlands. "
        "Elias segue na destilaria e Mara carrega suprimentos com outros nomades."
    )
    calls: list[str] = []

    def fake_ollama(prompt: str, *args, **kwargs) -> str:
        calls.append(prompt)
        return bad_reply if len(calls) == 1 else good_reply

    with patch("motor.narration.run_ollama", side_effect=fake_ollama):
        turn = generate_turn(
            "Observo Tomas no acampamento.",
            mode="narrador",
            settings=settings,
            channel="narracao",
        )

    assert turn.attempts == 2
    assert turn.reply == good_reply
    assert "CORRECAO OBRIGATORIA" in calls[1]


def test_generate_turn_quality_rescue_uses_compact_grok_after_three_failures(
    monkeypatch,
    tmp_path,
) -> None:
    settings = reset_settings()
    settings.provider = "ollama"
    settings.ollama_model_narration = "llama3.1:8b"
    settings.llm_routing_policy = "local_only"
    settings.cloud_fallback_enabled = False
    settings.quality_rescue_cloud_enabled = True
    grok_stub = tmp_path / "grok.exe"
    grok_stub.write_text("", encoding="utf-8")
    settings.grok_bin = grok_stub

    bad_local = "Curto."
    grok_reply = (
        "O Mule estaciona entre as tendas; o ar da manha ainda e seco nas Badlands. "
        '[NPC-M: Reyes] "Ainda nao temos o alcance exato, mas precisamos preparar saidas."'
    )
    ollama_calls: list[int] = []
    grok_prompts: list[str] = []

    def fake_ollama(*args, **kwargs) -> str:
        ollama_calls.append(1)
        return bad_local

    def fake_grok(prompt: str) -> str:
        grok_prompts.append(prompt)
        return grok_reply

    with (
        patch("motor.narration.run_ollama", side_effect=fake_ollama),
        patch("narracao_engine.run_grok", side_effect=fake_grok),
    ):
        turn = generate_turn(
            'Volto no Mule com a Valk.\n\n"Quanto eles ja sabem?"',
            mode="narrador",
            settings=settings,
            channel="narracao",
        )

    assert len(ollama_calls) == 3
    assert len(grok_prompts) == 1
    assert len(grok_prompts[0]) <= settings.quality_rescue_max_chars
    assert "## Resumo da cena (canon)" in grok_prompts[0]
    assert turn.reply == grok_reply
    assert turn.attempts == 4
    assert turn.routing_decision is not None
    assert turn.routing_decision.provider == "grok"
    assert "quality_gate:rescue_cloud" in turn.routing_decision.reasons


def test_generate_turn_skips_quality_for_mestre(monkeypatch) -> None:
    settings = reset_settings()
    settings.provider = "ollama"
    settings.llm_routing_policy = "local_only"

    with patch("motor.narration.run_ollama", return_value="Canon atual: nao."):
        turn = generate_turn(
            "Tomas ja virou traidor?",
            mode="mestre",
            settings=settings,
            channel="mestre",
        )

    assert turn.quality_report is None
    assert turn.attempts == 1