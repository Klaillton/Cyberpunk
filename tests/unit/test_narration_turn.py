from __future__ import annotations

from unittest.mock import patch

from motor.llm.types import QualityCheck, QualityReport
from motor.narration import generate_turn
from motor.settings import reset_settings


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
        "Ryan observa Tomas de longe no acampamento do Pack, sem se aproximar ainda. "
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