from __future__ import annotations

import json
import sqlite3

from motor.settings import Settings, get_settings
from motor.storage.database import init_database
from motor.update.models import UpdateProposal


class ProposalStore:
    def __init__(self, settings: Settings | None = None, conn: sqlite3.Connection | None = None) -> None:
        self.settings = settings or get_settings()
        self.conn = conn or init_database(self.settings)

    def save_many(self, proposals: list[UpdateProposal], *, session_id: str | None = None) -> list[UpdateProposal]:
        saved: list[UpdateProposal] = []
        for proposal in proposals:
            self.conn.execute(
                """
                INSERT INTO update_proposals (
                    id, session_id, target_path, target_section, change_type,
                    payload_json, rationale, confidence, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    target_path = excluded.target_path,
                    target_section = excluded.target_section,
                    change_type = excluded.change_type,
                    payload_json = excluded.payload_json,
                    rationale = excluded.rationale,
                    confidence = excluded.confidence,
                    status = excluded.status
                """,
                (
                    proposal.id,
                    session_id,
                    proposal.target_path,
                    proposal.target_section,
                    proposal.change_type,
                    json.dumps(proposal.payload, ensure_ascii=False),
                    proposal.rationale,
                    proposal.confidence,
                    proposal.status,
                ),
            )
            saved.append(proposal)
        self.conn.commit()
        return saved

    def list_by_status(self, status: str = "pending") -> list[UpdateProposal]:
        rows = self.conn.execute(
            """
            SELECT id, target_path, target_section, change_type, payload_json,
                   rationale, confidence, status
            FROM update_proposals
            WHERE status = ?
            ORDER BY created_at ASC
            """,
            (status,),
        ).fetchall()
        return [self._row_to_proposal(row) for row in rows]

    def get_by_ids(self, proposal_ids: list[str]) -> list[UpdateProposal]:
        if not proposal_ids:
            return []
        placeholders = ",".join("?" for _ in proposal_ids)
        rows = self.conn.execute(
            f"""
            SELECT id, target_path, target_section, change_type, payload_json,
                   rationale, confidence, status
            FROM update_proposals
            WHERE id IN ({placeholders})
            """,
            proposal_ids,
        ).fetchall()
        return [self._row_to_proposal(row) for row in rows]

    def mark_status(self, proposal_ids: list[str], status: str) -> int:
        if not proposal_ids:
            return 0
        placeholders = ",".join("?" for _ in proposal_ids)
        if status == "applied":
            cursor = self.conn.execute(
                f"""
                UPDATE update_proposals
                SET status = ?, applied_at = datetime('now')
                WHERE id IN ({placeholders})
                """,
                [status, *proposal_ids],
            )
        else:
            cursor = self.conn.execute(
                f"""
                UPDATE update_proposals
                SET status = ?
                WHERE id IN ({placeholders})
                """,
                [status, *proposal_ids],
            )
        self.conn.commit()
        return int(cursor.rowcount)

    def _row_to_proposal(self, row: sqlite3.Row) -> UpdateProposal:
        return UpdateProposal(
            id=str(row["id"]),
            target_path=str(row["target_path"]),
            target_section=row["target_section"],
            change_type=str(row["change_type"]),
            payload=json.loads(str(row["payload_json"])),
            rationale=str(row["rationale"] or ""),
            confidence=float(row["confidence"] or 0.0),
            status=str(row["status"]),
        )