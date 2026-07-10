from __future__ import annotations

import json
import re
import urllib.error
import urllib.request

import narracao_engine as engine

from motor.context_service import ContextService
from motor.llm.channel_profiles import (
    generation_params_for_channel,
    max_context_files_for_channel,
    max_prompt_chars_for_channel,
)
from motor.llm.quality_gate import ResponseQualityGate
from motor.llm.router import ProviderRouter
from motor.llm.types import RoutingDecision, TurnRequest
from motor.routing_log import RoutingLogEntry, RoutingLogStore
from motor.session_command_handler import detect_session_intent
from motor.settings import Settings, get_settings
from motor.turn_types import TurnResult

_MODE_BY_CHANNEL = {
    "narracao": "narrador",
    "mestre": "mestre",
    "sistema": "gestor",
    "gestor": "gestor",
}


def clean_error_text(value: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", value)


def format_provider_failure(provider: str, error: Exception, settings: Settings | None = None) -> str:
    cfg = settings or get_settings()
    message = clean_error_text(str(error)).strip()
    lowered = message.lower()

    if provider == "grok" and ("402" in lowered or "payment required" in lowered or "balance exhausted" in lowered):
        return "Grok indisponivel no momento. O saldo/credito do provider foi esgotado. Escolha outro provider ou tente mais tarde."

    if provider == "ollama" and ("connection" in lowered or "refused" in lowered or "urlopen" in lowered):
        return (
            "Ollama indisponivel. Verifique se o servico esta rodando "
            f"em {cfg.ollama_base_url} e se o modelo '{cfg.ollama_model_narration}' foi baixado."
        )

    if provider in {"chatgpt", "gemini", "copilot"}:
        return f"Provider de teste '{provider}' indisponivel para integracao real neste momento."

    return "Nao foi possivel consultar o provider no momento. Tente novamente mais tarde."


def run_ollama(
    prompt: str,
    settings: Settings | None = None,
    *,
    temperature: float | None = None,
    num_predict: int | None = None,
    num_ctx: int | None = None,
    model: str | None = None,
) -> str:
    cfg = settings or get_settings()
    body: dict = {
        "model": model or cfg.ollama_model_narration,
        "prompt": prompt,
        "stream": False,
    }
    if temperature is not None or num_predict is not None or num_ctx is not None:
        options: dict = {}
        if temperature is not None:
            options["temperature"] = temperature
        if num_predict is not None:
            options["num_predict"] = num_predict
        if num_ctx is not None:
            options["num_ctx"] = num_ctx
        body["options"] = options
    payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
    url = f"{cfg.ollama_base_url.rstrip('/')}/api/generate"
    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=600) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[-2000:]
        raise RuntimeError(f"Ollama HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Ollama indisponivel em {cfg.ollama_base_url}: {exc}") from exc

    text = str(body.get("response", "")).strip()
    if not text:
        raise RuntimeError(
            f"Ollama retornou resposta vazia (modelo: {model or cfg.ollama_model_narration})"
        )
    return text


def _generation_params(
    channel: str,
    session_intent: str | None,
    settings: Settings,
    *,
    retry: bool = False,
) -> tuple[float, int, int | None]:
    return generation_params_for_channel(channel, session_intent, settings, retry=retry)


def _invoke_provider(
    prompt: str,
    decision: RoutingDecision,
    settings: Settings,
    *,
    temperature: float,
    num_predict: int,
    num_ctx: int | None = None,
) -> str:
    provider = decision.provider
    if provider == "ollama":
        return run_ollama(
            prompt,
            settings,
            temperature=temperature,
            num_predict=num_predict,
            num_ctx=num_ctx,
            model=decision.model,
        )
    if provider == "grok":
        return engine.run_grok(prompt)
    if provider in {"chatgpt", "gemini", "copilot"}:
        return (
            f"Provider de teste '{provider}' selecionado. "
            "Integração real ainda não configurada; usando resposta local de validação."
        )
    raise RuntimeError(f"Provider '{provider}' nao suportado para geracao.")


def _quality_correction_suffix(report) -> str:
    failed = [check for check in report.checks if not check.passed]
    if not failed:
        return ""
    details = "; ".join(check.detail for check in failed[:4])
    hints: list[str] = []
    failed_names = {check.name for check in failed}
    if "player_echo" in failed_names or "narrator_repeat" in failed_names:
        hints.append(
            "Avance a cena com fato NOVO: resposta de NPC a pergunta do jogador, detalhe sensorial ou interrupcao."
        )
        hints.append("Nao repita frases do historico nem reformule a acao que o jogador acabou de descrever.")
    if "protagonist_control" in failed_names:
        hints.append("Nao descreva o que Ryan faz — apenas ambiente e NPCs.")
    if "meta_questions" in failed_names:
        hints.append("Remova perguntas ao jogador; termine com reacao do mundo.")
    hint_block = "\n".join(f"- {line}" for line in hints)
    return (
        "\n\n## CORRECAO OBRIGATORIA\n"
        f"A tentativa anterior falhou validacao: {details}.\n"
        "Reescreva usando apenas fatos do contexto e historico. Nao invente NPCs nem locais.\n"
        f"{hint_block}"
    )


def _uses_llm_provider(settings: Settings) -> bool:
    return settings.provider in {"ollama", "grok", "chatgpt", "gemini", "copilot"}


