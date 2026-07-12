from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse

from motor.character import build_character_profile
from motor.character_creation.resolver import resolve_image_path, resolve_sheet_path
from motor.npc import image_content_type
from motor.settings import get_settings

router = APIRouter(tags=["character"])


@router.get("/api/character-profile")
def character_profile(character_id: str | None = Query(default=None)) -> dict:
    return build_character_profile(character_id)


@router.get("/api/characters/{character_id}/profile")
def character_profile_by_id(character_id: str) -> dict:
    settings = get_settings()
    if resolve_sheet_path(character_id, settings) is None:
        raise HTTPException(status_code=404, detail="Ficha nao encontrada.")
    return build_character_profile(character_id)


@router.get("/api/character-image/{char_id}")
def character_image(char_id: str, variant: str = Query(default="full")) -> FileResponse:
    settings = get_settings()
    resolved_variant = variant.strip().lower()
    path = resolve_image_path(char_id, settings) or settings.character_image
    if resolved_variant == "token":
        from motor.npc import find_image_with_base

        base = path.stem
        token_path = find_image_with_base(base, token=True, settings=settings)
        if token_path is not None:
            path = token_path
    if not path.exists():
        raise HTTPException(status_code=404, detail="Imagem do personagem nao encontrada")
    return FileResponse(path, media_type=image_content_type(path))


@router.get("/cyberblade.png")
@router.get("/frontend/cyberblade.png")
@router.get("/cyberblade.jpg")
def legacy_character_image() -> FileResponse:
    settings = get_settings()
    if not settings.character_image.exists():
        raise HTTPException(status_code=404, detail="Imagem nao encontrada")
    path = settings.character_image
    return FileResponse(path, media_type=image_content_type(path))