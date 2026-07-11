from __future__ import annotations

from fastapi import APIRouter

from motor.ollama_health import inspect_ollama
from motor.settings import get_settings

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
    settings = get_settings()
    payload: dict = {
        "status": "ok",
        "version": API_VERSION,
        "features": list(API_FEATURES),
        "provider": settings.provider,
    }
    if settings.provider == "ollama":
        ollama = inspect_ollama(settings)
        payload["ollama"] = ollama
        if not ollama.get("reachable"):
            payload["status"] = "degraded"
        elif not ollama.get("narration_ready"):
            payload["status"] = "degraded"
    return payload