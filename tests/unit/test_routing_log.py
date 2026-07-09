from __future__ import annotations

from motor.llm.types import RoutingDecision
from motor.routing_log import RoutingLogEntry, RoutingLogStore
from motor.storage.database import init_database


def test_routing_log_persists_decision(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "motor.db"
    monkeypatch.setenv("DB_PATH", str(db_path))
    monkeypatch.setenv("DATA_DIR", str(tmp_path))

    from motor.settings import reset_settings

    reset_settings()
    conn = init_database()
    store = RoutingLogStore(conn)
    decision = RoutingDecision(
        provider="ollama",
        model="llama3.1:8b",
        tier="standard",
        score=3,
        reasons=["heuristic:test"],
        policy="local_only",
        escalated=False,
        requires_user_approval=False,
    )
    row_id = store.append(
        RoutingLogEntry(
            channel="narracao",
            mode="narrador",
            message_preview="Observo o pack",
            decision=decision,
            attempt=1,
            quality_passed=True,
        )
    )
    assert row_id > 0
    row = conn.execute(
        "SELECT provider, tier, quality_passed FROM provider_routing_log WHERE id = ?",
        (row_id,),
    ).fetchone()
    assert row["provider"] == "ollama"
    assert row["tier"] == "standard"
    assert row["quality_passed"] == 1