from __future__ import annotations

from motor.llm.quality_gate import ResponseQualityGate, is_simple_player_action
from motor.llm.types import ContextManifest


def test_is_simple_player_action_detects_workshop_visit() -> None:
    assert is_simple_player_action("Eu vou ate a oficina ver como esta o andamento dos projetos")


def test_quality_gate_relaxed_for_simple_action_echo() -> None:
    gate = ResponseQualityGate()
    manifest = ContextManifest(
        total_chars=2000,
        entity_ids=["ryan_wireghost_voss", "reyes"],
    )
    player = "Eu vou ate a oficina ver como esta o andamento dos projetos"
    reply = (
        "Ryan caminha em direcao a oficina improvisada. O cheiro de metal quente e oleo paira no ar. "
        "Ferramentas e projetos mecanicos ocupam as bancadas."
    )
    report = gate.validate(
        reply,
        manifest,
        channel="narracao",
        player_message=player,
        tier="standard",
    )
    assert report.passed is True