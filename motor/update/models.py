from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal
from uuid import uuid4

ChangeType = Literal["append", "replace", "upsert_field", "insert_row"]
ProposalStatus = Literal["pending", "approved", "rejected", "applied"]


@dataclass
class UpdateProposal:
    target_path: str
    change_type: str
    payload: dict[str, Any]
    rationale: str = ""
    confidence: float = 0.0
    target_section: str | None = None
    id: str = field(default_factory=lambda: f"prop_{uuid4().hex[:12]}")
    source_turn_id: str = ""
    status: str = "pending"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "target_path": self.target_path,
            "target_section": self.target_section,
            "change_type": self.change_type,
            "payload": self.payload,
            "rationale": self.rationale,
            "confidence": self.confidence,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UpdateProposal:
        return cls(
            id=str(data.get("id") or f"prop_{uuid4().hex[:12]}"),
            target_path=str(data["target_path"]),
            target_section=data.get("target_section"),
            change_type=str(data["change_type"]),
            payload=dict(data.get("payload") or {}),
            rationale=str(data.get("rationale") or ""),
            confidence=float(data.get("confidence") or 0.0),
            source_turn_id=str(data.get("source_turn_id") or ""),
            status=str(data.get("status") or "pending"),
        )


@dataclass(frozen=True)
class ValidationIssue:
    proposal_id: str
    code: str
    message: str
    severity: str = "error"


@dataclass
class ValidationReport:
    valid: bool
    issues: list[ValidationIssue] = field(default_factory=list)
    accepted: list[UpdateProposal] = field(default_factory=list)


@dataclass(frozen=True)
class ApplyReport:
    applied: int
    files_changed: list[str]
    sync_report: dict[str, int]
    errors: list[str] = field(default_factory=list)