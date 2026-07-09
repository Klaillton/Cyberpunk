from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from motor.markdown.campaign_paths import is_campaign_content_path
from motor.settings import Settings, get_settings

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".gif")


def normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def list_campaign_sheets(settings: Settings | None = None) -> list[dict[str, str]]:
    """Lista fichas de campanha em fichas/ (exclui templates)."""
    cfg = settings or get_settings()
    fichas_dir = cfg.campanha_root / "fichas"
    results: list[dict[str, str]] = []
    if not fichas_dir.exists():
        return results

    for path in sorted(fichas_dir.rglob("*.md")):
        rel = path.relative_to(cfg.campanha_root).as_posix()
        if not is_campaign_content_path(rel):
            continue
        stem = path.stem
        if " - " in stem:
            role, slug = stem.split(" - ", 1)
        elif path.parent.name == "npc":
            role, slug = "npc", stem
        elif path.parent.name == "notas_narrador":
            role, slug = "notas_narrador", stem
        else:
            role, slug = "ficha", stem
        results.append(
            {
                "rel": rel,
                "role": role.strip(),
                "slug": slug.strip(),
            }
        )
    return results


def find_sheet_by_name(name: str, settings: Settings | None = None) -> Path | None:
    cfg = settings or get_settings()
    normalized = normalize_name(name)
    fichas_dir = cfg.campanha_root / "fichas"
    if not fichas_dir.exists():
        return None

    matches: list[Path] = []
    for path in fichas_dir.rglob("*.md"):
        rel = path.relative_to(cfg.campanha_root).as_posix()
        if not is_campaign_content_path(rel):
            continue
        stem = normalize_name(path.stem)
        if not stem:
            continue
        if normalized in stem or stem in normalized:
            matches.append(path)

    if not matches:
        return None
    return min(matches, key=lambda p: abs(len(normalize_name(p.stem)) - len(normalized)))


def find_image_with_base(base_name: str, *, token: bool, settings: Settings | None = None) -> Path | None:
    cfg = settings or get_settings()
    if not cfg.images_dir.exists():
        return None

    suffix = "_token" if token else ""
    for ext in IMAGE_EXTENSIONS:
        candidate = cfg.images_dir / f"{base_name}{suffix}{ext}"
        if candidate.exists():
            return candidate
    return None


def fallback_generic_image(gender: str, settings: Settings | None = None) -> Path | None:
    cfg = settings or get_settings()
    generic_female = cfg.images_dir / "NPC_generic_female.png"
    generic_male = cfg.images_dir / "NPC_generic_male.png"
    if gender == "female" and generic_female.exists():
        return generic_female
    if generic_male.exists():
        return generic_male
    if generic_female.exists():
        return generic_female
    return None


def scan_image_matches(normalized_name: str, settings: Settings | None = None) -> tuple[Path | None, Path | None]:
    cfg = settings or get_settings()
    image_path: Path | None = None
    token_path: Path | None = None
    if not cfg.images_dir.exists() or not normalized_name:
        return image_path, token_path

    for candidate in cfg.images_dir.glob("*"):
        if not candidate.is_file() or candidate.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        candidate_norm = normalize_name(candidate.stem)
        if normalized_name not in candidate_norm and candidate_norm not in normalized_name:
            continue
        if "_token" in candidate.stem.lower() and token_path is None:
            token_path = candidate
        elif image_path is None:
            image_path = candidate
    return image_path, token_path


def resolve_npc_assets(name: str, gender: str, settings: Settings | None = None) -> dict:
    cfg = settings or get_settings()
    sheet = find_sheet_by_name(name, cfg)
    source = "fallback"
    normalized = normalize_name(name)
    image_path: Path | None = None
    token_path: Path | None = None

    if sheet is not None:
        base = sheet.stem
        image_path = find_image_with_base(base, token=False, settings=cfg)
        token_path = find_image_with_base(base, token=True, settings=cfg)
        source = "sheet-name"
    if image_path is None:
        scanned_image, scanned_token = scan_image_matches(normalized, cfg)
        image_path = scanned_image or image_path
        token_path = token_path or scanned_token
        source = "image-scan" if image_path is not None else source

    if image_path is None:
        image_path = fallback_generic_image(gender, cfg)
        source = "generic"

    resolved_image = image_path
    resolved_token = token_path or image_path
    return {
        "name": name,
        "gender": gender,
        "source": source,
        "hasImage": resolved_image is not None,
        "hasToken": resolved_token is not None,
        "imagePath": resolved_image,
        "tokenPath": resolved_token,
        "hasSheet": sheet is not None,
        "sheetPath": str(sheet.relative_to(cfg.repo_root)).replace("\\", "/") if sheet else "",
    }


def build_npc_asset_response(name: str, gender: str, settings: Settings | None = None) -> dict:
    assets = resolve_npc_assets(name, gender, settings)
    image_url = f"/api/npc-image?name={quote(name)}&variant=full&gender={quote(gender)}"
    token_url = f"/api/npc-image?name={quote(name)}&variant=token&gender={quote(gender)}"
    return {
        "name": assets["name"],
        "gender": assets["gender"],
        "source": assets["source"],
        "hasSheet": assets["hasSheet"],
        "sheetPath": assets["sheetPath"],
        "hasImage": assets["hasImage"],
        "hasToken": assets["hasToken"],
        "imageUrl": image_url,
        "tokenUrl": token_url,
    }


def resolve_npc_image_path(name: str, gender: str, variant: str, settings: Settings | None = None) -> Path | None:
    assets = resolve_npc_assets(name, gender, settings)
    path = assets["tokenPath"] if variant == "token" else assets["imagePath"]
    if path is None or not path.exists():
        return None
    return path


def image_content_type(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if ext == ".webp":
        return "image/webp"
    if ext == ".gif":
        return "image/gif"
    return "image/png"