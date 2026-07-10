from __future__ import annotations

from motor.settings import Settings

TIER_RANK: dict[str, int] = {
    "trivial": 0,
    "standard": 1,
    "complex": 2,
    "critical": 3,
}

NARRATION_CHANNELS = frozenset({"narracao", "gestor"})
AUX_CHANNELS = frozenset({"sistema", "mestre"})


def is_narration_channel(channel: str) -> bool:
    return channel in NARRATION_CHANNELS


def is_aux_channel(channel: str) -> bool:
    return channel in AUX_CHANNELS


def _tier_at_least(tier: str, floor: str) -> str:
    if TIER_RANK.get(tier, 0) >= TIER_RANK.get(floor, 0):
        return tier
    return floor


def _tier_at_most(tier: str, ceiling: str) -> str:
    if TIER_RANK.get(tier, 0) <= TIER_RANK.get(ceiling, 99):
        return tier
    return ceiling


def apply_channel_tier(channel: str, tier: str, settings: Settings) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if is_narration_channel(channel):
        floored = _tier_at_least(tier, settings.narration_min_tier)
        reasons.append(f"profile:narracao_tier={floored}")
        return floored, reasons
    if is_aux_channel(channel):
        capped = _tier_at_most(tier, "trivial")
        reasons.append(f"profile:aux_tier={capped}")
        return capped, reasons
    return tier, reasons


def local_model_for_channel(channel: str, settings: Settings) -> str:
    if is_aux_channel(channel):
        return settings.ollama_model_aux
    return settings.ollama_model_narration


def max_context_files_for_channel(channel: str, settings: Settings) -> int:
    if is_aux_channel(channel):
        return settings.ollama_max_context_files_aux
    return settings.ollama_max_context_files


def max_prompt_chars_for_channel(channel: str, settings: Settings) -> int:
    if is_aux_channel(channel):
        return settings.ollama_max_prompt_chars_aux
    return settings.ollama_max_prompt_chars


def generation_params_for_channel(
    channel: str,
    session_intent: str | None,
    settings: Settings,
    *,
    retry: bool = False,
) -> tuple[float, int, int | None]:
    """Retorna (temperature, num_predict, num_ctx)."""
    if session_intent == "summary":
        return (
            0.18 if retry else 0.2,
            settings.ollama_num_predict_summary,
            settings.ollama_num_ctx_narration,
        )
    if is_aux_channel(channel):
        temp = 0.18 if channel == "mestre" and not retry else (0.1 if retry else 0.12)
        if channel == "mestre" and retry:
            temp = 0.16
        return (
            temp,
            settings.ollama_num_predict_aux,
            settings.ollama_num_ctx_aux,
        )
    return (
        0.26 if retry else 0.32,
        settings.ollama_num_predict_narration,
        settings.ollama_num_ctx_narration,
    )