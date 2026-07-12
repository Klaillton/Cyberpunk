from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

from motor.settings import Settings, get_settings

_DEFAULT_RETRIES = 3
_DEFAULT_RETRY_DELAY_S = 1.5


def _fetch_tags_payload(cfg: Settings, *, timeout: float = 12.0) -> dict | None:
    url = f"{cfg.ollama_base_url.rstrip('/')}/api/tags"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError):
        return None


def list_installed_models(
    settings: Settings | None = None,
    *,
    retries: int = _DEFAULT_RETRIES,
    retry_delay_s: float = _DEFAULT_RETRY_DELAY_S,
) -> list[str]:
    cfg = settings or get_settings()
    attempts = max(1, retries)
    payload: dict | None = None
    for attempt in range(attempts):
        payload = _fetch_tags_payload(cfg)
        if payload is not None:
            break
        if attempt < attempts - 1:
            time.sleep(retry_delay_s)
    if payload is None:
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


def inspect_ollama(
    settings: Settings | None = None,
    *,
    retries: int = _DEFAULT_RETRIES,
) -> dict:
    cfg = settings or get_settings()
    installed = list_installed_models(cfg, retries=retries)
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


def warm_ollama_model(settings: Settings | None = None, *, timeout: float = 180.0) -> bool:
    """Carrega o modelo de narracao na memoria (evita timeout na primeira cena)."""
    cfg = settings or get_settings()
    model = cfg.ollama_model_narration
    body: dict = {
        "model": model,
        "prompt": "Responda apenas: pronto.",
        "stream": False,
        "keep_alive": cfg.ollama_keep_alive,
        "options": {
            "num_predict": 8,
            "num_ctx": min(cfg.ollama_num_ctx_narration, 2048),
        },
    }
    if cfg.ollama_num_gpu is not None:
        body["options"]["num_gpu"] = cfg.ollama_num_gpu
    payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
    url = f"{cfg.ollama_base_url.rstrip('/')}/api/generate"
    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            json.loads(response.read().decode("utf-8"))
        return True
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError):
        return False


def _ollama_reachable(
    cfg: Settings,
    *,
    retries: int = _DEFAULT_RETRIES,
    retry_delay_s: float = _DEFAULT_RETRY_DELAY_S,
) -> bool:
    attempts = max(1, retries)
    for attempt in range(attempts):
        if _fetch_tags_payload(cfg, timeout=8.0) is not None:
            return True
        if attempt < attempts - 1:
            time.sleep(retry_delay_s)
    return False