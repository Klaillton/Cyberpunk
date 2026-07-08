from __future__ import annotations

from pathlib import Path

from motor.markdown.campaign_paths import (
    discover_campaign_files,
    is_campaign_content_path,
    is_template_path,
)


def test_is_template_path_detects_known_templates() -> None:
    templates = [
        "fichas/npc/npc_template.md",
        "logs/sessao_resumo_template.md",
        "logs/job_template.md",
        "logs/pulso_log_template.md",
        "facoes/faccao_template.md",
        "pulso_do_mundo/template_pulso_npc.md",
    ]
    for rel in templates:
        assert is_template_path(rel), rel


def test_is_campaign_content_path_accepts_live_files() -> None:
    live_files = [
        "fichas/nomad - lena_valk_kane.md",
        "board/board_campanha.md",
        "logs/sessao_resumo_042.md",
        "heat.md",
    ]
    for rel in live_files:
        assert is_campaign_content_path(rel), rel


def test_discover_campaign_files_excludes_templates(tmp_path: Path) -> None:
    fichas = tmp_path / "fichas" / "npc"
    fichas.mkdir(parents=True)
    logs = tmp_path / "logs"
    logs.mkdir(parents=True)

    (fichas / "npc_template.md").write_text("# template", encoding="utf-8")
    (fichas / "fixer - reyes.md").write_text("# Reyes", encoding="utf-8")
    (logs / "sessao_resumo_template.md").write_text("# template", encoding="utf-8")
    (logs / "sessao_resumo_001.md").write_text("# sessao", encoding="utf-8")

    discovered = discover_campaign_files(tmp_path)
    rel_paths = {path.relative_to(tmp_path).as_posix() for path in discovered}

    assert "fichas/npc/fixer - reyes.md" in rel_paths
    assert "logs/sessao_resumo_001.md" in rel_paths
    assert "fichas/npc/npc_template.md" not in rel_paths
    assert "logs/sessao_resumo_template.md" not in rel_paths