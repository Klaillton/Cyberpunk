from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path

import faiss
import numpy as np

from motor.index.embedder import Embedder, TfidfEmbedder, create_embedder
from motor.settings import Settings, get_settings
from motor.storage.database import init_database


@dataclass(frozen=True)
class FaissHit:
    chunk_id: str
    source_path: str
    section: str | None
    score: float
    preview: str
    doc_type: str
    entity_id: str | None


class FaissIndex:
    def __init__(self, settings: Settings | None = None, embedder: Embedder | None = None) -> None:
        self.settings = settings or get_settings()
        self.embedder = embedder or create_embedder()
        self.conn = init_database(self.settings)
        self.index_path = self.settings.faiss_dir / "index.faiss"
        self.metadata_path = self.settings.faiss_dir / "metadata.jsonl"
        self._index: faiss.Index | None = None
        self._metadata: list[dict[str, object]] = []

    def rebuild(self) -> int:
        rows = self.conn.execute(
            """
            SELECT
                c.id AS chunk_id,
                c.section,
                c.text,
                d.path AS source_path,
                d.doc_type,
                d.entity_id
            FROM document_chunks c
            JOIN documents d ON d.id = c.document_id
            ORDER BY c.id
            """
        ).fetchall()

        if not rows:
            self._reset_index_files()
            return 0

        texts = [str(row["text"]) for row in rows]
        if isinstance(self.embedder, TfidfEmbedder):
            self.embedder.fit(texts)
        vectors = self.embedder.embed(texts)
        if vectors.size == 0:
            self._reset_index_files()
            return 0

        dimension = vectors.shape[1]
        index = faiss.IndexFlatIP(dimension)
        index.add(vectors.astype(np.float32))

        self.settings.faiss_dir.mkdir(parents=True, exist_ok=True)
        faiss.write_index(index, str(self.index_path))

        metadata: list[dict[str, object]] = []
        self.conn.execute("DELETE FROM faiss_vectors")
        for vector_id, row in enumerate(rows):
            chunk_id = str(row["chunk_id"])
            metadata.append(
                {
                    "chunk_id": chunk_id,
                    "vector_id": vector_id,
                    "source_path": row["source_path"],
                    "section": row["section"],
                    "doc_type": row["doc_type"],
                    "entity_id": row["entity_id"],
                    "preview": str(row["text"])[:240],
                }
            )
            self.conn.execute(
                """
                UPDATE document_chunks SET faiss_vector_id = ? WHERE id = ?
                """,
                (vector_id, chunk_id),
            )
            self.conn.execute(
                "INSERT INTO faiss_vectors (vector_id, chunk_id) VALUES (?, ?)",
                (vector_id, chunk_id),
            )
        self.conn.commit()

        with self.metadata_path.open("w", encoding="utf-8") as handle:
            for item in metadata:
                handle.write(json.dumps(item, ensure_ascii=False) + "\n")

        self._index = index
        self._metadata = metadata
        return len(metadata)

    def search(
        self,
        query: str,
        top_k: int = 8,
        doc_types: list[str] | None = None,
    ) -> list[FaissHit]:
        self._ensure_loaded()
        if self._index is None or self._index.ntotal == 0:
            return []

        if isinstance(self.embedder, TfidfEmbedder) and self.embedder.dimension == 0:
            return []

        query_vec = self.embedder.embed([query]).astype(np.float32)
        if query_vec.size == 0:
            return []

        scores, indices = self._index.search(query_vec, min(top_k * 3, self._index.ntotal))
        hits: list[FaissHit] = []
        allowed = {value.lower() for value in doc_types} if doc_types else None

        for score, vector_id in zip(scores[0], indices[0]):
            if vector_id < 0:
                continue
            meta = self._metadata[int(vector_id)]
            doc_type = str(meta.get("doc_type", ""))
            if allowed and doc_type.lower() not in allowed:
                continue
            hits.append(
                FaissHit(
                    chunk_id=str(meta["chunk_id"]),
                    source_path=str(meta["source_path"]),
                    section=str(meta["section"]) if meta.get("section") else None,
                    score=float(score),
                    preview=str(meta.get("preview", "")),
                    doc_type=doc_type,
                    entity_id=str(meta["entity_id"]) if meta.get("entity_id") else None,
                )
            )
            if len(hits) >= top_k:
                break
        return hits

    def _ensure_loaded(self) -> None:
        if self._index is not None:
            return
        if not self.index_path.exists() or not self.metadata_path.exists():
            return

        self._index = faiss.read_index(str(self.index_path))
        self._metadata = []
        with self.metadata_path.open(encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    self._metadata.append(json.loads(line))

        if isinstance(self.embedder, TfidfEmbedder):
            rows = self.conn.execute("SELECT text FROM document_chunks ORDER BY id").fetchall()
            self.embedder.fit([str(row["text"]) for row in rows])

    def _reset_index_files(self) -> None:
        self._index = None
        self._metadata = []
        if self.index_path.exists():
            self.index_path.unlink()
        if self.metadata_path.exists():
            self.metadata_path.unlink()
        self.conn.execute("DELETE FROM faiss_vectors")
        self.conn.commit()