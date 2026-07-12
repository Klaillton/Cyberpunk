from __future__ import annotations

from motor.character_creation.validator import validate_complete_package


def _valid_draft() -> dict:
    return {
        "name": "Test Char",
        "slug": "test_char",
        "role": "solo",
        "role_ability_rank": 4,
        "stats": {
            "INT": 6,
            "REF": 8,
            "DEX": 6,
            "TECH": 5,
            "COOL": 6,
            "WILL": 6,
            "LUCK": 4,
            "MOVE": 6,
            "BODY": 8,
            "EMP": 7,
        },
        "skills": {"Perception": 6, "Streetwise": 6, "Education": 2},
    }


def test_validate_complete_package_passes_with_pools_adjusted() -> None:
    draft = _valid_draft()
    # Ajuste rápido: 62 stats já ok; skills precisam somar 86 — preencher genérico
    draft["skills"] = {f"Skill{i}": 2 for i in range(43)}
    report = validate_complete_package(draft)
    assert report.passed is True


def test_validate_rejects_stat_pool() -> None:
    draft = _valid_draft()
    draft["stats"]["INT"] = 10
    report = validate_complete_package(draft)
    assert report.passed is False
    assert any(issue.code == "range" for issue in report.issues)