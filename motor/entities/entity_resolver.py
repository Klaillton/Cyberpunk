from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass, field

from motor.storage.database import init_database


@dataclass(frozen=True)
class ResolvedEntities:
    character_ids: list[str] = field(default_factory=list)
    npc_ids: list[str] = field(default_factory=list)
    faction_ids: list[str] = field(default_factory=list)
    location_ids: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    confidence: float = 0.0


_CAPITALIZED_RE = re.compile(r"\b([A-Z][a-záàâãéêíóôõúç]{2,})\b")


class EntityResolver:
    def __init__(self, conn: sqlite3.Connection | None = None) -> None:
        self.conn = conn or init_database()

    def resolve(self, message: str) -> ResolvedEntities:
        lowered = message.lower()
        npc_ids: list[str] = []
        character_ids: list[str] = []
        faction_ids: list[str] = []
        keywords: list[str] = []
        confidence = 0.0

        alias_rows = self.conn.execute(
            "SELECT entity_id, entity_type, alias, normalized FROM entity_aliases ORDER BY LENGTH(alias) DESC"
        ).fetchall()

        matched_entities: set[str] = set()
        for row in alias_rows:
            alias = str(row["alias"])
            normalized = str(row["normalized"])
            pattern = rf"\b{re.escape(normalized)}\b"
            if not re.search(pattern, lowered, flags=re.IGNORECASE):
                continue
            entity_id = str(row["entity_id"])
            if entity_id in matched_entities:
                continue
            matched_entities.add(entity_id)
            keywords.append(alias)
            confidence = max(confidence, 0.9 if len(alias) <= 5 else 0.75)
            entity_type = str(row["entity_type"])
            if entity_type == "npc":
                npc_ids.append(entity_id)
            elif entity_type == "character":
                character_ids.append(entity_id)
            elif entity_type == "faction":
                faction_ids.append(entity_id)

        for token in _CAPITALIZED_RE.findall(message):
            token_lower = token.lower()
            if token_lower in {alias.lower() for alias in keywords}:
                continue
            row = self.conn.execute(
                """
                SELECT entity_id, entity_type
                FROM entity_aliases
                WHERE normalized = ?
                LIMIT 1
                """,
                (token_lower,),
            ).fetchone()
            if row:
                entity_id = str(row["entity_id"])
                if entity_id in matched_entities:
                    continue
                matched_entities.add(entity_id)
                keywords.append(token)
                confidence = max(confidence, 0.6)
                entity_type = str(row["entity_type"])
                if entity_type == "npc":
                    npc_ids.append(entity_id)
                elif entity_type == "character":
                    character_ids.append(entity_id)

        return ResolvedEntities(
            character_ids=character_ids,
            npc_ids=npc_ids,
            faction_ids=faction_ids,
            keywords=keywords,
            confidence=confidence,
        )