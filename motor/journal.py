from __future__ import annotations

import json
import re
from pathlib import Path

from motor.settings import Settings, get_settings


def journal_file(character_id: str, settings: Settings | None = None) -> Path:
    cfg = settings or get_settings()
    safe = re.sub(r"[^a-zA-Z0-9_-]", "_", character_id).lower()
    return cfg.journal_dir / f"{safe}.json"


def journal_storage_display(character_id: str, settings: Settings | None = None) -> str:
    cfg = settings or get_settings()
    path = journal_file(character_id, cfg)
    try:
        return str(path.relative_to(cfg.repo_root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def load_journal_entries(character_id: str, settings: Settings | None = None) -> list[dict]:
    path = journal_file(character_id, settings)
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    if not isinstance(data, list):
        return []
    out: list[dict] = []
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            continue
        entry_id = str(item.get("id", "")).strip() or f"{character_id}-{idx}"
        text = str(item.get("text", "")).strip()
        timestamp = str(item.get("timestamp", "")).strip()
        if not text or not timestamp:
            continue
        out.append({"id": entry_id, "timestamp": timestamp, "text": text})
    return out


def save_journal_entries(character_id: str, entries: list[dict], settings: Settings | None = None) -> None:
    cfg = settings or get_settings()
    cfg.journal_dir.mkdir(parents=True, exist_ok=True)
    path = journal_file(character_id, cfg)
    path.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")


def add_journal_entry(character_id: str, text: str, timestamp: str, settings: Settings | None = None) -> list[dict]:
    entries = load_journal_entries(character_id, settings)
    entry_id = f"{character_id}-{len(entries) + 1}-{abs(hash(timestamp + text)) % 1000000}"
    entries.append({"id": entry_id, "timestamp": timestamp, "text": text})
    save_journal_entries(character_id, entries, settings)
    return entries


def delete_journal_entry(character_id: str, entry_id: str, settings: Settings | None = None) -> list[dict] | None:
    entries = load_journal_entries(character_id, settings)
    filtered = [entry for entry in entries if str(entry.get("id", "")) != entry_id]
    if len(filtered) == len(entries):
        return None
    save_journal_entries(character_id, filtered, settings)
    return filtered