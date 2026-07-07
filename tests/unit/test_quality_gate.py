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