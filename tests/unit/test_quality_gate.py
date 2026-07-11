from __future__ import annotations

from motor.llm.quality_gate import ResponseQualityGate
from motor.llm.types import ContextManifest


def test_quality_gate_rejects_invented_npc() -> None:
    gate = ResponseQualityGate()
    manifest = ContextManifest(
        total_chars=1000,
        entity_ids=["ryan_wireghost_voss", "lena_valk_kane"],
        source_paths=["board/board_campanha.md"],
    )
    report = gate.validate(
        "Captain Zorath aparece no acampamento e exige respostas imediatas de todos.",
        manifest,
        channel="narracao",
    )
    assert report.passed is False
    assert any(check.name == "known_entities" and not check.passed for check in report.checks)


def test_quality_gate_rejects_board_location_contradiction() -> None:
    gate = ResponseQualityGate()
    manifest = ContextManifest(
        total_chars=2000,
        entity_ids=["ryan_wireghost_voss"],
        board_excerpt="Local atual: acampamento do Pack nas Badlands.",
    )
    report = gate.validate(
        "A cena se passa em Night City, com chuva acida e neon em todos os predios.",
        manifest,
        channel="narracao",
    )
    assert report.passed is False
    assert any(check.name == "board_consistency" and not check.passed for check in report.checks)


def test_quality_gate_rejects_player_echo() -> None:
    gate = ResponseQualityGate()
    manifest = ContextManifest(
        total_chars=2000,
        entity_ids=["ryan_wireghost_voss", "lena_valk_kane", "reyes"],
    )
    player = (
        "Eu saio da tenda em direcao ao refeitorio, Valk me acompanha, estamos de maos dadas "
        "e conversando sobre coisas simples"
    )
    reply = (
        "Voce sai da tenda em direcao ao refeitorio, Valk o acompanha, voces estao de maos dadas "
        "e conversando sobre coisas simples. O sol esta alto no ceu."
    )
    report = gate.validate(
        reply,
        manifest,
        channel="narracao",
        player_message=player,
    )
    assert report.passed is False
    assert any(check.name == "player_echo" and not check.passed for check in report.checks)


def test_quality_gate_rejects_narrator_repeat() -> None:
    gate = ResponseQualityGate()
    manifest = ContextManifest(
        total_chars=2000,
        entity_ids=["ryan_wireghost_voss", "lena_valk_kane", "reyes"],
    )
    previous = (
        "Valk solta sua mao para abracar Tio Gringo, enquanto voce continua a conversa sobre os planos do dia. "
        "O aroma do cafe se espalha pelo refeitorio."
    )
    reply = (
        "Valk solta sua mao para abracar Tio Gringo, enquanto voce continua a conversa sobre os planos do dia. "
        "Tio Gringo responde sobre a oficina."
    )
    report = gate.validate(
        reply,
        manifest,
        channel="narracao",
        previous_narrator=previous,
    )
    assert report.passed is False
    assert any(check.name == "narrator_repeat" and not check.passed for check in report.checks)


def test_quality_gate_rejects_meta_question() -> None:
    gate = ResponseQualityGate()
    manifest = ContextManifest(total_chars=1000, entity_ids=["ryan_wireghost_voss"])
    report = gate.validate(
        "Tio Gringo prepara o cafe. O que voce faz em seguida?",
        manifest,
        channel="narracao",
    )
    assert report.passed is False
    assert any(check.name == "meta_questions" and not check.passed for check in report.checks)


def test_quality_gate_rejects_ryan_protagonist_control() -> None:
    gate = ResponseQualityGate()
    manifest = ContextManifest(
        total_chars=2000,
        entity_ids=["ryan_wireghost_voss", "reyes"],
    )
    report = gate.validate(
        "Ryan olha para Reyes com um sorriso serio, assentindo com a cabeca.",
        manifest,
        channel="narracao",
    )
    assert report.passed is False
    assert any(check.name == "protagonist_control" and not check.passed for check in report.checks)


def test_quality_gate_rejects_npc_repeating_player_speech() -> None:
    gate = ResponseQualityGate()
    manifest = ContextManifest(
        total_chars=2000,
        entity_ids=["ryan_wireghost_voss", "reyes"],
    )
    player = (
        'Ryan fica serio e assente.\n\n'
        '"Quanto eles ja sabem? Mover o pack e uma alternativa?"'
    )
    reply = (
        'Reyes encara Ryan por um instante.\n'
        '[NPC-M: Reyes] "Quanto eles ja sabem? Mover o pack e uma alternativa?"'
    )
    report = gate.validate(
        reply,
        manifest,
        channel="narracao",
        player_message=player,
    )
    assert report.passed is False
    assert any(check.name == "npc_echo" and not check.passed for check in report.checks)


def test_quality_gate_rejects_camp_scene_when_player_in_mule() -> None:
    gate = ResponseQualityGate()
    manifest = ContextManifest(
        total_chars=2000,
        entity_ids=["ryan_wireghost_voss", "lena_valk_kane", "reyes"],
        board_excerpt="Local: Acampamento do Pack nas Badlands. Valk dormindo na tenda.",
    )
    player = (
        "Eu estou no Mule, Valk esta dirigindo pelas Badlands enquanto voltamos de uma Incursao"
    )
    reply = (
        "A manha continua fresca no acampamento. Valk dorme na tenda ao lado. "
        "Reyes discute com Tio Gringo enquanto Mara prepara o almoco."
    )
    report = gate.validate(
        reply,
        manifest,
        channel="narracao",
        player_message=player,
    )
    assert report.passed is False
    assert any(check.name == "scene_continuity" and not check.passed for check in report.checks)


def test_quality_gate_passes_consistent_reply() -> None:
    gate = ResponseQualityGate()
    manifest = ContextManifest(
        total_chars=2000,
        entity_ids=["ryan_wireghost_voss", "lena_valk_kane", "reyes"],
        board_excerpt="Acampamento do Pack nas Badlands.",
    )
    report = gate.validate(
        "Valk e Reyes conferem os geradores no acampamento enquanto o sol desce sobre as Badlands.",
        manifest,
        channel="narracao",
    )
    assert report.passed is True