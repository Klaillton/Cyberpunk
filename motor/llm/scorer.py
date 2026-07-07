from __future__ import annotations

import re

from motor.entities.entity_resolver import ResolvedEntities
from motor.llm.types import ContextManifest, TurnRequest

_COMBAT_RE = re.compile(
    r"\b(combate|combatei|atir|dispar|iniciativa|dano|armadura|raffen|incursao|hack|quickdraw)\b",
    re.IGNORECASE,
)
_EMOTIONAL_RE = re.compile(
    r"\b(declaracao de amor|vulnerabil|romance|arco emocional|relacao profunda)\b",
    re.IGNORECASE,
)


class SceneComplexityScorer:
    def score(
        self,
        request: TurnRequest,
        entities: ResolvedEntities,
        manifest: ContextManifest,
    ) -> tuple[int, list[str]]:
        score = 0
        reasons: list[str] = []

        npc_count = len(entities.npc_ids) + len(entities.character_ids)
        if npc_count > 2:
            bonus = (npc_count - 2) * 2
            score += bonus
            reasons.append(f"heuristic:npc_count={npc_count}")

        if manifest.total_chars > 20_000:
            score += 3
            reasons.append(f"heuristic:context_chars={manifest.total_chars}")

        if request.channel == "gestor" or request.mode == "gestor":
            score += 2
            reasons.append("heuristic:gestor_structured_output")

        if _COMBAT_RE.search(request.message):
            score += 3
            reasons.append("heuristic:combat_keywords")

        if _EMOTIONAL_RE.search(request.message):
            score += 1
            reasons.append("heuristic:emotional_arc")

        if request.channel == "narrador":
            score -= 2
            reasons.append("heuristic:narrador_off_record")

        clean = request.message.strip()
        if len(clean) < 80 and npc_count <= 1:
            score -= 3
            reasons.append("heuristic:short_message")

        return score, reasons


def score_to_tier(score: int) -> str:
    if score <= 2:
        return "trivial"
    if score <= 6:
        return "standard"
    if score <= 10:
        return "complex"
    return "critical"