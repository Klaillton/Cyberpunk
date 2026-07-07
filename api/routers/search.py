from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas import SearchHit, SearchRequest, SearchResponse
from motor.search_service import SearchService

router = APIRouter(tags=["search"])


@router.post("/api/search", response_model=SearchResponse)
def search_documents(body: SearchRequest) -> SearchResponse:
    query = body.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail={"error": "Campo 'query' e obrigatorio"})

    top_k = max(1, min(body.top_k, 50))
    doc_types = None
    if body.filters and body.filters.doc_type:
        doc_types = [value.strip().lower() for value in body.filters.doc_type if value.strip()]

    service = SearchService()
    result = service.search(query, top_k=top_k, doc_types=doc_types)
    return SearchResponse(
        hits=[
            SearchHit(
                source_path=hit.source_path,
                section=hit.section,
                score=round(hit.score, 4),
                preview=hit.preview,
                doc_type=hit.doc_type,
                entity_id=hit.entity_id,
            )
            for hit in result.hits
        ],
        index_size=result.index_size,
    )