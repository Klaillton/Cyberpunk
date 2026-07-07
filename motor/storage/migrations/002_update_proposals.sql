CREATE TABLE IF NOT EXISTS update_proposals (
    id              TEXT PRIMARY KEY,
    session_id      TEXT,
    turn_id         INTEGER,
    target_path     TEXT NOT NULL,
    target_section  TEXT,
    change_type     TEXT NOT NULL,
    payload_json    TEXT NOT NULL,
    rationale       TEXT,
    confidence      REAL NOT NULL DEFAULT 0.0,
    status          TEXT NOT NULL DEFAULT 'pending',
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    applied_at      TEXT
);

CREATE INDEX IF NOT EXISTS idx_proposals_status ON update_proposals(status);