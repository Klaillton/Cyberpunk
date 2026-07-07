"""Validação estática do stack Docker (rápido, sem subir containers)."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from tests.integration.ollama_helpers import docker_available, docker_daemon_running

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
COMPOSE_FILE = REPO_ROOT / "deploy" / "docker-compose.yml"
COMPOSE_PI_FILE = REPO_ROOT / "deploy" / "docker-compose.pi.yml"
ENV_EXAMPLE = REPO_ROOT / "deploy" / ".env.example"


@pytest.mark.skipif(not docker_available(), reason="docker CLI nao encontrado")
def test_docker_compose_laptop_config_valid() -> None:
    if not docker_daemon_running():
        pytest.skip("Docker daemon nao esta rodando")

    subprocess.run(
        ["docker", "compose", "-f", str(COMPOSE_FILE), "--env-file", str(ENV_EXAMPLE), "config", "--quiet"],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )


@pytest.mark.skipif(not docker_available(), reason="docker CLI nao encontrado")
def test_docker_compose_pi_config_valid() -> None:
    if not docker_daemon_running():
        pytest.skip("Docker daemon nao esta rodando")

    subprocess.run(
        ["docker", "compose", "-f", str(COMPOSE_PI_FILE), "config", "--quiet"],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_compose_files_define_expected_services() -> None:
    laptop = COMPOSE_FILE.read_text(encoding="utf-8")
    assert "ollama:" in laptop
    assert "motor:" in laptop
    assert "ollama-pull:" in laptop

    pi = COMPOSE_PI_FILE.read_text(encoding="utf-8")
    assert "motor:" in pi
    assert "ollama:" not in pi