def _fallback_static_reply(channel: str, mode: str) -> str:
    if channel == "sistema":
        return "Canal Sistema ativo. Pergunte sobre LLM, API, arquivos e comandos."
    if channel == "mestre" or mode == "mestre":
        return "Canal Mestre off-game ativo. Consulta meta fora da cronologia."
    if mode == "narrador":
        return "Canal de narracao ativo."
    return "Canal principal ativo. Mensagem recebida para narracao da historia."


def generate_turn(
    message: str,
    mode: str,
    settings: Settings | None = None,
    *,
    channel: str = "narracao",
    history: list[dict] | None = None,
    user_approved_cloud: bool = False,
) -> TurnResult:
    cfg = settings or get_settings()
    channel = engine.normalize_channel(channel)
    session_intent = detect_session_intent(message)
    missing = engine.check_integrity()
    if missing:
        return TurnResult(
            reply="Nao foi possivel responder porque arquivos obrigatorios estao ausentes.",
        )

    context_service = ContextService(cfg)
    selection = context_service.select(
        message,
        provider=cfg.provider,
        channel=channel,
        session_intent=session_intent,
        max_files=max_context_files_for_channel(channel, cfg),
    )

    effective_mode = _MODE_BY_CHANNEL.get(channel, mode)
    request = TurnRequest(
        message=message.strip(),
        channel=channel,
        mode=effective_mode,
    )

    router = ProviderRouter(cfg)
    quality_gate = ResponseQualityGate()
    routing_log = RoutingLogStore()

    decision = router.resolve(
        request,
        selection.entities,
        selection.manifest,
        user_approved_cloud=user_approved_cloud,
    )

    if not _uses_llm_provider(cfg) and decision.provider in {"ollama", "grok"}:
        decision = RoutingDecision(
            provider=cfg.provider,
            model=None,
            tier=decision.tier,
            score=decision.score,
            reasons=decision.reasons + ["provider:none_static"],
            policy=decision.policy,
            escalated=False,
            requires_user_approval=False,
        )

    prompt = engine.build_prompt(
        message,
        selection.paths,
        effective_mode,
        provider=cfg.provider if cfg.provider == "ollama" else decision.provider,
        max_prompt_chars=(
            max_prompt_chars_for_channel(channel, cfg) if decision.provider == "ollama" else None
        ),
        channel=channel,
        session_intent=session_intent,
        history=history,
    )

    if not _uses_llm_provider(cfg):
        return TurnResult(
            reply=_fallback_static_reply(channel, effective_mode),
            routing_decision=decision,
            context_sources=selection.manifest.source_paths,
        )

    run_quality = channel == "narracao" and session_intent != "summary"
    temp, num_predict, num_ctx = _generation_params(channel, session_intent, cfg)
    attempts = 0
    last_reply = ""
    last_report = None
    active_decision = decision
    active_prompt = prompt

    while attempts < 2:
        attempts += 1
        retry = attempts > 1
        if retry:
            temp, num_predict, num_ctx = _generation_params(channel, session_intent, cfg, retry=True)

        try:
            raw = _invoke_provider(
                active_prompt,
                active_decision,
                cfg,
                temperature=temp,
                num_predict=num_predict,
                num_ctx=num_ctx,
            )
            last_reply = engine.sanitize_ollama_reply(
                raw,
                channel=channel,
                session_intent=session_intent,
                history=history,
            )
        except Exception as exc:  # pragma: no cover
            return TurnResult(
                reply=format_provider_failure(active_decision.provider, exc, cfg),
                routing_decision=active_decision,
                attempts=attempts,
                provider_used=active_decision.provider,
                model_used=active_decision.model,
                context_sources=selection.manifest.source_paths,
            )

        if not run_quality:
            routing_log.append(
                RoutingLogEntry(
                    channel=channel,
                    mode=effective_mode,
                    message_preview=message,
                    decision=active_decision,
                    attempt=attempts,
                    quality_passed=None,
                )
            )
            return TurnResult(
                reply=last_reply,
                routing_decision=active_decision,
                attempts=attempts,
                provider_used=active_decision.provider,
                model_used=active_decision.model,
                context_sources=selection.manifest.source_paths,
            )

        last_report = quality_gate.validate(
            last_reply,
            selection.manifest,
            channel,
            player_message=message,
            previous_narrator=engine._last_narrator_text(history),
        )
        routing_log.append(
            RoutingLogEntry(
                channel=channel,
                mode=effective_mode,
                message_preview=message,
                decision=active_decision,
                attempt=attempts,
                quality_passed=last_report.passed,
                quality_report=last_report,
            )
        )
        if last_report.passed:
            break

        if attempts >= 2:
            break

        cloud_fallback = router.resolve_fallback(active_decision, quality_passed=False)
        if cloud_fallback is not None:
            active_decision = cloud_fallback
            active_prompt = prompt
        else:
            active_decision = decision
            active_prompt = prompt + _quality_correction_suffix(last_report)

    return TurnResult(
        reply=last_reply,
        routing_decision=active_decision,
        quality_report=last_report,
        attempts=attempts,
        provider_used=active_decision.provider,
        model_used=active_decision.model,
        context_sources=selection.manifest.source_paths,
    )


def generate_reply(
    message: str,
    mode: str,
    settings: Settings | None = None,
    *,
    channel: str = "narracao",
    history: list[dict] | None = None,
) -> str:
    return generate_turn(
        message,
        mode,
        settings,
        channel=channel,
        history=history,
    ).reply