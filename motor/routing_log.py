from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass

from motor.llm.types import QualityReport, RoutingDecision
from motor.storage.database import init_database


@dataclass(frozen=True)
class RoutingLogEntry:
    channel: str
    mode: str
    message_preview: str
    decision: RoutingDecision
    attempt: int
    quality_passed: bool | None = None
    quality_report: QualityReport | None = None


class RoutingLogStore:
    def __init__(self, conn: sqlite3.Connection | None = None) -> None:
        self.conn = conn or init_database()

    def append(self, entry: RoutingLogEntry) -> int:
        quality_checks = None
        if entry.quality_report is not None:
            quality_checks = json.dumps(
                [
                    {"name": check.name, "passed": check.passed, "detail": check.detail}
                    for check in entry.quality_report.checks
                ],
                ensure_ascii=False,
            )
        cursor = self.conn.execute(
            """
            INSERT INTO provider_routing_log (
                channel, mode, message_preview, provider, model, tier, score, policy,
                escalated, attempt, quality_passed, reasons_json, quality_checks_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry.channel,
                entry.mode,
                entry.message_preview[:240],
                entry.decision.provider,
                entry.decision.model,
                entry.decision.tier,
                entry.decision.score,
                entry.decision.policy,
                1 if entry.decision.escalated else 0,
                entry.attempt,
                None if entry.quality_passed is None else (1 if entry.quality_passed else 0),
                json.dumps(entry.decision.reasons, ensure_ascii=False),
                quality_checks,
            ),
        )
        self.conn.commit()
        return int(cursor.lastrowid or 0)