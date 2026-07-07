from __future__ import annotations

import sqlite3
from pathlib import Path

from motor.settings import Settings, get_settings

MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"


def get_connection(settings: Settings | None = None) -> sqlite3.Connection:
    cfg = settings or get_settings()
    cfg.db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(cfg.db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


def run_migrations(conn: sqlite3.Connection | None = None, settings: Settings | None = None) -> int:
    cfg = settings or get_settings()
    own_conn = conn is None
    connection = conn or get_connection(cfg)
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version INTEGER PRIMARY KEY,
                applied_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        applied = {
            int(row[0])
            for row in connection.execute("SELECT version FROM schema_migrations").fetchall()
        }
        migrations = sorted(MIGRATIONS_DIR.glob("*.sql"))
        count = 0
        for migration in migrations:
            version = int(migration.stem.split("_", 1)[0])
            if version in applied:
                continue
            sql = migration.read_text(encoding="utf-8")
            connection.executescript(sql)
            connection.execute(
                "INSERT INTO schema_migrations (version) VALUES (?)",
                (version,),
            )
            count += 1
        connection.commit()
        return count
    finally:
        if own_conn:
            connection.close()


def init_database(settings: Settings | None = None) -> sqlite3.Connection:
    conn = get_connection(settings)
    run_migrations(conn, settings)
    return conn