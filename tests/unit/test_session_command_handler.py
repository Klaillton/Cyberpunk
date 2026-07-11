from __future__ import annotations

from motor.session_command_handler import (
    detect_session_intent,
    format_history_block,
    is_finalize_summary_command,
    next_session_log_rel,
    normalize_history_entry,
    session_summary_context_paths,
)
from motor.settings import reset_settings


def test_detect_session_intent_recognizes_summary_commands() -> None:
    assert detect_session_intent("[Resumo da Sessão]") == "summary"
    assert detect_session_intent("[Finalizar sessão e gerar resumo]") == "summary"
    assert detect_session_intent("Criar resumo da sessão atual") == "summary"


def test_is_finalize_summary_command() -> None:
    assert is_finalize_summary_command("[Finalizar sessão e gerar resumo]")
    assert not is_finalize_summary_command("[Resumo da Sessão]")


def test_next_session_log_rel_uses_latest_number(repo_root) -> None:
    settings = reset_settings(repo_root)
    assert next_session_log_rel(settings) == "logs/sessao_resumo_007.md"


def test_session_summary_context_paths_include_template_and_latest(repo_root) -> None:
    settings = reset_settings(repo_root)
    paths = session_summary_context_paths(settings)
    assert "logs/sessao_resumo_template.md" in paths
    assert "sistema/diretrizes_ia.md" in paths
    assert any(path.endswith("sessao_resumo_006.md") for path in paths)


def test_format_history_block_renders_entries() -> None:
    block = format_history_block(
        [
            {"role": "user", "content": "[HISTORIA] VOCE: ataco a torre"},
            {"role": "assistant", "content": "NARRADOR: Ryan avanca em silencio"},
        ]
    )
    assert "Jogador" in block
    assert "ataco a torre" in block
    assert "Ryan avanca" in block


def test_format_history_block_empty_does_not_ask_model_to_warn_player() -> None:
    block = format_history_block([])
    assert "avise que o resumo" not in block.lower()
    assert "Primeiro turno" in block


def test_normalize_history_entry_strips_meta_and_prefixes() -> None:
    polluted = (
        "NARRADOR: Ryan olha ao redor. "
        "LLM: ollama · validacao: revisada · tentativas: 2"
    )
    assert normalize_history_entry("assistant", polluted) == "Ryan olha ao redor."
    assert (
        normalize_history_entry("user", "[HISTORIA] VOCE: observo o patio")
        == "observo o patio"
    )