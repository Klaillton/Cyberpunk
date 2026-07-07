from __future__ import annotations

from pathlib import Path

import pytest

from motor.settings import reset_settings
from motor.update.applier import UpdateApplier
from motor.update.models import UpdateProposal

HEAT_SAMPLE = """# Heat

## Heat por Personagem

| Personagem | Nivel de Heat | Justificativa |
| ---------- | ------------- | ------------- |
| **Ryan** | Media | Base |
"""


@pytest.fixture
def applier(tmp_path: Path) -> UpdateApplier:
    settings = reset_settings()
    settings.campanha_root = tmp_path
    settings.data_dir = tmp_path / "data"
    settings.db_path = settings.data_dir / "motor.db"
    settings.faiss_dir = settings.data_dir / "faiss"
    (tmp_path / "heat.md").write_text(HEAT_SAMPLE, encoding="utf-8")
    return UpdateApplier(settings)


def test_update_applier_inserts_heat_row(applier: UpdateApplier, tmp_path: Path) -> None:
    proposal = UpdateProposal(
        target_path="heat.md",
        target_section="Heat por Personagem",
        change_type="insert_row",
        payload={
            "personagem": "Ryan Wireghost",
            "nivel": "Alta",
            "justificativa": "Operacao exposta",
        },
        rationale="Teste",
        confidence=0.9,
    )
    report = applier.apply([proposal])

    assert report.applied == 1
    content = (tmp_path / "heat.md").read_text(encoding="utf-8")
    assert "Ryan Wireghost" in content
    assert "Alta" in content


def test_update_applier_inserts_row_before_next_section(applier: UpdateApplier, tmp_path: Path) -> None:
    sample = """# Heat

### Heat por Personagem

| Personagem | Nivel | Justificativa |
| ---------- | ----- | ------------- |
| **Ryan** | Media | Base |

## Fatores que Aumentam o Heat

- Item canonico.
"""
    (tmp_path / "heat.md").write_text(sample, encoding="utf-8")
    proposal = UpdateProposal(
        target_path="heat.md",
        target_section="Heat por Personagem",
        change_type="insert_row",
        payload={
            "personagem": "E2E Runner",
            "nivel": "Baixa",
            "justificativa": "Teste",
        },
        rationale="Teste",
        confidence=0.9,
    )
    report = applier.apply([proposal])
    content = (tmp_path / "heat.md").read_text(encoding="utf-8")

    assert report.applied == 1
    assert "| **E2E Runner** | Baixa | Teste |" in content
    assert "| **E2E Runner** | Baixa | Teste |\n\n## Fatores" in content