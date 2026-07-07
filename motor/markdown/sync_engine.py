from __future__ import annotations

import hashlib
import sqlite3
import uuid
from dataclasses import dataclass
from pathlib import Path

from motor.markdown.campaign_paths import (
    discover_campaign_files,
    entity_id_from_path,
    extract_aliases,
    infer_doc_type,
)
from motor.markdown.chunker import TextChunk, chunk_document
from motor.markdown.parser import document_to_json, parse_markdown_document
from motor.settings import Settings, get_settings
from motor.storage.database import init_database


@dataclass(frozen=True)
class SyncReport:
    documents_synced: int
    chunks_written: int
    aliases_written: int
    files_removed: int


def _content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _chunk_id(document_id: str, chunk: TextChunk) -> str:
    return f"chk_{document_id}_{chunk.chunk_index}"


class SyncEngine:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.conn = init_database(self.settings)

    def full_sync(self) -> SyncReport:
        root = self.settings.campanha_root
        discovered = {path.relative_to(root).as_posix(): path for path in discover_campaign_files(root)}
        existing = {
            row["path"]: row["id"]
            for row in self.conn.execute("SELECT id, path FROM documents").fetchall()
        }

        removed = 0
        for path, doc_id in existing.items():
            if path not in discovered:
                self.conn.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
                removed += 1

        docs_synced = 0
        chunks_written = 0
        aliases_written = 0

        for rel_path, file_path in sorted(discovered.items()):
            report = self.sync_file(file_path, rel_path=rel_path)
            docs_synced += 1
            chunks_written += report.chunks_written
            aliases_written += report.aliases_written

        self.conn.commit()
        return SyncReport(
            documents_synced=docs_synced,
            chunks_written=chunks_written,
            aliases_written=aliases_written,
            files_removed=removed,
        )

    def sync_file(self, path: Path, rel_path: str | None = None) -> SyncReport:
        root = self.settings.campanha_root
        resolved = path.resolve()
        relative = rel_path or resolved.relative_to(root.resolve()).as_posix()
        raw = resolved.read_text(encoding="utf-8")
        content_hash = _content_hash(raw)

        row = self.conn.execute(
            "SELECT id, content_hash FROM documents WHERE path = ?",
            (relative,),
        ).fetchone()
        if row and row["content_hash"] == content_hash:
            return SyncReport(documents_synced=0, chunks_written=0, aliases_written=0, files_removed=0)

        doc = parse_markdown_document(resolved, raw)
        doc_type = infer_doc_type(relative)
        entity_id = entity_id_from_path(relative, doc.title, doc.frontmatter)
        document_id = (
            relative.replace("/", "_").replace(".", "_").replace(" ", "_").replace("-", "_").lower()
        )

        self.conn.execute(
            """
            INSERT INTO documents (id, path, doc_type, title, entity_id, content_hash, frontmatter_json, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
            ON CONFLICT(path) DO UPDATE SET
                doc_type = excluded.doc_type,
                title = excluded.title,
                entity_id = excluded.entity_id,
                content_hash = excluded.content_hash,
                frontmatter_json = excluded.frontmatter_json,
                updated_at = datetime('now')
            """,
            (
                document_id,
                relative,
                doc_type,
                doc.title,
                entity_id,
                content_hash,
                document_to_json(doc),
            ),
        )
        self.conn.execute("DELETE FROM document_chunks WHERE document_id = ?", (document_id,))

        chunks = chunk_document(doc)
        for chunk in chunks:
            chunk_id = _chunk_id(document_id, chunk)
            self.conn.execute(
                """
                INSERT INTO document_chunks (id, document_id, section, chunk_index, text, char_count)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    chunk_id,
                    document_id,
                    chunk.section,
                    chunk.chunk_index,
                    chunk.text,
                    len(chunk.text),
                ),
            )

        aliases_written = 0
        if entity_id:
            self.conn.execute(
                "DELETE FROM entity_aliases WHERE entity_id = ?",
                (entity_id,),
            )
            entity_type = "npc" if doc_type == "npc" else doc_type
            for alias in extract_aliases(doc.title, entity_id):
                normalized = alias.lower()
                self.conn.execute(
                    """
                    INSERT OR IGNORE INTO entity_aliases (entity_id, entity_type, alias, normalized)
                    VALUES (?, ?, ?, ?)
                    """,
                    (entity_id, entity_type, alias, normalized),
                )
                aliases_written += 1

        self.conn.commit()
        return SyncReport(
            documents_synced=1,
            chunks_written=len(chunks),
            aliases_written=aliases_written,
            files_removed=0,
        )

    def on_file_changed(self, path: Path) -> SyncReport:
        return self.sync_file(path)

    def list_chunks(self) -> list[sqlite3.Row]:
        return self.conn.execute(
            """
            SELECT
                c.id AS chunk_id,
                c.section,
                c.text,
                c.chunk_index,
                d.path AS source_path,
                d.doc_type,
                d.entity_id
            FROM document_chunks c
            JOIN documents d ON d.id = c.document_id
            ORDER BY d.path, c.chunk_index
            """
        ).fetchall()