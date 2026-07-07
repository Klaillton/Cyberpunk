from __future__ import annotations

from dataclasses import dataclass

from motor.index.faiss_index import FaissHit, FaissIndex
from motor.markdown.sync_engine import SyncEngine
from motor.settings import Settings, get_settings


@dataclass(frozen=True)
class SearchResult:
    hits: list[FaissHit]
    index_size: int


class SearchService:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def ensure_index(self) -> int:
        index = FaissIndex(self.settings)
        chunk_count = int(index.conn.execute("SELECT COUNT(*) FROM document_chunks").fetchone()[0])
        if chunk_count == 0 or not index.index_path.exists():
            SyncEngine(self.settings).full_sync()
            return FaissIndex(self.settings).rebuild()
        if not index.index_path.exists():
            return index.rebuild()
        return chunk_count

    def search(
        self,
        query: str,
        top_k: int = 8,
        doc_types: list[str] | None = None,
    ) -> SearchResult:
        clean_query = query.strip()
        if not clean_query:
            return SearchResult(hits=[], index_size=0)

        index = FaissIndex(self.settings)
        if not index.index_path.exists():
            self.ensure_index()
            index = FaissIndex(self.settings)

        hits = index.search(clean_query, top_k=top_k, doc_types=doc_types)
        size = index._index.ntotal if index._index is not None else 0
        return SearchResult(hits=hits, index_size=size)