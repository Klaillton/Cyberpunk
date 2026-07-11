from __future__ import annotations

from unittest.mock import patch

from motor.narration import format_provider_failure
from motor.ollama_health import inspect_ollama, model_is_installed
from motor.settings import reset_settings


def test_format_provider_failure_reports_missing_model() -> None:
    settings = reset_settings()
    settings.ollama_model_narration = "qwen2.5:14b-instruct"
    message = format_provider_failure(
        "ollama",
        RuntimeError('Ollama HTTP 404: {"error":"model \'qwen2.5:14b-instruct\' not found"}'),
        settings,
    )
    assert "nao esta instalado" in message
    assert "qwen2.5:14b-instruct" in message


def test_model_is_installed_matches_name_prefix() -> None:
    settings = reset_settings()
    with patch("motor.ollama_health.list_installed_models", return_value=["llama3.1:8b"]):
        assert model_is_installed("llama3.1:8b", settings)
        assert not model_is_installed("qwen2.5:14b-instruct", settings)


def test_format_provider_failure_ollama_empty_message() -> None:
    settings = reset_settings()
    message = format_provider_failure("ollama", RuntimeError(), settings)
    assert "Ollama falhou" in message
    assert "qwen2.5:14b-instruct" in message


def test_inspect_ollama_marks_narration_not_ready() -> None:
    settings = reset_settings()
    settings.provider = "ollama"
    settings.ollama_model_narration = "qwen2.5:14b-instruct"
    with patch(
        "motor.ollama_health.list_installed_models",
        return_value=["llama3.1:8b"],
    ), patch("motor.ollama_health._ollama_reachable", return_value=True):
        report = inspect_ollama(settings)
    assert report["reachable"] is True
    assert report["narration_ready"] is False
    assert "llama3.1:8b" in report["installed_models"]