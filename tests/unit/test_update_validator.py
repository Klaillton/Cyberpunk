from __future__ import annotations

from pathlib import Path

import pytest

from motor.settings import reset_settings
from motor.update.models import UpdateProposal
from motor.update.validator import UpdateValidator


@pytest.fixture
def validator(tmp_path: Path) -> UpdateValidator:
    settings = reset_settings()
    settings.campanha_root = tmp_path
    rel_dir = tmp_path / "relacionamentos"
    rel_dir.mkdir(parents=True)
    (rel_dir / "ryan_relacionamentos.md").write_text("# Relacionamentos\n", encoding="utf-8")
    return UpdateValidator(settings)


def test_update_validator_rejects_large_relationship_delta(validator: UpdateValidator) -> None:
    proposal = UpdateProposal(
        target_path="relacionamentos/ryan_relacionamentos.md",
        change_type="upsert_field",
        payload={"attribute": "trust", "delta": 25, "target": "lena_valk_kane"},
        rationale="Aumento abrupto",
        confidence=0.9,
    )
    report = validator.validate([proposal])

    assert report.accepted == []
    assert any(issue.code == "RELATIONSHIP_DELTA_EXCEEDED" for issue in report.issues)


def test_update_validator_accepts_small_relationship_delta(validator: UpdateValidator) -> None:
    proposal = UpdateProposal(
        target_path="relacionamentos/ryan_relacionamentos.md",
        change_type="upsert_field",
        payload={"attribute": "trust", "delta": 8, "target": "lena_valk_kane"},
        rationale="Pequeno avanco apos conversa",
        confidence=0.8,
    )
    report = validator.validate([proposal])
    assert len(report.accepted) == 1