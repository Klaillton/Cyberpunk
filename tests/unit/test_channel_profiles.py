from __future__ import annotations

from motor.llm.channel_profiles import (
    apply_channel_tier,
    generation_params_for_channel,
    local_model_for_channel,
    max_context_files_for_channel,
)
from motor.settings import reset_settings


def test_narracao_floor_standard() -> None:
    settings = reset_settings()
    settings.narration_min_tier = "standard"
    tier, reasons = apply_channel_tier("narracao", "trivial", settings)
    assert tier == "standard"
    assert any("profile:narracao_tier=standard" in reason for reason in reasons)


def test_aux_cap_trivial() -> None:
    settings = reset_settings()
    tier, reasons = apply_channel_tier("sistema", "complex", settings)
    assert tier == "trivial"
    assert any("profile:aux_tier=trivial" in reason for reason in reasons)


def test_local_model_by_channel() -> None:
    settings = reset_settings()
    settings.ollama_model_narration = "llama3.1:8b"
    settings.ollama_model_aux = "phi3:mini"
    assert local_model_for_channel("narracao", settings) == "llama3.1:8b"
    assert local_model_for_channel("sistema", settings) == "phi3:mini"
    assert local_model_for_channel("mestre", settings) == "phi3:mini"


def test_narracao_generation_uses_higher_budget() -> None:
    settings = reset_settings()
    aux_temp, aux_predict, aux_ctx = generation_params_for_channel("sistema", None, settings)
    narr_temp, narr_predict, narr_ctx = generation_params_for_channel("narracao", None, settings)
    assert narr_predict > aux_predict
    assert narr_ctx >= aux_ctx
    assert narr_temp >= aux_temp


def test_max_context_files_narracao_vs_aux() -> None:
    settings = reset_settings()
    assert max_context_files_for_channel("narracao", settings) > max_context_files_for_channel(
        "sistema", settings
    )