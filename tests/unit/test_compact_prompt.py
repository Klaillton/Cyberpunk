from __future__ import annotations

from pathlib import Path

from motor.llm.compact_prompt import build_quality_rescue_prompt
from motor.llm.types import ContextManifest
from motor.settings import reset_settings


def test_build_quality_rescue_prompt_is_compact_and_structured(repo_root: Path) -> None:
    settings = reset_settings(repo_root)
    board = (repo_root / "board" / "board_campanha.md").read_text(encoding="utf-8")
    manifest = ContextManifest(
        total_chars=len(board),
        source_paths=["board/board_campanha.md", "fichas/npc/reyes.md"],
        entity_ids=["reyes", "lena_valk_kane"],
        board_excerpt=board[:4000],
    )
    paths = [
        repo_root / "board" / "board_campanha.md",
        repo_root / "fichas" / "npc" / "reyes.md",
        repo_root / "fichas" / "nomad - lena_valk_kane.md",
    ]
    prompt = build_quality_rescue_prompt(
        message='Volto no Mule com a Valk.\n\n"Quanto eles ja sabem?"',
        history=[
            {"role": "user", "content": "Estou no Mule voltando da incursao"},
            {
                "role": "assistant",
                "content": "O acampamento surge no horizonte sob sol baixo.",
            },
        ],
        manifest=manifest,
        context_paths=paths,
        repo_root=repo_root,
        quality_details="Eco da acao do jogador",
        max_chars=4500,
    )

    assert len(prompt) <= 4500
    assert "## Resumo da cena (canon)" in prompt
    assert "## Historico recente" in prompt
    assert "## Acao do jogador AGORA" in prompt
    assert "NPCs envolvidos" in prompt
    assert "Falhas da validacao local" in prompt
    assert "Badlands" in prompt
    assert settings.repo_root == repo_root