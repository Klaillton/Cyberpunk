#!/usr/bin/env python3
"""Smoke manual: 3 turnos reais contra /api/narracao (perfil estavel 8B)."""

from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request

API = "http://127.0.0.1:8787"
TURNS = [
    ("acao_simples", "Eu vou ate a oficina ver como esta o andamento dos projetos"),
    (
        "dialogo",
        'Eu entro na oficina e pergunto: "Elias, como esta o andamento do projeto?"',
    ),
    ("acao_sequencia", "Eu observo as pecas na bancada e espero a resposta dele"),
]


def post_narracao(message: str, history: list[dict]) -> tuple[float, dict]:
    payload = {"message": message, "history": history}
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        f"{API}/api/narracao",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=300) as response:
        body = json.loads(response.read().decode("utf-8"))
    elapsed = time.perf_counter() - started
    return elapsed, body


def main() -> int:
    history: list[dict] = []
    print(f"Smoke manual — {API} (3 turnos)\n")

    for index, (label, message) in enumerate(TURNS, start=1):
        print(f"--- Turno {index}: {label} ---")
        print(f"Jogador: {message}")
        try:
            elapsed, data = post_narracao(message, history)
        except urllib.error.HTTPError as exc:
            print(f"ERRO HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')[:500]}")
            return 1
        except Exception as exc:  # pragma: no cover
            print(f"ERRO: {exc}")
            return 1

        reply = (data.get("reply") or "").strip()
        provider = data.get("provider", "?")
        routing = data.get("routing_decision") or {}
        tier = routing.get("tier", "?")
        quality = data.get("quality_passed")
        attempts = data.get("turn_attempts")
        reasons = routing.get("reasons") or []
        rescue = any("quality_gate:rescue_cloud" in str(r) for r in reasons)

        preview = reply.replace("\n", " ")[:280]
        if len(reply) > 280:
            preview += "..."

        print(f"Tempo: {elapsed:.1f}s")
        print(f"LLM: {provider} · tier {tier} · qualidade {quality} · tentativas {attempts}")
        if rescue and provider == "grok":
            print("AVISO: rescue Grok acionado")
        elif rescue:
            print("AVISO: reason rescue_cloud presente mas provider nao e grok")
        print(f"Narrador: {preview}\n")

        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": reply})

    print("Smoke concluido — 3/3 turnos OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())