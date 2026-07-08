from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas import MessageRequest, MessageResponse
from motor.narration import generate_reply
from motor.settings import get_settings
from motor.update_service import UpdateService
from narracao_engine import normalize_channel

router = APIRouter(tags=["message"])

_MODE_BY_CHANNEL = {
    "narracao": "narrador",
    "mestre": "mestre",
    "sistema": "gestor",
    "gestor": "gestor",
}


def _process_message(channel: str, body: MessageRequest) -> MessageResponse:
    message = body.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail={"error": "Campo 'message' e obrigatorio"})

    channel = normalize_channel(channel)
    mode = _MODE_BY_CHANNEL.get(channel, "narrador")
    settings = get_settings()
    raw_reply = generate_reply(message, mode, channel=channel)
    if settings.update_proposals_enabled and channel == "gestor":
        update_service = UpdateService(settings)
        reply, proposals, _report = update_service.ingest_narrative(raw_reply)
    else:
        reply, proposals = raw_reply, []
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


@router.post("/api/mestre", response_model=MessageResponse)
def post_mestre(body: MessageRequest) -> MessageResponse:
    return _process_message("mestre", body)


@router.post("/api/narrador", response_model=MessageResponse)
def post_narrador(body: MessageRequest) -> MessageResponse:
    """Alias legado — redireciona para o canal Mestre off-game."""
    return _process_message("mestre", body)


@router.post("/api/sistema", response_model=MessageResponse)
def post_sistema(body: MessageRequest) -> MessageResponse:
    return _process_message("sistema", body)


@router.post("/api/message", response_model=MessageResponse)
def post_message(body: MessageRequest) -> MessageResponse:
    channel = normalize_channel(body.mode or "narracao")
    return _process_message(channel, body)