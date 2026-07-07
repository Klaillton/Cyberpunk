from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request


def _get_json(url: str) -> tuple[int, dict | list | str]:
    with urllib.request.urlopen(url, timeout=10) as response:
        body = response.read().decode("utf-8")
        return response.status, json.loads(body)


def _post_json(url: str, payload: dict) -> tuple[int, dict]:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = {"error": body}
        return exc.code, parsed


def test_root_serves_frontend(api_base_url: str) -> None:
    with urllib.request.urlopen(f"{api_base_url}/", timeout=10) as response:
        html = response.read().decode("utf-8")
    assert response.status == 200
    assert "NARRACAO AO VIVO" in html
    assert "app.js" in html


def test_character_profile_returns_sections(api_base_url: str) -> None:
    status, data = _get_json(f"{api_base_url}/api/character-profile")
    assert status == 200
    assert data["characterId"] == "ryan_wireghost_voss"
    assert data["sourceSheet"].endswith("ryan_wireghost_voss.md")
    section_titles = [s["title"] for s in data.get("sections", [])]
    assert any("Aparência" in t or "Background" in t for t in section_titles)


def test_journal_crud_flow(api_base_url: str) -> None:
    char_id = "ryan_wireghost_voss"
    note = f"nota-integration-{__import__('time').time_ns()}"

    status_post, data_post = _post_json(
        f"{api_base_url}/api/journal/{char_id}",
        {"timestamp": "07/07/2026, 12:00:00", "text": note},
    )
    assert status_post == 201
    entries = data_post["entries"]
    created = next(e for e in entries if e["text"] == note)
    entry_id = created["id"]

    status_get, data_get = _get_json(f"{api_base_url}/api/journal/{char_id}")
    assert status_get == 200
    assert any(e["text"] == note for e in data_get["entries"])

    delete_url = f"{api_base_url}/api/journal/{char_id}/{urllib.parse.quote(entry_id)}"
    request = urllib.request.Request(delete_url, method="DELETE")
    with urllib.request.urlopen(request, timeout=10) as response:
        deleted = json.loads(response.read().decode("utf-8"))
    assert response.status == 200
    assert all(e["id"] != entry_id for e in deleted["entries"])


def test_narracao_endpoint_none_provider(api_base_url: str) -> None:
    status, data = _post_json(
        f"{api_base_url}/api/narracao",
        {"message": "Observo o acampamento"},
    )
    assert status == 200
    assert data["channel"] == "narracao"
    assert data["provider"] == "none"
    assert "reply" in data and data["reply"]


def test_narrador_endpoint_off_record(api_base_url: str) -> None:
    status, data = _post_json(
        f"{api_base_url}/api/narrador",
        {"message": "Posso confiar no Reyes?"},
    )
    assert status == 200
    assert data["channel"] == "mestre"
    assert "Canal Mestre off-game ativo" in data["reply"]


def test_narracao_rejects_empty_message(api_base_url: str) -> None:
    status, data = _post_json(f"{api_base_url}/api/narracao", {"message": "  "})
    assert status == 400
    assert "error" in data


def test_npc_asset_returns_urls(api_base_url: str) -> None:
    query = urllib.parse.urlencode({"name": "Lira", "gender": "female"})
    status, data = _get_json(f"{api_base_url}/api/npc-asset?{query}")
    assert status == 200
    assert "tokenUrl" in data
    assert "imageUrl" in data