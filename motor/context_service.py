from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

import narracao_engine as engine

from motor.entities.entity_resolver import EntityResolver, ResolvedEntities
from motor.llm.types import ContextManifest
from motor.markdown.campaign_paths import is_campaign_content_path, is_template_path
from motor.search_service import SearchService
from motor.settings import Settings, get_settings


@dataclass(frozen=True)
class ContextSelection:
    paths: list[Path]
    entities: ResolvedEntities
    manifest: ContextManifest
    faiss_hits: int
    sources: list[str]


_SEMANTIC_CHANNELS = frozenset({"narracao", "gestor", "narrador"})


class ContextService:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.resolver = EntityResolver()
        self.search = SearchService(self.settings)

    def select(
        self,
        message: str,
        *,
        provider: str | None = None,
        channel: str = "narracao",
        session_intent: str | None = None,
        max_files: int | None = None,
    ) -> ContextSelection:
        channel = engine.normalize_channel(channel)
        entities = self.resolver.resolve(message)
        regex_paths = engine.select_context_files(
            message,
            max_files=max_files or 10,
            provider=provider,
            channel=channel,
            session_intent=session_intent,
        )

        merged_rel: list[str] = []
        sources: list[str] = []

        def add_paths(paths: list[Path], source: str) -> None:
            for path in paths:
                rel = self._relative_path(path)
                if not rel or rel in merged_rel:
                    continue
                if is_template_path(rel) and session_intent != "summary":
                    continue
                if not is_campaign_content_path(rel) and session_intent != "summary":
                    continue
                merged_rel.append(rel)
                sources.append(source)

        add_paths(regex_paths, "regex")

        entity_paths = self._paths_for_entities(entities)
        add_paths(entity_paths, "entity")

        faiss_hits = 0
        if self._use_semantic_search(channel, session_intent):
            faiss_paths, faiss_hits = self._paths_from_search(message)
            add_paths(faiss_paths, "faiss")

        effective_max = max_files or engine.DEFAULT_OLLAMA_MAX_CONTEXT_FILES
        if provider == "ollama":
            if session_intent == "summary":
                effective_max = 6
            elif channel in {"mestre", "sistema"}:
                effective_max = 6
            else:
                effective_max = engine.DEFAULT_OLLAMA_MAX_CONTEXT_FILES

        trimmed_rel = merged_rel[:effective_max]
        resolved = engine.resolve_paths(
            trimmed_rel,
            allow_summary_templates=session_intent == "summary",
        )
        if provider == "ollama":
            resolved = [
                path
                for path in resolved
                if path.relative_to(engine.REPO_ROOT).as_posix() not in engine.OLLAMA_SKIP_CONTEXT
                or (
                    channel == "sistema"
                    and path.relative_to(engine.REPO_ROOT).as_posix() in engine.SISTEMA_OLLAMA_KEEP
                )
            ]
            resolved = engine.prioritize_paths_for_ollama(resolved, channel=channel)[:effective_max]
        else:
            resolved = resolved[:effective_max]

        manifest = self._build_manifest(resolved, entities)
        return ContextSelection(
            paths=resolved,
            entities=entities,
            manifest=manifest,
            faiss_hits=faiss_hits,
            sources=sources[: len(trimmed_rel)],
        )

    def _use_semantic_search(self, channel: str, session_intent: str | None) -> bool:
        if session_intent == "summary":
            return False
        if channel not in _SEMANTIC_CHANNELS:
            return False
        return True

    def _paths_for_entities(self, entities: ResolvedEntities) -> list[Path]:
        root = self.settings.campanha_root
        entity_ids = [
            *entities.character_ids,
            *entities.npc_ids,
            *entities.faction_ids,
        ]
        if not entity_ids:
            return []

        conn = self.resolver.conn
        paths: list[Path] = []
        seen: set[str] = set()
        for entity_id in dict.fromkeys(entity_ids):
            rows = conn.execute(
                "SELECT path FROM documents WHERE entity_id = ? ORDER BY path",
                (entity_id,),
            ).fetchall()
            for row in rows:
                rel = str(row["path"]).replace("\\", "/")
                if rel in seen:
                    continue
                seen.add(rel)
                candidate = root / rel
                if candidate.exists():
                    paths.append(candidate)
        return paths

    def _paths_from_search(self, message: str) -> tuple[list[Path], int]:
        try:
            self.search.ensure_index()
            result = self.search.search(message.strip(), top_k=6)
        except Exception:
            return [], 0

        root = self.settings.campanha_root
        paths: list[Path] = []
        for hit in result.hits:
            if hit.score < 0.05:
                continue
            rel = hit.source_path.replace("\\", "/")
            candidate = root / rel
            if candidate.exists() and candidate.is_file():
                paths.append(candidate)
        return paths, len(result.hits)

    def _build_manifest(self, paths: list[Path], entities: ResolvedEntities) -> ContextManifest:
        total_chars = 0
        board_excerpt = ""
        source_paths: list[str] = []
        root = self.settings.repo_root

        for path in paths:
            rel = path.relative_to(root).as_posix()
            source_paths.append(rel)
            text = path.read_text(encoding="utf-8", errors="replace")
            total_chars += len(text)
            if "board_campanha" in rel:
                board_excerpt = text[:4000]

        entity_ids = list(
            dict.fromkeys(
                [*entities.npc_ids, *entities.character_ids, *entities.faction_ids, *entities.keywords]
            )
        )
        return ContextManifest(
            total_chars=total_chars,
            source_paths=source_paths,
            entity_ids=entity_ids,
            board_excerpt=board_excerpt,
        )

    def _relative_path(self, path: Path) -> str:
        root = self.settings.repo_root
        campanha = self.settings.campanha_root
        try:
            return path.relative_to(root).as_posix()
        except ValueError:
            try:
                return path.relative_to(campanha).as_posix()
            except ValueError:
                return ""