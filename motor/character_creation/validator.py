from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from motor.character_creation.catalog import basic_skills
from motor.character_creation.rules import (
    ROLE_ABILITY_START,
    SKILL_BASIC_MIN,
    SKILL_MAX,
    SKILL_POOL,
    STAT_KEYS,
    STAT_MAX,
    STAT_MIN,
    STAT_POOL,
)


@dataclass
class ValidationIssue:
    field: str
    code: str
    message: str


@dataclass
class ValidationReport:
    passed: bool
    issues: list[ValidationIssue] = field(default_factory=list)


def validate_complete_package(draft: dict[str, Any]) -> ValidationReport:
    issues: list[ValidationIssue] = []

    stats = draft.get("stats") or {}
    if not isinstance(stats, dict):
        issues.append(ValidationIssue("stats", "invalid", "Atributos inválidos."))
        stats = {}

    total = 0
    for key in STAT_KEYS:
        value = stats.get(key)
        if value is None:
            issues.append(ValidationIssue("stats", "missing", f"STAT {key} ausente."))
            continue
        try:
            iv = int(value)
        except (TypeError, ValueError):
            issues.append(ValidationIssue("stats", "invalid", f"STAT {key} inválido."))
            continue
        total += iv
        if iv < STAT_MIN or iv > STAT_MAX:
            issues.append(
                ValidationIssue(
                    "stats",
                    "range",
                    f"STAT {key} deve estar entre {STAT_MIN} e {STAT_MAX}.",
                )
            )
    if total != STAT_POOL:
        issues.append(
            ValidationIssue(
                "stats",
                "pool",
                f"Distribua exatamente {STAT_POOL} pontos em STATs (atual: {total}).",
            )
        )

    skills = draft.get("skills") or {}
    if not isinstance(skills, dict):
        issues.append(ValidationIssue("skills", "invalid", "Skills inválidas."))
        skills = {}

    skill_total = 0
    for level in skills.values():
        try:
            skill_total += int(level)
        except (TypeError, ValueError):
            issues.append(ValidationIssue("skills", "invalid", "Nivel de skill invalido."))
    if skill_total != SKILL_POOL:
        issues.append(
            ValidationIssue(
                "skills",
                "pool",
                f"Distribua exatamente {SKILL_POOL} pontos em Skills (atual: {skill_total}).",
            )
        )
    for name, level in skills.items():
        try:
            lv = int(level)
        except (TypeError, ValueError):
            issues.append(ValidationIssue("skills", "invalid", f"Skill {name} inválida."))
            continue
        if lv > SKILL_MAX:
            issues.append(
                ValidationIssue("skills", "max", f"Skill {name} não pode passar de {SKILL_MAX}.")
            )
        base_name = str(name).split("(")[0].strip()
        if base_name in basic_skills() and lv < SKILL_BASIC_MIN:
            issues.append(
                ValidationIssue(
                    "skills",
                    "basic_min",
                    f"Skill básica {name} deve ser pelo menos {SKILL_BASIC_MIN}.",
                )
            )

    role = str(draft.get("role", "")).strip()
    if not role:
        issues.append(ValidationIssue("role", "required", "Escolha um Role."))

    ability = draft.get("role_ability_rank", ROLE_ABILITY_START)
    try:
        if int(ability) != ROLE_ABILITY_START:
            issues.append(
                ValidationIssue(
                    "role_ability_rank",
                    "start",
                    f"Role Ability deve iniciar em {ROLE_ABILITY_START}.",
                )
            )
    except (TypeError, ValueError):
        issues.append(ValidationIssue("role_ability_rank", "invalid", "Role Ability inválida."))

    name = str(draft.get("name", "")).strip()
    slug = str(draft.get("slug", "")).strip().lower()
    if not name:
        issues.append(ValidationIssue("name", "required", "Nome do personagem obrigatório."))
    if not slug or not slug.replace("_", "").isalnum():
        issues.append(ValidationIssue("slug", "invalid", "Slug inválido (use letras, números e _)."))

    return ValidationReport(passed=not issues, issues=issues)