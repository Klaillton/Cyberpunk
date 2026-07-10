from __future__ import annotations

import pytest

from motor.entities.entity_resolver import ResolvedEntities
from motor.llm.router import ProviderRouter
from motor.llm.types import ContextManifest, TurnRequest
from motor.settings import reset_settings


@pytest.fixture
def router() -> ProviderRouter:
    settings = reset_settings()
    settings.provider = "ollama"
    settings.llm_routing_policy = "local_preferred"
    settings.cloud_fallback_enabled = False
    return ProviderRouter(settings)


def test_provider_router_narracao_short_message_uses_narration_profile(
    router: ProviderRouter,
) -> None:
    request = TurnRequest(message="ok", channel="narracao")
    entities = ResolvedEntities()
    manifest = ContextManifest(total_chars=1200)

    decision = router.resolve(request, entities, manifest)

    assert decision.provider == "ollama"
    assert decision.tier == "standard"
    assert decision.model == router.settings.ollama_model_narration
    assert any("profile:narracao_tier=standard" in reason for reason in decision.reasons)
    assert decision.escalated is False
    assert decision.requires_user_approval is False


def test_provider_router_sistema_uses_aux_model_and_trivial_tier(router: ProviderRouter) -> None:
    request = TurnRequest(
        message="qual o caminho da ficha do ryan?",
        channel="sistema",
    )
    decision = router.resolve(request, ResolvedEntities(), ContextManifest(total_chars=1200))

    assert decision.provider == "ollama"
    assert decision.tier == "trivial"
    assert decision.model == router.settings.ollama_model_aux
    assert any("profile:aux_tier=trivial" in reason for reason in decision.reasons)


def test_provider_router_force_local_override(router: ProviderRouter) -> None:
    router.settings.llm_routing_policy = "hybrid"
    router.settings.cloud_fallback_enabled = True
    request = TurnRequest(
        message="Cena epica com combate",
        channel="narracao",
        provider_override="force_local",
    )
    decision = router.resolve(request, ResolvedEntities(), ContextManifest(total_chars=9000))
    assert decision.provider == "ollama"
    assert "override:force_local" in decision.reasons


def test_provider_router_hybrid_escalates_on_complex_scene() -> None:
    settings = reset_settings()
    settings.provider = "ollama"
    settings.llm_routing_policy = "hybrid"
    settings.cloud_fallback_enabled = True
    settings.cloud_provider = "grok"
    router = ProviderRouter(settings)

    request = TurnRequest(
        message="Ryan, Valk, Reyes e Lira preparam combate contra Raffen no acampamento",
        channel="narracao",
    )
    entities = ResolvedEntities(npc_ids=["reyes", "lira", "sasha", "elias_recruit"])
    manifest = ContextManifest(total_chars=5000)

    decision = router.resolve(request, entities, manifest)

    assert decision.tier in {"complex", "critical"}
    assert decision.provider == "grok"
    assert decision.escalated is True
    assert decision.escalated is True


def test_provider_router_local_only_never_escalates() -> None:
    settings = reset_settings()
    settings.provider = "ollama"
    settings.llm_routing_policy = "local_only"
    settings.cloud_fallback_enabled = True
    router = ProviderRouter(settings)

    request = TurnRequest(message="Combate epico", channel="narracao")
    entities = ResolvedEntities(npc_ids=["a", "b", "c", "d", "e"])
    manifest = ContextManifest(total_chars=25_000)
    decision = router.resolve(request, entities, manifest)

    assert decision.provider == "ollama"
    assert decision.escalated is False


def test_provider_router_critical_requires_approval_without_cloud_consent() -> None:
    settings = reset_settings()
    settings.provider = "ollama"
    settings.llm_routing_policy = "hybrid"
    settings.cloud_fallback_enabled = True
    router = ProviderRouter(settings)

    request = TurnRequest(message="Operacao critica", channel="gestor")
    entities = ResolvedEntities(npc_ids=["reyes", "lira", "sasha", "elias_recruit", "tomas_recruit"])
    manifest = ContextManifest(total_chars=25_000)
    decision = router.resolve(request, entities, manifest, user_approved_cloud=False)

    assert decision.tier == "critical"
    assert decision.requires_user_approval is True
    assert decision.provider == "ollama"