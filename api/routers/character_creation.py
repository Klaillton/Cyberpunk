from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas import (
    CharacterDraftRequest,
    CreateCharacterResponse,
    ValidationReportResponse,
)
from motor.character_creation.catalog import load_catalog
from motor.character_creation.persistence import create_protagonist
from motor.character_creation.renderer import render_character_markdown
from motor.character_creation.resolver import resolve_sheet_path
from motor.character_creation.sheet_parser import parse_character_sheet
from motor.character_creation.validator import validate_complete_package
from motor.settings import get_settings

router = APIRouter(tags=["character-creation"])


@router.get("/api/character-creation/catalog")
def character_creation_catalog() -> dict:
    return load_catalog()


@router.post("/api/character-creation/validate", response_model=ValidationReportResponse)
def validate_character_draft(body: CharacterDraftRequest) -> ValidationReportResponse:
    report = validate_complete_package(body.model_dump())
    return ValidationReportResponse(
        passed=report.passed,
        issues=[issue.__dict__ for issue in report.issues],
    )


@router.post("/api/character-creation/preview")
def preview_character_draft(body: CharacterDraftRequest) -> dict:
    markdown = render_character_markdown(body.model_dump())
    return {"markdown": markdown}


@router.post("/api/characters", response_model=CreateCharacterResponse)
def create_character(body: CharacterDraftRequest) -> CreateCharacterResponse:
    draft = body.model_dump()
    report = validate_complete_package(draft)
    if not report.passed:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Ficha invalida.",
                "issues": [issue.__dict__ for issue in report.issues],
            },
        )
    try:
        created = create_protagonist(draft)
    except FileExistsError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    settings = get_settings()
    settings.character_id = created.id
    return CreateCharacterResponse(
        id=created.id,
        sheet_path=created.sheet_path,
        journal_path=created.journal_path,
        relationships_path=created.relationships_path,
    )


@router.get("/api/characters/active")
def active_character() -> dict:
    settings = get_settings()
    return {"character_id": settings.character_id}


@router.put("/api/characters/{character_id}/protagonist")
def set_protagonist(character_id: str) -> dict:
    settings = get_settings()
    sheet = resolve_sheet_path(character_id, settings)
    if sheet is None:
        raise HTTPException(status_code=404, detail="Ficha nao encontrada.")
    settings.character_id = character_id.strip().lower()
    return {"character_id": settings.character_id, "sheet_path": sheet.as_posix()}


@router.get("/api/characters/{character_id}/sheet")
def character_sheet_data(character_id: str) -> dict:
    settings = get_settings()
    sheet = resolve_sheet_path(character_id, settings)
    if sheet is None or not sheet.exists():
        raise HTTPException(status_code=404, detail="Ficha nao encontrada.")
    return parse_character_sheet(sheet, settings=settings)