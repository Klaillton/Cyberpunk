from __future__ import annotations

from pydantic import BaseModel, Field


class ChatHistoryEntry(BaseModel):
    role: str
    content: str


class MessageRequest(BaseModel):
    message: str = ""
    mode: str | None = None
    history: list[ChatHistoryEntry] | None = None


class RoutingDecisionResponse(BaseModel):
    provider: str
    model: str | None = None
    tier: str | None = None
    score: int | None = None
    policy: str | None = None
    escalated: bool = False
    reasons: list[str] = []


class QualityCheckResponse(BaseModel):
    name: str
    passed: bool
    detail: str


class MessageResponse(BaseModel):
    channel: str
    provider: str
    reply: str
    model: str | None = None
    update_proposals: list[dict] = []
    routing_decision: RoutingDecisionResponse | None = None
    quality_passed: bool | None = None
    quality_checks: list[QualityCheckResponse] | None = None
    turn_attempts: int | None = None
    context_sources: list[str] | None = None


class JournalEntryRequest(BaseModel):
    text: str
    timestamp: str


class JournalResponse(BaseModel):
    characterId: str
    storage: str
    entries: list[dict]


class ErrorResponse(BaseModel):
    error: str


class MessageBody(BaseModel):
    message: str = Field(default="")


class SearchFilters(BaseModel):
    doc_type: list[str] | None = None


class SearchRequest(BaseModel):
    query: str
    top_k: int = 8
    filters: SearchFilters | None = None


class SearchHit(BaseModel):
    source_path: str
    section: str | None = None
    score: float
    preview: str
    doc_type: str | None = None
    entity_id: str | None = None


class SearchResponse(BaseModel):
    hits: list[SearchHit]
    index_size: int = 0


class RoutingPreviewRequest(BaseModel):
    message: str
    channel: str = "narracao"
    provider_override: str | None = None
    user_approved_cloud: bool = False


class RoutingPreviewResponse(BaseModel):
    decision: dict
    would_escalate_to_cloud: bool
    entities: dict
    context_chars: int = 0


class RoutingPolicyResponse(BaseModel):
    policy: str
    default_provider: str
    cloud_provider: str
    cloud_fallback_enabled: bool


class SaveRequest(BaseModel):
    proposal_ids: list[str]
    approved: bool = True


class SaveResponse(BaseModel):
    applied: int
    files_changed: list[str]
    sync_report: dict[str, int]
    errors: list[str] = []


class ProposalsListResponse(BaseModel):
    proposals: list[dict]


class IngestProposalsRequest(BaseModel):
    narrative: str


class IngestProposalsResponse(BaseModel):
    narrative: str
    proposals: list[dict]
    validation: dict


class BriefItem(BaseModel):
    id: str
    title: str
    teaser: str
    detail: str
    sources: list[str] = []


class BriefMeta(BaseModel):
    location: str = ""
    date: str = ""
    period: str = ""
    updatedAt: str = ""
    sources: list[str] = []


class BriefResponse(BaseModel):
    opening: str
    meta: BriefMeta
    briefs: list[BriefItem]


class NpcCatalogEntry(BaseModel):
    id: str
    name: str
    role: str = ""
    relation: str = ""
    summary: str = ""
    gender: str = "male"
    sheetPath: str = ""
    imageUrl: str = ""
    tokenUrl: str = ""
    hasImage: bool = False
    hasSheet: bool = False
    featured: bool = False


class NpcCatalogResponse(BaseModel):
    count: int
    npcs: list[NpcCatalogEntry]
    sources: list[str] = []