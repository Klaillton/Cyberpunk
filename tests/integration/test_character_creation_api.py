from __future__ import annotations

import sys

import pytest
from fastapi.testclient import TestClient

from api.main import create_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())


def test_catalog_endpoint(client: TestClient) -> None:
    response = client.get("/api/character-creation/catalog")
    assert response.status_code == 200
    data = response.json()
    assert len(data.get("roles", [])) == 10


def test_sheet_endpoint_ryan(client: TestClient) -> None:
    response = client.get("/api/characters/ryan_wireghost_voss/sheet")
    assert response.status_code == 200
    data = response.json()
    assert data.get("tier") == "protagonist"
    assert data.get("stats", {}).get("TECH") == 8


def test_seed_pack_roster(client: TestClient) -> None:
    response = client.post("/api/factions/pack_badlands/seed-roster")
    assert response.status_code == 200
    assert "skipped" in response.json()