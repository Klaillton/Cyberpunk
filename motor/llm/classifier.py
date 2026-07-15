from __future__ import annotations

from motor.llm.scorer import score_to_tier
from motor.llm.types import ContextManifest, TurnRequest
from motor.npc_agency import is_npc_agency_turn


class ComplexityClassifier:
    """Classificador heurístico (Fase 4). phi3:mini opcional em fase posterior."""

    def classify(
        self,
        request: TurnRequest,
        manifest: ContextManifest,
        score: int,
    ) -> tuple[str, list[str]]:
        tier = score_to_tier(score)
        reasons = [f"classifier:{tier}"]
        if manifest.total_chars > 24_000:
            tier = "complex" if tier in {"trivial", "standard"} else tier
            reasons.append("classifier:heavy_context")
        if is_npc_agency_turn(request.message) and tier in {"complex", "critical"}:
            tier = "standard"
            reasons.append("classifier:agency_cap_standard")
        return tier, reasons