from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from api.schemas import SaveRequest, SaveResponse
from motor.update.models import ApplyReport
from motor.update_service import UpdateService

router = APIRouter(tags=["save"])


@router.post("/api/save", response_model=SaveResponse)
def save_proposals(body: SaveRequest):
    if not body.proposal_ids:
        raise HTTPException(status_code=400, detail={"error": "Campo 'proposal_ids' e obrigatorio"})

    service = UpdateService()
    result = service.save_proposals(body.proposal_ids, approved=body.approved)

    if isinstance(result, dict) and result.get("validation_issues"):
        return JSONResponse(status_code=422, content=result)

    report: ApplyReport = result
    return SaveResponse(
        applied=report.applied,
        files_changed=report.files_changed,
        sync_report=report.sync_report,
        errors=report.errors,
    )