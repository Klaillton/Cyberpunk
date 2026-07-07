PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS schema_migrations (
    version     INTEGER PRIMARY KEY,
    applied_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS documents (
    id               TEXT PRIMARY KEY,
    path             TEXT NOT NULL UNIQUE,
    doc_type         TEXT NOT NULL,
    title            TEXT,
    entity_id        TEXT,
    content_hash     TEXT NOT NULL,
    frontmatter_json TEXT,
    indexed_at       TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at       TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_documents_type ON documents(doc_type);
CREATE INDEX IF NOT EXISTS idx_documents_entity ON documents(entity_id);

CREATE TABLE IF NOT EXISTS document_chunks (
    id              TEXT PRIMARY KEY,
    document_id     TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    section         TEXT,
    chunk_index     INTEGER NOT NULL,
    text            TEXT NOT NULL,
    char_count      INTEGER NOT NULL,
    faiss_vector_id INTEGER
);

CREATE INDEX IF NOT EXISTS idx_chunks_document ON document_chunks(document_id);

CREATE TABLE IF NOT EXISTS entity_aliases (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id   TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    alias       TEXT NOT NULL,
    normalized  TEXT NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_alias_unique ON entity_aliases(entity_type, normalized);

CREATE TABLE IF NOT EXISTS faiss_vectors (
    vector_id INTEGER PRIMARY KEY,
    chunk_id  TEXT NOT NULL UNIQUE REFERENCES document_chunks(id) ON DELETE CASCADE
);