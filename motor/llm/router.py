from __future__ import annotations

from motor.entities.entity_resolver import ResolvedEntities
from motor.llm.classifier import ComplexityClassifier
from motor.llm.scorer import SceneComplexityScorer
from motor.llm.types import ContextManifest, RoutingDecision, TurnRequest
from motor.settings import Settings, get_settings

LOCAL_PROVIDERS = frozenset({"none", "ollama"})
CLOUD_PROVIDERS = frozenset({"grok", "chatgpt", "gemini", "copilot", "openai"})


class ProviderRouter:
    def __init__(
        self,
        settings: Settings | None = None,
        scorer: SceneComplexityScorer | None = None,
        classifier: ComplexityClassifier | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.scorer = scorer or SceneComplexityScorer()
        self.classifier = classifier or ComplexityClassifier()

    def resolve(
        self,
        request: TurnRequest,
        entities: ResolvedEntities,
        manifest: ContextManifest,
        *,
        user_approved_cloud: bool = False,
    ) -> RoutingDecision:
        policy = self.settings.llm_routing_policy
        reasons: list[str] = []

        override = (request.provider_override or "").strip().lower()
        if override == "force_local":
            return self._local_decision(policy, reasons + ["override:force_local"], tier="standard", score=0)
        if override == "force_cloud":
            return self._cloud_decision(
                policy,
                reasons + ["override:force_cloud"],
                tier="complex",
                score=8,
                escalated=True,
            )

        if policy == "local_only":
            score, score_reasons = self.scorer.score(request, entities, manifest)
            tier, class_reasons = self.classifier.classify(request, manifest, score)
            return self._local_decision(
                policy,
                reasons + score_reasons + class_reasons,
                tier=tier,
                score=score,
            )

        if policy == "cloud_preferred":
            if self.settings.cloud_fallback_enabled:
                return self._cloud_decision(policy, reasons + ["policy:cloud_preferred"], tier="standard", score=4)
            return self._local_decision(policy, reasons + ["policy:cloud_unavailable"], tier="standard", score=4)

        score, score_reasons = self.scorer.score(request, entities, manifest)
        tier, class_reasons = self.classifier.classify(request, manifest, score)
        reasons.extend(score_reasons)
        reasons.extend(class_reasons)

        if tier in {"trivial", "standard"}:
            return self._local_decision(policy, reasons, tier=tier, score=score)

        if tier == "complex":
            if policy == "hybrid" and self.settings.cloud_fallback_enabled:
                return self._cloud_decision(
                    policy,
                    reasons + ["policy:hybrid_escalation"],
                    tier=tier,
                    score=score,
                    escalated=True,
                )
            return self._local_decision(policy, reasons + ["policy:complex_local"], tier=tier, score=score)

        # critical
        if policy == "hybrid" and self.settings.cloud_fallback_enabled and user_approved_cloud:
            return self._cloud_decision(
                policy,
                reasons + ["policy:critical_approved"],
                tier=tier,
                score=score,
                escalated=True,
            )

        decision = self._local_decision(policy, reasons + ["policy:critical_local_fallback"], tier=tier, score=score)
        return RoutingDecision(
            provider=decision.provider,
            model=decision.model,
            tier=decision.tier,
            score=decision.score,
            reasons=decision.reasons,
            policy=decision.policy,
            escalated=decision.escalated,
            requires_user_approval=True,
        )

    def resolve_fallback(
        self,
        original: RoutingDecision,
        quality_passed: bool,
    ) -> RoutingDecision | None:
        if quality_passed:
            return None
        if not self.settings.cloud_fallback_enabled:
            return None
        if original.escalated or original.provider in CLOUD_PROVIDERS:
            return None
        if self.settings.llm_routing_policy not in {"hybrid", "local_preferred", "cloud_preferred"}:
            return None
        return self._cloud_decision(
            original.policy,
            original.reasons + ["quality_gate:retry_cloud"],
            tier=original.tier,
            score=original.score,
            escalated=True,
        )

    def _local_decision(
        self,
        policy: str,
        reasons: list[str],
        *,
        tier: str,
        score: int,
    ) -> RoutingDecision:
        provider = self.settings.provider if self.settings.provider in LOCAL_PROVIDERS else "ollama"
        if provider == "none" and self.settings.llm_routing_policy != "local_only":
            provider = "ollama"
        model = self.settings.ollama_model_narration if provider == "ollama" else None
        return RoutingDecision(
            provider=provider,
            model=model,
            tier=tier,  # type: ignore[arg-type]
            score=score,
            reasons=reasons,
            policy=policy,
            escalated=False,
            requires_user_approval=False,
        )

    def _cloud_decision(
        self,
        policy: str,
        reasons: list[str],
        *,
        tier: str,
        score: int,
        escalated: bool = False,
    ) -> RoutingDecision:
        provider = self.settings.cloud_provider
        return RoutingDecision(
            provider=provider,
            model=None,
            tier=tier,  # type: ignore[arg-type]
            score=score,
            reasons=reasons,
            policy=policy,
            escalated=escalated,
            requires_user_approval=False,
        )