CREATE TABLE IF NOT EXISTS provider_routing_log (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at          TEXT NOT NULL DEFAULT (datetime('now')),
    channel             TEXT NOT NULL,
    mode                TEXT NOT NULL,
    message_preview     TEXT NOT NULL,
    provider            TEXT NOT NULL,
    model               TEXT,
    tier                TEXT,
    score               INTEGER,
    policy              TEXT,
    escalated           INTEGER NOT NULL DEFAULT 0,
    attempt             INTEGER NOT NULL DEFAULT 1,
    quality_passed      INTEGER,
    reasons_json        TEXT,
    quality_checks_json TEXT
);

CREATE INDEX IF NOT EXISTS idx_routing_log_created ON provider_routing_log(created_at);
CREATE INDEX IF NOT EXISTS idx_routing_log_channel ON provider_routing_log(channel);