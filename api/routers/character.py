from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from motor.character import build_character_profile
from motor.npc import image_content_type
from motor.settings import get_settings

router = APIRouter(tags=["character"])


@router.get("/api/character-profile")
def character_profile() -> dict:
    return build_character_profile()


@router.get("/api/character-image/{char_id}")
def character_image(char_id: str) -> FileResponse:
    settings = get_settings()
    if char_id != settings.character_id or not settings.character_image.exists():
        raise HTTPException(status_code=404, detail="Imagem do personagem nao encontrada")
    path = settings.character_image
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