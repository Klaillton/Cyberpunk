from __future__ import annotations

import json
import urllib.request


def test_brief_endpoint_returns_dynamic_content(api_base_url: str) -> None:
    with urllib.request.urlopen(f"{api_base_url}/api/brief", timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))
    assert data["opening"]
    assert len(data["briefs"]) == 3
    assert data["meta"]["sources"]


def test_health_endpoint_reports_features(api_base_url: str) -> None:
    with urllib.request.urlopen(f"{api_base_url}/api/health", timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))
    assert data["status"] == "ok"
    assert "brief" in data["features"]
    assert "sistema" in data["features"]


def test_session_commands_endpoint_returns_catalog(api_base_url: str) -> None:
    with urllib.request.urlopen(f"{api_base_url}/api/session-commands", timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))
    assert len(data["categories"]) >= 3
    assert data["quick"][0]["text"]


def test_npcs_endpoint_returns_catalog(api_base_url: str) -> None:
    with urllib.request.urlopen(f"{api_base_url}/api/npcs", timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))
    assert data["count"] > 0
    assert data["npcs"][0]["name"]
    assert data["npcs"][0]["tokenUrl"].startswith("/api/npc-image")