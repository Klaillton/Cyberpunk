from __future__ import annotations

from dataclasses import dataclass

import narracao_engine as engine

from motor.context_service import ContextService
from motor.entities.entity_resolver import ResolvedEntities
from motor.llm.channel_profiles import max_context_files_for_channel
from motor.llm.router import ProviderRouter
from motor.llm.types import ContextManifest, RoutingDecision, TurnRequest
from motor.settings import Settings, get_settings


@dataclass(frozen=True)
class RoutingPreview:
    decision: RoutingDecision
    would_escalate_to_cloud: bool
    entities: ResolvedEntities
    manifest: ContextManifest


class RoutingService:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.context = ContextService(self.settings)
        self.router = ProviderRouter(self.settings)

    def preview(
        self,
        message: str,
        channel: str = "narracao",
        *,
        provider_override: str | None = None,
        user_approved_cloud: bool = False,
    ) -> RoutingPreview:
        missing = engine.check_integrity()
        if missing:
            raise RuntimeError(f"Arquivos obrigatorios ausentes: {', '.join(missing)}")

        channel = engine.normalize_channel(channel)
        request = TurnRequest(
            message=message.strip(),
            channel=channel,
            mode="narrador" if channel in {"narracao", "narrador"} else "gestor",
            provider_override=provider_override,
        )
        selection = self.context.select(
            message,
            provider=self.settings.provider,
            channel=channel,
            max_files=max_context_files_for_channel(channel, self.settings),
        )
        decision = self.router.resolve(
            request,
            selection.entities,
            selection.manifest,
            user_approved_cloud=user_approved_cloud,
        )
        would_escalate = decision.escalated and decision.provider not in {"none", "ollama"}
        return RoutingPreview(
            decision=decision,
            would_escalate_to_cloud=would_escalate,
            entities=selection.entities,
            manifest=selection.manifest,
        )