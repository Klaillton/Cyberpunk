from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Tier = Literal["trivial", "standard", "complex", "critical"]
RoutingPolicy = Literal["local_only", "local_preferred", "hybrid", "cloud_preferred"]


@dataclass(frozen=True)
class TurnRequest:
    message: str
    channel: str = "narracao"
    mode: str = "gestor"
    provider_override: str | None = None


@dataclass(frozen=True)
class ContextManifest:
    total_chars: int
    source_paths: list[str] = field(default_factory=list)
    entity_ids: list[str] = field(default_factory=list)
    board_excerpt: str = ""


@dataclass(frozen=True)
class RoutingDecision:
    provider: str
    model: str | None
    tier: Tier
    score: int
    reasons: list[str]
    policy: str
    escalated: bool
    requires_user_approval: bool


@dataclass(frozen=True)
class QualityCheck:
    name: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class QualityReport:
    passed: bool
    checks: list[QualityCheck]