from __future__ import annotations

import json
import re
import urllib.error
import urllib.request

import narracao_engine as engine

from motor.settings import Settings, get_settings


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
) -> str:
    cfg = settings or get_settings()
    body: dict = {
        "model": cfg.ollama_model_narration,
        "prompt": prompt,
        "stream": False,
    }
    if temperature is not None or num_predict is not None:
        options: dict = {}
        if temperature is not None:
            options["temperature"] = temperature
        if num_predict is not None:
            options["num_predict"] = num_predict
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
        raise RuntimeError(f"Ollama retornou resposta vazia (modelo: {cfg.ollama_model_narration})")
    return text


def generate_reply(
    message: str,
    mode: str,
    settings: Settings | None = None,
    *,
    channel: str = "narracao",
) -> str:
    cfg = settings or get_settings()
    channel = engine.normalize_channel(channel)
    missing = engine.check_integrity()
    if missing:
        return "Nao foi possivel responder porque arquivos obrigatorios estao ausentes."

    context_paths = engine.select_context_files(message, provider=cfg.provider, channel=channel)
    prompt = engine.build_prompt(
        message,
        context_paths,
        mode,
        provider=cfg.provider,
        max_prompt_chars=cfg.ollama_max_prompt_chars if cfg.provider == "ollama" else None,
        channel=channel,
    )

    if cfg.provider == "ollama":
        try:
            if channel == "mestre":
                temp = 0.25
                num_predict = 320
            else:
                temp = 0.55
                num_predict = None
            raw = run_ollama(prompt, cfg, temperature=temp, num_predict=num_predict)
            return engine.sanitize_ollama_reply(raw, channel=channel)
        except Exception as exc:  # pragma: no cover
            return format_provider_failure(cfg.provider, exc, cfg)

    if cfg.provider == "grok":
        try:
            return engine.run_grok(prompt)
        except Exception as exc:  # pragma: no cover
            return format_provider_failure(cfg.provider, exc, cfg)

    if cfg.provider in {"chatgpt", "gemini", "copilot"}:
        return (
            f"Provider de teste '{cfg.provider}' selecionado. "
            "Integração real ainda não configurada; usando resposta local de validação."
        )

    if channel == "mestre" or mode == "mestre":
        return "Canal Mestre off-game ativo. Consulta meta fora da cronologia."
    if mode == "narrador":
        return "Canal de narracao ativo."
    return "Canal principal ativo. Mensagem recebida para narracao da historia."