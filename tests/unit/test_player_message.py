from __future__ import annotations

from motor.player_message import format_player_message_for_prompt, parse_player_message


def test_parse_player_message_splits_action_speech_and_beat() -> None:
    raw = (
        "Estou encostado na cerca fumando.\n"
        '_ A manhã está lenta. *Falo para mim mesmo*'
    )
    parsed = parse_player_message(raw)
    assert any("cerca" in item for item in parsed.actions)
    assert any("manhã" in item or "manha" in item for item in parsed.speeches)
    assert any("mim mesmo" in item for item in parsed.beats)


def test_parse_player_message_supports_explicit_tags() -> None:
    raw = (
        "[Ação] Ryan atravessa a sala.\n"
        '[Fala] Eu cheguei!\n'
        "[Beat] Olha pela janela."
    )
    parsed = parse_player_message(raw)
    assert parsed.actions == ["Ryan atravessa a sala."]
    assert parsed.speeches == ["Eu cheguei!"]
    assert parsed.beats == ["Olha pela janela."]


def test_format_player_message_for_prompt_marks_completed_actions() -> None:
    parsed = parse_player_message('[Fala] "Oi, Elias."')
    block = format_player_message_for_prompt(parsed)
    assert "JA aconteceu" in block or "ja ditas" in block.lower()
    assert "Falas" in block
    assert "Oi, Elias." in block