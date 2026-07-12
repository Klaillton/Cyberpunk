from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest

from motor.settings import reset_settings

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(autouse=True)
def _reset_settings_singleton() -> None:
    reset_settings(REPO_ROOT)
SCRIPTS_DIR = REPO_ROOT / "scripts"


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _wait_for_http(url: str, timeout: float = 30.0) -> None:
    deadline = time.time() + timeout
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                if response.status == 200:
                    return
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
            time.sleep(0.25)
    raise RuntimeError(f"Servidor nao respondeu em {url}: {last_error}")


@pytest.fixture(scope="module")
def api_base_url(tmp_path_factory) -> str:
    """Sobe narracao_api.py em porta livre com journal isolado."""
    journal_dir = tmp_path_factory.mktemp("journal")
    port = _find_free_port()
    env = {
        **dict(__import__("os").environ),
        "NARRACAO_PROVIDER": "none",
        "NARRACAO_API_HOST": "127.0.0.1",
        "NARRACAO_API_PORT": str(port),
        "JOURNAL_DIR": str(journal_dir),
        "NARRACAO_SKIP_PROVIDER_PROMPT": "1",
    }
    env["PYTHONPATH"] = os.pathsep.join(
        [str(REPO_ROOT), str(SCRIPTS_DIR), env.get("PYTHONPATH", "")]
    ).strip(os.pathsep)

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
        cwd=str(REPO_ROOT),
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    base = f"http://127.0.0.1:{port}"
    try:
        _wait_for_http(f"{base}/", timeout=45.0)
        yield base
    except RuntimeError as exc:
        stderr = proc.stderr.read() if proc.stderr else ""
        proc.terminate()
        raise RuntimeError(f"{exc}\n--- stderr ---\n{stderr}") from exc
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()