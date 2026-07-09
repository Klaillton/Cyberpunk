from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas import MessageRequest, MessageResponse
from api.schemas import QualityCheckResponse, RoutingDecisionResponse
from motor.narration import generate_turn
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
    history = (
        [{"role": entry.role, "content": entry.content} for entry in body.history]
        if body.history
        else None
    )
    turn = generate_turn(message, mode, settings=settings, channel=channel, history=history)
    raw_reply = turn.reply
    if settings.update_proposals_enabled and channel in {"gestor", "sistema"}:
        update_service = UpdateService(settings)
        reply, proposals, _report = update_service.ingest_narrative(raw_reply)
    else:
        reply, proposals = raw_reply, []

    provider_used = turn.provider_used or settings.provider
    model_used = turn.model_used
    if model_used is None and provider_used == "ollama":
        model_used = settings.ollama_model_narration

    routing_payload = None
    if turn.routing_decision is not None:
        decision = turn.routing_decision
        routing_payload = RoutingDecisionResponse(
            provider=decision.provider,
            model=decision.model,
            tier=decision.tier,
            score=decision.score,
            policy=decision.policy,
            escalated=decision.escalated,
            reasons=decision.reasons,
        )

    quality_checks = None
    quality_passed = None
    if turn.quality_report is not None:
        quality_passed = turn.quality_report.passed
        quality_checks = [
            QualityCheckResponse(name=check.name, passed=check.passed, detail=check.detail)
            for check in turn.quality_report.checks
        ]

    return MessageResponse(
        channel=channel,
        provider=provider_used,
        reply=reply,
        model=model_used,
        update_proposals=[proposal.to_dict() for proposal in proposals],
        routing_decision=routing_payload,
        quality_passed=quality_passed,
        quality_checks=quality_checks,
        turn_attempts=turn.attempts,
        context_sources=turn.context_sources or None,
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