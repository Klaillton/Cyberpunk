from __future__ import annotations

from motor.settings import Settings, get_settings
from motor.update.models import UpdateProposal, ValidationIssue, ValidationReport
from motor.update.paths import (
    ALLOWED_CHANGE_TYPES,
    HEAT_PATH_HINTS,
    RELATIONSHIP_PATH_HINTS,
    normalize_target_path,
    resolve_target_file,
)

_HEAT_LEVELS = {"baixa": 1, "low": 1, "media": 2, "média": 2, "medium": 2, "alta": 3, "high": 3}
_TIME_KEYWORDS = ("tempo", "semana", "dia", "mes", "mês", "passou", "downtime", "periodo", "período")


class UpdateValidator:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def validate(self, proposals: list[UpdateProposal]) -> ValidationReport:
        issues: list[ValidationIssue] = []
        accepted: list[UpdateProposal] = []

        for proposal in proposals:
            proposal_issues = self._validate_one(proposal)
            issues.extend(proposal_issues)
            if not any(issue.severity == "error" for issue in proposal_issues):
                accepted.append(proposal)

        return ValidationReport(valid=len(issues) == 0 or bool(accepted), issues=issues, accepted=accepted)

    def _validate_one(self, proposal: UpdateProposal) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        rel_path = normalize_target_path(proposal.target_path)

        if proposal.change_type not in ALLOWED_CHANGE_TYPES:
            issues.append(
                ValidationIssue(
                    proposal_id=proposal.id,
                    code="INVALID_CHANGE_TYPE",
                    message=f"change_type invalido: {proposal.change_type}",
                )
            )

        target = resolve_target_file(proposal.target_path, self.settings.campanha_root)
        if target is None or not target.exists():
            if proposal.change_type != "append":
                issues.append(
                    ValidationIssue(
                        proposal_id=proposal.id,
                        code="TARGET_NOT_FOUND",
                        message=f"Arquivo alvo nao encontrado: {rel_path}",
                    )
                )

        if proposal.confidence < 0.35:
            issues.append(
                ValidationIssue(
                    proposal_id=proposal.id,
                    code="LOW_CONFIDENCE",
                    message="Confianca abaixo do limiar recomendado",
                    severity="warning",
                )
            )

        issues.extend(self._validate_relationship_delta(proposal, rel_path))
        issues.extend(self._validate_heat_change(proposal, rel_path))
        return issues

    def _validate_relationship_delta(self, proposal: UpdateProposal, rel_path: str) -> list[ValidationIssue]:
        if not any(hint in rel_path.lower() for hint in RELATIONSHIP_PATH_HINTS):
            return []

        payload = proposal.payload
        delta = payload.get("delta")
        if delta is None and "value" in payload and "previous" in payload:
            try:
                delta = float(payload["value"]) - float(payload["previous"])
            except (TypeError, ValueError):
                delta = None

        if delta is None:
            return []

        try:
            delta_value = float(delta)
        except (TypeError, ValueError):
            return [
                ValidationIssue(
                    proposal_id=proposal.id,
                    code="INVALID_DELTA",
                    message="Delta de relacionamento invalido",
                )
            ]

        if abs(delta_value) > 20:
            return [
                ValidationIssue(
                    proposal_id=proposal.id,
                    code="RELATIONSHIP_DELTA_EXCEEDED",
                    message=f"Mudanca de relacionamento ({delta_value:+.0f}) excede limite de 20 por turno",
                )
            ]
        return []

    def _validate_heat_change(self, proposal: UpdateProposal, rel_path: str) -> list[ValidationIssue]:
        if not any(hint in rel_path.lower() for hint in HEAT_PATH_HINTS):
            return []
        if proposal.change_type not in {"insert_row", "upsert_field", "replace"}:
            return []

        payload = proposal.payload
        new_level = str(payload.get("nivel") or payload.get("level") or "").strip().lower()
        previous = str(payload.get("previous") or payload.get("nivel_anterior") or "").strip().lower()
        if not new_level or not previous:
            return []

        new_score = _HEAT_LEVELS.get(new_level)
        prev_score = _HEAT_LEVELS.get(previous)
        if new_score is None or prev_score is None:
            return []

        if new_score < prev_score:
            rationale = f"{proposal.rationale} {payload.get('justificativa', '')}".lower()
            if not any(keyword in rationale for keyword in _TIME_KEYWORDS):
                return [
                    ValidationIssue(
                        proposal_id=proposal.id,
                        code="HEAT_DECREASE_WITHOUT_TIME",
                        message="Reducao de heat exige justificativa temporal na rationale",
                    )
                ]
        return []