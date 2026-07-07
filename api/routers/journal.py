from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response

from api.schemas import JournalEntryRequest, JournalResponse
from motor.journal import (
    add_journal_entry,
    delete_journal_entry,
    journal_storage_display,
    load_journal_entries,
)
from motor.settings import get_settings

router = APIRouter(tags=["journal"])


@router.get("/api/journal/{character_id}", response_model=JournalResponse)
def get_journal(character_id: str) -> JournalResponse:
    if not character_id.strip():
        raise HTTPException(status_code=400, detail={"error": "characterId inválido"})
    return JournalResponse(
        characterId=character_id,
        storage=journal_storage_display(character_id),
        entries=load_journal_entries(character_id),
    )


@router.post("/api/journal/{character_id}", response_model=JournalResponse, status_code=201)
def post_journal(character_id: str, body: JournalEntryRequest) -> JournalResponse:
    text = body.text.strip()
    timestamp = body.timestamp.strip()
    if not text:
        raise HTTPException(status_code=400, detail={"error": "Campo 'text' é obrigatório"})
    if not timestamp:
        raise HTTPException(status_code=400, detail={"error": "Campo 'timestamp' é obrigatório"})

    entries = add_journal_entry(character_id, text, timestamp)
    return JournalResponse(
        characterId=character_id,
        storage=journal_storage_display(character_id),
        entries=entries,
    )


@router.delete("/api/journal/{character_id}/{entry_id}", response_model=JournalResponse)
def remove_journal_entry(character_id: str, entry_id: str) -> JournalResponse:
    filtered = delete_journal_entry(character_id, entry_id)
    if filtered is None:
        raise HTTPException(status_code=404, detail={"error": "Entrada não encontrada"})
    return JournalResponse(
        characterId=character_id,
        storage=journal_storage_display(character_id),
        entries=filtered,
    )