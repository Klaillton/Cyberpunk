from __future__ import annotations

from pathlib import Path

PATH_ALIASES: dict[str, str] = {
    "campanha/estado/heat.md": "heat.md",
    "estado/heat.md": "heat.md",
    "campanha/estado/board.md": "board/board_campanha.md",
    "campanha/estado/economia.md": "economia.md",
    "campanha/estado/reputacao.md": "reputacao.md",
    "campanha/relacionamentos/ryan_relacionamentos.md": "relacionamentos/ryan_relacionamentos.md",
}

ALLOWED_CHANGE_TYPES = frozenset({"append", "replace", "upsert_field", "insert_row"})
RELATIONSHIP_PATH_HINTS = ("relacionamento", "relationship")
HEAT_PATH_HINTS = ("heat.md", "estado/heat")


def normalize_target_path(target_path: str) -> str:
    clean = target_path.strip().replace("\\", "/")
    return PATH_ALIASES.get(clean, clean.removeprefix("campanha/"))


def resolve_target_file(target_path: str, campanha_root: Path) -> Path | None:
    rel = normalize_target_path(target_path)
    candidate = campanha_root / rel
    if candidate.exists():
        return candidate
    fallback = campanha_root.parent / rel if campanha_root.name != "campanha" else None
    if fallback and fallback.exists():
        return fallback
    return candidate if candidate.parent.exists() else None