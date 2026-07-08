from __future__ import annotations

from motor.session_commands import build_session_commands


def test_build_session_commands_exposes_documented_player_commands() -> None:
    data = build_session_commands()
    assert len(data["categories"]) == 3
    assert len(data["quick"]) == 3

    texts = {
        command["text"]
        for category in data["categories"]
        for command in category["commands"]
    }
    assert "[Resumo da Sessão]" in texts
    assert "[Finalizar sessão e gerar resumo]" in texts
    assert any("Pulso do Mundo" in text for text in texts)