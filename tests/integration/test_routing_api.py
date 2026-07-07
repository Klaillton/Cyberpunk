from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


@pytest.fixture(scope="module")
def routing_api_base_url():
    import socket
    import time

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        port = int(sock.getsockname()[1])

    env = {
        **dict(os.environ),
        "NARRACAO_PROVIDER": "ollama",
        "NARRACAO_SKIP_PROVIDER_PROMPT": "1",
        "NARRACAO_API_HOST": "127.0.0.1",
        "NARRACAO_API_PORT": str(port),
        "LLM_ROUTING_POLICY": "local_preferred",
        "CLOUD_FALLBACK_ENABLED": "false",
        "PYTHONPATH": os.pathsep.join(
            [str(REPO_ROOT), str(REPO_ROOT / "scripts"), os.environ.get("PYTHONPATH", "")]
        ).strip(os.pathsep),
    }

    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api.main:app", "--host", "127.0.0.1", "--port", str(port)],
        cwd=str(REPO_ROOT),
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    base = f"http://127.0.0.1:{port}"
    deadline = time.time() + 45.0
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{base}/", timeout=2) as response:
                if response.status == 200:
                    break
        except (urllib.error.URLError, TimeoutError):
            time.sleep(0.25)
    else:
        stderr = proc.stderr.read() if proc.stderr else ""
        proc.terminate()
        pytest.fail(f"Servidor nao subiu: {stderr}")

    try:
        yield base
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


def _get_json(url: str) -> tuple[int, dict]:
    with urllib.request.urlopen(url, timeout=10) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def _post_json(url: str, payload: dict) -> tuple[int, dict]:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def test_routing_policy_endpoint(routing_api_base_url: str) -> None:
    status, data = _get_json(f"{routing_api_base_url}/api/routing/policy")
    assert status == 200
    assert data["policy"] == "local_preferred"
    assert data["default_provider"] == "ollama"
    assert data["cloud_fallback_enabled"] is False


def test_routing_preview_returns_local_decision(routing_api_base_url: str) -> None:
    status, data = _post_json(
        f"{routing_api_base_url}/api/routing/preview",
        {"message": "Observo o acampamento", "channel": "narracao"},
    )
    assert status == 200
    assert data["decision"]["provider"] == "ollama"
    assert data["decision"]["tier"] in {"trivial", "standard", "complex"}
    assert "reasons" in data["decision"]
    assert data["would_escalate_to_cloud"] is False