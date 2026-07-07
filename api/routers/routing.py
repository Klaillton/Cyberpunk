from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas import RoutingPolicyResponse, RoutingPreviewRequest, RoutingPreviewResponse
from motor.routing_service import RoutingService
from motor.settings import get_settings

router = APIRouter(tags=["routing"])


@router.get("/api/routing/policy", response_model=RoutingPolicyResponse)
def get_routing_policy() -> RoutingPolicyResponse:
    settings = get_settings()
    return RoutingPolicyResponse(
        policy=settings.llm_routing_policy,
        default_provider=settings.provider,
        cloud_provider=settings.cloud_provider,
        cloud_fallback_enabled=settings.cloud_fallback_enabled,
    )


@router.post("/api/routing/preview", response_model=RoutingPreviewResponse)
def preview_routing(body: RoutingPreviewRequest) -> RoutingPreviewResponse:
    message = body.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail={"error": "Campo 'message' e obrigatorio"})

    channel = (body.channel or "narracao").strip().lower()
    if channel not in {"narracao", "narrador", "gestor"}:
        channel = "narracao"

    try:
        preview = RoutingService().preview(
            message,
            channel=channel,
            provider_override=body.provider_override,
            user_approved_cloud=bool(body.user_approved_cloud),
        )
    except RuntimeError as exc:
        if "obrigatorios ausentes" in str(exc).lower():
            raise HTTPException(status_code=409, detail={"error": str(exc)}) from exc
        raise HTTPException(status_code=500, detail={"error": str(exc)}) from exc

    decision = preview.decision
    return RoutingPreviewResponse(
        decision={
            "provider": decision.provider,
            "model": decision.model,
            "tier": decision.tier,
            "score": decision.score,
            "reasons": decision.reasons,
            "policy": decision.policy,
            "requires_user_approval": decision.requires_user_approval,
        },
        would_escalate_to_cloud=preview.would_escalate_to_cloud,
        entities={
            "npc_ids": preview.entities.npc_ids,
            "character_ids": preview.entities.character_ids,
            "keywords": preview.entities.keywords,
            "confidence": preview.entities.confidence,
        },
        context_chars=preview.manifest.total_chars,
    )