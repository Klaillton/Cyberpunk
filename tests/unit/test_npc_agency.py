from __future__ import annotations

from motor.llm.quality_gate import ResponseQualityGate
from motor.llm.types import ContextManifest
from motor.npc_agency import (
    agency_context_paths,
    build_agency_prompt_block,
    is_delegation_turn,
    is_npc_agency_turn,
    is_passive_observation_turn,
    reply_passes_delegation_check,
)


def test_is_delegation_turn_valk_hunt_plan() -> None:
    msg = "Valk, quero cacar aves amanha. Planeja rota, horario e equipamento para mim."
    assert is_delegation_turn(msg)
    assert is_npc_agency_turn(msg)


def test_is_passive_observation_turn() -> None:
    assert is_passive_observation_turn("*observo em silencio enquanto eles falam*")


def test_agency_context_paths_includes_valk_pulso() -> None:
    paths = agency_context_paths("Valk, planeja a caca das aves")
    assert "sistema/npc_agencia_cena.md" in paths
    assert "pulso_do_mundo/crew/valk.md" in paths


def test_build_agency_prompt_block_anti_loop() -> None:
    history = [
        {"role": "user", "content": "Valk, planeja a caca das aves"},
        {"role": "assistant", "content": "Qual rota voce prefere?"},
    ]
    block = build_agency_prompt_block("Valk, planeja de novo", history)
    assert "ANTI-LOOP" in block
    assert "DELEGACAO" in block


def test_reply_passes_delegation_rejects_ping_pong() -> None:
    player = "Valk, planeja a caca das aves amanha"
    bad = "Qual rota voce prefere: A leste ou B oeste?"
    good = (
        '[NPC-F: Valk] "Saida 05h20 pelo leste do acampamento. Mule ate o canion; '
        'depois a pe. Rusty no radio; volta 10h30."'
    )
    assert reply_passes_delegation_check(bad, player) is False
    assert reply_passes_delegation_check(good, player) is True


def test_quality_gate_rejects_planning_ping_pong_on_delegation() -> None:
    gate = ResponseQualityGate()
    manifest = ContextManifest(total_chars=2000, entity_ids=["ryan_wireghost_voss", "valk"])
    player = "Valk, planeja a caca das aves amanha cedo"
    reply = "Como voce prefere planejar a saida? Opcao A ou B?"
    report = gate.validate(reply, manifest, channel="narracao", player_message=player, tier="standard")
    assert report.passed is False
    assert any(c.name == "delegation_fulfilled" and not c.passed for c in report.checks)


def test_quality_gate_accepts_valk_plan_delivery() -> None:
    gate = ResponseQualityGate()
    manifest = ContextManifest(
        total_chars=2000,
        entity_ids=["ryan_wireghost_voss", "lena_valk_kane"],
        source_paths=["fichas/nomad - lena_valk_kane.md"],
    )
    player = "Valk, planeja a caca das aves amanha"
    reply = (
        '[NPC-F:Valk] "05h20, rota pelo leste ate o canion. Mule no perimetro; '
        'Rusty no radio. Equipamento: rifle leve e kit de campo. Volta 10h30."'
    )
    report = gate.validate(reply, manifest, channel="narracao", player_message=player, tier="standard")
    assert report.passed is True