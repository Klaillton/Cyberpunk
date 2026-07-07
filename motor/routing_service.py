from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import narracao_engine as engine

from motor.entities.entity_resolver import EntityResolver, ResolvedEntities
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
        self.resolver = EntityResolver()
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

        request = TurnRequest(
            message=message.strip(),
            channel=channel,
            mode="narrador" if channel == "narrador" else "gestor",
            provider_override=provider_override,
        )
        entities = self.resolver.resolve(message)
        manifest = self._build_manifest(message, entities)
        decision = self.router.resolve(
            request,
            entities,
            manifest,
            user_approved_cloud=user_approved_cloud,
        )
        would_escalate = decision.escalated and decision.provider not in {"none", "ollama"}
        return RoutingPreview(
            decision=decision,
            would_escalate_to_cloud=would_escalate,
            entities=entities,
            manifest=manifest,
        )

    def _build_manifest(self, message: str, entities: ResolvedEntities) -> ContextManifest:
        paths = engine.select_context_files(message)
        root = self.settings.campanha_root
        total_chars = 0
        board_excerpt = ""
        entity_ids = list(
            dict.fromkeys(
                [*entities.npc_ids, *entities.character_ids, *entities.faction_ids, *entities.keywords]
            )
        )

        normalized_paths: list[str] = []
        for rel_path in paths:
            rel = str(rel_path).replace("\\", "/")
            normalized_paths.append(rel)
            file_path = root / rel
            if not file_path.exists():
                file_path = self.settings.repo_root / rel
            if not file_path.exists():
                continue
            text = file_path.read_text(encoding="utf-8", errors="replace")
            total_chars += len(text)
            if "board_campanha" in rel:
                board_excerpt = text[:4000]

        return ContextManifest(
            total_chars=total_chars,
            source_paths=normalized_paths,
            entity_ids=entity_ids,
            board_excerpt=board_excerpt,
        )