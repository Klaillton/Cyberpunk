from __future__ import annotations

from fastapi import APIRouter

from motor.session_commands import build_session_commands

router = APIRouter(tags=["session"])


@router.get("/api/session-commands")
def session_commands() -> dict:
    return build_session_commands()