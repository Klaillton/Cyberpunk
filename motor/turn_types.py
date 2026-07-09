from __future__ import annotations

from dataclasses import dataclass, field

from motor.llm.types import QualityReport, RoutingDecision


@dataclass(frozen=True)
class TurnResult:
    reply: str
    routing_decision: RoutingDecision | None = None
    quality_report: QualityReport | None = None
    attempts: int = 1
    provider_used: str | None = None
    model_used: str | None = None
    context_sources: list[str] = field(default_factory=list)