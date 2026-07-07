"""Smoke tests contra Ollama real — executar com: npm run test:slow"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

import pytest

from motor.narration import run_ollama
from motor.settings import reset_settings
from tests.integration.ollama_helpers import ollama_runtime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(scope="module")
def ollama_settings():
    cfg, skip_reason = ollama_runtime()
    if skip_reason:
        pytest.skip(skip_reason)
    return cfg


def _post_json(url: str, payload: dict, timeout: float = 120.0) -> tuple[int, dict]:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = {"error": body}
        return exc.code, parsed


@pytest.fixture(scope="module")
def ollama_api_base_url(tmp_path_factory, ollama_settings):
    """Sobe FastAPI com NARRACAO_PROVIDER=ollama apontando para Ollama real."""
    import socket
    import time

    journal_dir = tmp_path_factory.mktemp("journal_ollama")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        port = int(sock.getsockname()[1])

    env = {
        **dict(os.environ),
        "NARRACAO_PROVIDER": "ollama",
        "NARRACAO_API_HOST": "127.0.0.1",
        "NARRACAO_API_PORT": str(port),
        "JOURNAL_DIR": str(journal_dir),
        "NARRACAO_SKIP_PROVIDER_PROMPT": "1",
        "OLLAMA_BASE_URL": ollama_settings.ollama_base_url,
        "OLLAMA_MODEL_NARRATION": ollama_settings.ollama_model_narration,
        "PYTHONPATH": os.pathsep.join(
            [REPO_ROOT, os.path.join(REPO_ROOT, "scripts"), os.environ.get("PYTHONPATH", "")]
        ).strip(os.pathsep),
    }

    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "api.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        cwd=REPO_ROOT,
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    base = f"http://127.0.0.1:{port}"
    deadline = time.time() + 45.0
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{base}/", timeout=2) as response:
                if response.status == 200:
                    break
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
            time.sleep(0.25)
    else:
        stderr = proc.stderr.read() if proc.stderr else ""
        proc.terminate()
        pytest.fail(f"Servidor nao respondeu em {base}: {last_error}\n--- stderr ---\n{stderr}")

    try:
        yield base
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


@pytest.mark.slow
def test_run_ollama_returns_text(ollama_settings) -> None:
    reset_settings()
    reply = run_ollama("Responda apenas: OK", settings=ollama_settings)
    assert reply.strip()
    assert "Ollama indisponivel" not in reply


@pytest.mark.slow
def test_narracao_endpoint_uses_ollama_provider(ollama_api_base_url, ollama_settings) -> None:
    status, data = _post_json(
        f"{ollama_api_base_url}/api/narracao",
        {"message": "Descreva em uma frase um beco em Night City."},
        timeout=600.0,
    )
    assert status == 200
    assert data["channel"] == "narracao"
    assert data["provider"] == "ollama"
    assert data.get("model") == ollama_settings.ollama_model_narration
    assert data["reply"].strip()
    assert "Ollama indisponivel" not in data["reply"]