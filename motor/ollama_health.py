from __future__ import annotations

import json
import urllib.error
import urllib.request

from motor.settings import Settings, get_settings


def list_installed_models(settings: Settings | None = None) -> list[str]:
    cfg = settings or get_settings()
    url = f"{cfg.ollama_base_url.rstrip('/')}/api/tags"
    try:
        with urllib.request.urlopen(url, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError):
        return []
    models: list[str] = []
    for entry in payload.get("models", []):
        name = str(entry.get("name", "")).strip()
        if name:
            models.append(name)
    return models


def model_is_installed(model: str, settings: Settings | None = None) -> bool:
    target = model.strip().lower()
    if not target:
        return False
    installed = [name.lower() for name in list_installed_models(settings)]
    if target in installed:
        return True
    # Ollama pode registrar com tag :latest
    base = target.split(":", 1)[0]
    return any(name == base or name.startswith(f"{base}:") for name in installed)


def inspect_ollama(settings: Settings | None = None) -> dict:
    cfg = settings or get_settings()
    installed = list_installed_models(cfg)
    narration = cfg.ollama_model_narration
    aux = cfg.ollama_model_aux
    return {
        "reachable": bool(installed) or _ollama_reachable(cfg),
        "base_url": cfg.ollama_base_url,
        "configured_narration": narration,
        "configured_aux": aux,
        "narration_ready": model_is_installed(narration, cfg),
        "aux_ready": model_is_installed(aux, cfg),
        "installed_models": installed,
    }


def _ollama_reachable(cfg: Settings) -> bool:
    url = f"{cfg.ollama_base_url.rstrip('/')}/api/tags"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return response.status == 200
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
        return False