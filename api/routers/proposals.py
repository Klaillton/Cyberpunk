from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas import IngestProposalsRequest, IngestProposalsResponse, ProposalsListResponse
from motor.update_service import UpdateService

router = APIRouter(tags=["proposals"])


@router.get("/api/proposals", response_model=ProposalsListResponse)
def list_pending_proposals() -> ProposalsListResponse:
    service = UpdateService()
    pending = service.list_pending()
    return ProposalsListResponse(proposals=[proposal.to_dict() for proposal in pending])


@router.post("/api/proposals/ingest", response_model=IngestProposalsResponse)
def ingest_proposals(body: IngestProposalsRequest) -> IngestProposalsResponse:
    narrative = body.narrative.strip()
    if not narrative:
        raise HTTPException(status_code=400, detail={"error": "Campo 'narrative' e obrigatorio"})

    service = UpdateService()
    clean, stored, report = service.ingest_narrative(narrative)
    return IngestProposalsResponse(
        narrative=clean,
        proposals=[proposal.to_dict() for proposal in stored],
        validation={
            "valid": report.valid,
            "issues": [
                {
                    "proposal_id": issue.proposal_id,
                    "code": issue.code,
                    "message": issue.message,
                    "severity": issue.severity,
                }
                for issue in report.issues
            ],
        },
    )