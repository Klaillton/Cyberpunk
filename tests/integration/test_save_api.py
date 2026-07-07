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

SAMPLE_NARRATIVE = """Cena encerrada.

---UPDATE_PROPOSALS---
```json
[
  {
    "target_path": "heat.md",
    "target_section": "Heat por Personagem",
    "change_type": "insert_row",
    "payload": {
      "personagem": "Test NPC",
      "nivel": "Baixa",
      "justificativa": "Sem exposicao"
    },
    "rationale": "Teste integracao",
    "confidence": 0.9
  }
]
```
"""

HEAT_SAMPLE = """# Heat

## Heat por Personagem

| Personagem | Nivel | Justificativa |
| ---------- | ----- | ------------- |
"""


@pytest.fixture(scope="module")
def save_api_env(tmp_path_factory):
    import socket
    import time

    campaign = tmp_path_factory.mktemp("campaign_save")
    data_dir = tmp_path_factory.mktemp("data_save")
    (campaign / "heat.md").write_text(HEAT_SAMPLE, encoding="utf-8")

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
        proc.terminate()
        pytest.fail(proc.stderr.read() if proc.stderr else "server failed")

    try:
        yield {"base": base, "campaign": campaign}
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
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = {"error": body}
        return exc.code, parsed


def test_save_api_applies_approved_proposal(save_api_env) -> None:
    base = save_api_env["base"]
    campaign = save_api_env["campaign"]

    status_ingest, ingest = _post_json(
        f"{base}/api/proposals/ingest",
        {"narrative": SAMPLE_NARRATIVE},
    )
    assert status_ingest == 200
    assert ingest["proposals"]
    proposal_id = ingest["proposals"][0]["id"]

    status_save, saved = _post_json(
        f"{base}/api/save",
        {"proposal_ids": [proposal_id], "approved": True},
    )
    assert status_save == 200
    assert saved["applied"] == 1
    assert "heat.md" in saved["files_changed"]

    content = (campaign / "heat.md").read_text(encoding="utf-8")
    assert "Test NPC" in content