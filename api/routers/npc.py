from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse

from motor.npc import build_npc_asset_response, image_content_type, resolve_npc_image_path

router = APIRouter(tags=["npc"])


@router.get("/api/npc-asset")
def npc_asset(
    name: str = Query(default=""),
    gender: str = Query(default="male"),
) -> dict:
    clean_name = name.strip()
    clean_gender = gender.strip().lower() or "male"
    if not clean_name:
        raise HTTPException(status_code=400, detail={"error": "Parâmetro 'name' é obrigatório"})
    resolved_gender = "female" if clean_gender == "female" else "male"
    return build_npc_asset_response(clean_name, resolved_gender)


@router.get("/api/npc-image")
def npc_image(
    name: str = Query(default=""),
    variant: str = Query(default="full"),
    gender: str = Query(default="male"),
) -> FileResponse:
    clean_name = name.strip()
    if not clean_name:
        raise HTTPException(status_code=400, detail="Parâmetro name é obrigatório")
    resolved_gender = "female" if gender.strip().lower() == "female" else "male"
    path = resolve_npc_image_path(clean_name, resolved_gender, variant.strip().lower())
    if path is None:
        raise HTTPException(status_code=404, detail="Imagem do NPC nao encontrada")
    return FileResponse(path, media_type=image_content_type(path))