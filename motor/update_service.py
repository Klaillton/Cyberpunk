from __future__ import annotations

from motor.settings import Settings, get_settings
from motor.update.applier import UpdateApplier
from motor.update.models import ApplyReport, UpdateProposal, ValidationReport
from motor.update.parser import UpdateParser
from motor.update.store import ProposalStore
from motor.update.validator import UpdateValidator


class UpdateService:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.parser = UpdateParser()
        self.validator = UpdateValidator(self.settings)
        self.applier = UpdateApplier(self.settings)
        self.store = ProposalStore(self.settings)

    def ingest_narrative(self, narrative: str) -> tuple[str, list[UpdateProposal], ValidationReport]:
        clean, proposals = self.parser.parse(narrative)
        if not proposals:
            return clean, [], ValidationReport(valid=True, accepted=[])

        report = self.validator.validate(proposals)
        stored = self.store.save_many(report.accepted)
        return clean, stored, report

    def list_pending(self) -> list[UpdateProposal]:
        return self.store.list_by_status("pending")

    def save_proposals(
        self,
        proposal_ids: list[str],
        *,
        approved: bool,
    ) -> ApplyReport | dict:
        proposals = self.store.get_by_ids(proposal_ids)
        if not proposals:
            return ApplyReport(applied=0, files_changed=[], sync_report={"sqlite": 0, "faiss_chunks_added": 0})

        if not approved:
            self.store.mark_status(proposal_ids, "rejected")
            return ApplyReport(applied=0, files_changed=[], sync_report={"sqlite": 0, "faiss_chunks_added": 0})

        report = self.validator.validate(proposals)
        if not report.accepted:
            return {
                "applied": 0,
                "files_changed": [],
                "sync_report": {"sqlite": 0, "faiss_chunks_added": 0},
                "validation_issues": [
                    {"proposal_id": issue.proposal_id, "code": issue.code, "message": issue.message}
                    for issue in report.issues
                    if issue.severity == "error"
                ],
            }

        apply_report = self.applier.apply(report.accepted)
        applied_ids = [proposal.id for proposal in report.accepted]
        self.store.mark_status(applied_ids, "applied")
        return apply_report