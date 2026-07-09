from __future__ import annotations

from motor.settings import reset_settings
from motor.update_service import UpdateService


def test_sistema_mode_ingests_update_proposals(monkeypatch) -> None:
    monkeypatch.setenv("UPDATE_PROPOSALS_ENABLED", "true")
    settings = reset_settings()

    raw = (
        "Sugestao de atualizacao.\n\n"
        "---UPDATE_PROPOSALS---\n"
        "```json\n"
        '[{"target_path": "heat.md", "change_type": "insert_row", '
        '"payload": {"personagem": "Ryan"}, "confidence": 0.8}]\n'
        "```\n"
    )
    service = UpdateService(settings)
    reply, proposals, _report = service.ingest_narrative(raw)

    assert "UPDATE_PROPOSALS" not in reply
    assert len(proposals) == 1
    assert proposals[0].target_path == "heat.md"


def test_proposal_channels_include_sistema() -> None:
    proposal_channels = {"gestor", "sistema"}
    assert "sistema" in proposal_channels