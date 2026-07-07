"""Helpers compartilhados para smoke tests Ollama (@slow)."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import urllib.error
import urllib.request

from motor.settings import Settings, get_settings


def docker_available() -> bool:
    return shutil.which("docker") is not None


def ollama_reachable(base_url: str, timeout: float = 3.0) -> bool:
    url = f"{base_url.rstrip('/')}/api/tags"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return response.status == 200
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def ollama_model_installed(base_url: str, model: str, timeout: float = 5.0) -> bool:
    url = f"{base_url.rstrip('/')}/api/tags"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError):
        return False

    target = model.split(":")[0].lower()
    for entry in payload.get("models", []):
        name = str(entry.get("name", "")).lower()
        if name == model.lower() or name.startswith(f"{target}:"):
            return True
    return False


def ollama_runtime(settings: Settings | None = None) -> tuple[Settings, str]:
    """Retorna settings e motivo de skip se Ollama/modelo indisponíveis."""
    cfg = settings or get_settings()
    if not ollama_reachable(cfg.ollama_base_url):
        return cfg, f"Ollama indisponivel em {cfg.ollama_base_url}"
    if not ollama_model_installed(cfg.ollama_base_url, cfg.ollama_model_narration):
        return (
            cfg,
            f"Modelo '{cfg.ollama_model_narration}' nao instalado. "
            f"Execute: .\\deploy\\scripts\\pull_models.ps1",
        )
    return cfg, ""


def docker_compose_config_valid(compose_file: str, env_file: str | None = None) -> bool:
    if not docker_available():
        return False
    cmd = ["docker", "compose"]
    if env_file:
        cmd.extend(["--env-file", env_file])
    cmd.extend(["-f", compose_file, "config", "--quiet"])
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=30)
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return False


def docker_daemon_running() -> bool:
    if not docker_available():
        return False
    try:
        subprocess.run(
            ["docker", "info"],
            check=True,
            capture_output=True,
            text=True,
            timeout=15,
        )
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return False