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
def search_api_base_url(tmp_path_factory):
    import socket
    import time

    campaign = tmp_path_factory.mktemp("campaign")
    data_dir = tmp_path_factory.mktemp("data")
    fichas = campaign / "fichas"
    fichas.mkdir(parents=True)
    (fichas / "nomad - lena_valk_kane.md").write_text(
        '# Lena "Valk" Kane\n\n## Background\n\nMotorista estoica do The Mule no Pack Badlands.\n',
        encoding="utf-8",
    )

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        port = int(sock.getsockname()[1])

    env = {
        **dict(os.environ),
        "NARRACAO_PROVIDER": "none",
        "NARRACAO_SKIP_PROVIDER_PROMPT": "1",
        "NARRACAO_API_HOST": "127.0.0.1",
        "NARRACAO_API_PORT": str(port),
        "CAMPANHA_ROOT": str(campaign),
        "DATA_DIR": str(data_dir),
        "DB_PATH": str(data_dir / "motor.db"),
        "FAISS_DIR": str(data_dir / "faiss"),
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


def _post_json(url: str, payload: dict) -> tuple[int, dict]:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        body = response.read().decode("utf-8")
        return response.status, json.loads(body)


def test_search_api_returns_npc_chunk(search_api_base_url: str) -> None:
    status, data = _post_json(
        f"{search_api_base_url}/api/search",
        {"query": "Valk motorista Mule", "top_k": 5, "filters": {"doc_type": ["character", "npc"]}},
    )
    assert status == 200
    assert data["hits"]
    paths = [hit["source_path"] for hit in data["hits"]]
    assert any("lena_valk_kane" in path for path in paths)
    assert data["hits"][0]["score"] > 0