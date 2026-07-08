from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["health"])

API_VERSION = "1.1.0"
API_FEATURES = (
    "brief",
    "session-commands",
    "npcs",
    "mestre",
    "sistema",
    "narracao",
)


@router.get("/api/health")
def health() -> dict:
    return {
        "status": "ok",
        "version": API_VERSION,
        "features": list(API_FEATURES),
    }