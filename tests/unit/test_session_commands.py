from __future__ import annotations

from motor.session_commands import build_session_commands
from motor.settings import reset_settings


def test_build_session_commands_exposes_documented_player_commands() -> None:
    data = build_session_commands()
    assert len(data["categories"]) == 3
    assert len(data["quick"]) == 3

    texts = {
        command["text"]
        for category in data["categories"]
        for command in category["commands"]
    }
    assert "[Resumo da Sessão]" in texts
    assert "[Finalizar sessão e gerar resumo]" in texts
    assert any("Pulso do Mundo" in text for text in texts)


def test_build_session_commands_loads_descriptions_from_sistema_files(repo_root) -> None:
    settings = reset_settings(repo_root)
    data = build_session_commands(settings)

    summary_category = next(cat for cat in data["categories"] if cat["id"] == "summary")
    resumo = next(cmd for cmd in summary_category["commands"] if cmd["id"] == "resumo_sessao")
    assert "sessao_resumo" in resumo["description"].lower()
    assert resumo["behavior"]
    assert "confirmação" in resumo["behavior"].lower() or "confirmacao" in resumo["behavior"].lower()
    assert resumo["source"] == "sistema/instrucoes_projeto.md"

    updates_category = next(cat for cat in data["categories"] if cat["id"] == "updates")
    preview = next(cmd for cmd in updates_category["commands"] if cmd["id"] == "preview_atualizacoes")
    assert preview["description"]
    assert preview["behavior"]
    assert preview["source"] == "sistema/como_atualizar_arquivos.md"

    time_category = next(cat for cat in data["categories"] if cat["id"] == "time")
    pulso = next(cmd for cmd in time_category["commands"] if cmd["id"] == "pulso_1_dia")
    assert "pulso" in pulso["behavior"].lower()

    assert data["sources"] == [
        "sistema/instrucoes_projeto.md",
        "sistema/como_atualizar_arquivos.md",
    ]