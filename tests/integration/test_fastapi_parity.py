"""Garante que a API ativa é FastAPI e permanece importável."""

from __future__ import annotations

from fastapi import FastAPI

from api.main import app


def test_app_is_fastapi_instance() -> None:
    assert isinstance(app, FastAPI)


def test_openapi_exposes_legacy_paths() -> None:
    paths = app.openapi()["paths"]
    for route in (
        "/api/narracao",
        "/api/mestre",
        "/api/narrador",
        "/api/character-profile",
        "/api/journal/{character_id}",
        "/api/npc-asset",
        "/api/search",
        "/api/routing/preview",
        "/api/routing/policy",
        "/api/proposals",
        "/api/save",
    ):
        assert route in paths, f"Rota ausente no OpenAPI: {route}"