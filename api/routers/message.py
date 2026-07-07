from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas import MessageRequest, MessageResponse
from motor.narration import generate_reply
from motor.settings import get_settings
from motor.update_service import UpdateService

router = APIRouter(tags=["message"])


def _process_message(channel: str, body: MessageRequest) -> MessageResponse:
    message = body.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail={"error": "Campo 'message' e obrigatorio"})

    mode = "narrador" if channel == "narrador" else "gestor"
    settings = get_settings()
    raw_reply = generate_reply(message, mode)
    update_service = UpdateService(settings)
    reply, proposals, _report = update_service.ingest_narrative(raw_reply)
    model = settings.ollama_model_narration if settings.provider == "ollama" else None
    return MessageResponse(
        channel=channel,
        provider=settings.provider,
        reply=reply,
        model=model,
        update_proposals=[proposal.to_dict() for proposal in proposals],
    )


@router.post("/api/narracao", response_model=MessageResponse)
def post_narracao(body: MessageRequest) -> MessageResponse:
    return _process_message("narracao", body)


@router.post("/api/narrador", response_model=MessageResponse)
def post_narrador(body: MessageRequest) -> MessageResponse:
    return _process_message("narrador", body)


@router.post("/api/message", response_model=MessageResponse)
def post_message(body: MessageRequest) -> MessageResponse:
    channel = (body.mode or "narracao").strip().lower()
    if channel not in {"narracao", "narrador", "gestor"}:
        channel = "narracao"
    api_channel = "narrador" if channel == "narrador" else "narracao"
    return _process_message(api_channel, body)