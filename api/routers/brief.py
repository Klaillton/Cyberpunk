from __future__ import annotations

from fastapi import APIRouter

from motor.brief_service import build_campaign_brief

router = APIRouter(tags=["brief"])


@router.get("/api/brief")
def campaign_brief() -> dict:
    return build_campaign_brief()