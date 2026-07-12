from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from motor.settings import get_settings


@lru_cache(maxsize=1)
def load_catalog() -> dict:
    root = get_settings().repo_root
    path = root / "data" / "cpr" / "catalog.json"
    if not path.exists():
        return {"roles": [], "basic_skills": [], "skill_categories": {}, "stats": []}
    return json.loads(path.read_text(encoding="utf-8"))


def list_roles() -> list[dict]:
    return list(load_catalog().get("roles", []))


def basic_skills() -> list[str]:
    return list(load_catalog().get("basic_skills", []))