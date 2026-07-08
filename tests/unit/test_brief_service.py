from __future__ import annotations

from motor.brief_service import build_campaign_brief
from motor.npc_catalog import build_npc_catalog
from motor.settings import reset_settings


def test_build_campaign_brief_reads_campaign_files(repo_root) -> None:
    settings = reset_settings(repo_root)
    brief = build_campaign_brief(settings)

    assert brief["opening"]
    assert "canal" in brief["opening"].lower()
    assert len(brief["briefs"]) == 3
    ids = {item["id"] for item in brief["briefs"]}
    assert ids == {"summary", "objective_long", "objective_short"}

    summary = next(item for item in brief["briefs"] if item["id"] == "summary")
    assert summary["teaser"]
    assert "Pack" in summary["detail"] or "pack" in summary["detail"].lower()
    assert summary["sources"]

    assert brief["meta"]["location"]
    assert brief["meta"]["date"]


def test_build_npc_catalog_resolves_valk_sheet(repo_root) -> None:
    settings = reset_settings(repo_root)
    catalog = build_npc_catalog(settings)
    valk = next(
        (npc for npc in catalog["npcs"] if "valk" in npc["name"].lower()),
        None,
    )
    assert valk is not None
    assert valk["sheetPath"]
    assert "lena_valk_kane" in valk["sheetPath"].lower()
    assert valk["hasSheet"]


def test_build_npc_catalog_includes_board_npcs(repo_root) -> None:
    settings = reset_settings(repo_root)
    catalog = build_npc_catalog(settings)

    assert catalog["count"] > 0
    names = {npc["name"].lower() for npc in catalog["npcs"]}
    assert "reyes" in names
    featured = [npc for npc in catalog["npcs"] if npc["featured"]]
    assert featured
    assert featured[0]["summary"]
    assert featured[0]["imageUrl"].startswith("/api/npc-image")


def test_build_npc_catalog_excludes_template_sheets(repo_root) -> None:
    settings = reset_settings(repo_root)
    catalog = build_npc_catalog(settings)

    sheet_paths = {npc["sheetPath"].lower() for npc in catalog["npcs"] if npc["sheetPath"]}
    names = {npc["name"].lower() for npc in catalog["npcs"]}

    assert not any("template" in path for path in sheet_paths)
    assert not any("template" in name for name in names)