#!/usr/bin/env python3
"""Start narracao API with a model, run smoke_manual_turns, stop API. Usage: python scripts/_ab_smoke_one.py llama3.1:8b"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
API = "http://127.0.0.1:8787"


def wait_api(timeout: float = 60.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f"{API}/docs", timeout=2)
            return True
        except Exception:
            time.sleep(0.5)
    return False


def free_port(port: int = 8787) -> None:
    if sys.platform != "win32":
        return
    try:
        out = subprocess.check_output(
            f'netstat -ano | findstr :{port}',
            shell=True,
            text=True,
            errors="replace",
        )
    except subprocess.CalledProcessError:
        return
    pids = set()
    for line in out.splitlines():
        parts = line.split()
        if parts and parts[-1].isdigit():
            pids.add(parts[-1])
    for pid in pids:
        subprocess.run(["taskkill", "/F", "/PID", pid], capture_output=True)


def warm(model: str) -> None:
    import json

    payload = json.dumps(
        {
            "model": model,
            "prompt": "Responda apenas: pronto.",
            "stream": False,
            "keep_alive": "15m",
            "options": {"num_predict": 8, "num_ctx": 2048},
        }
    ).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            resp.read()
        print(f"Warm OK: {model}", flush=True)
    except Exception as exc:
        print(f"Warm WARN: {exc}", flush=True)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: _ab_smoke_one.py <model>")
        return 2
    model = sys.argv[1]
    label = model.replace(":", "_").replace(".", "_")
    out_path = REPO / "agent-tools" / f"ab_smoke_{label}.txt"
    log_path = REPO / "agent-tools" / f"ab_api_{label}.log"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env.update(
        {
            "NARRACAO_PROVIDER": "ollama",
            "OLLAMA_MODEL_NARRATION": model,
            "OLLAMA_MODEL_AUX": "phi3:mini",
            "OLLAMA_MODEL_CLASSIFIER": "phi3:mini",
            "LLM_ROUTING_POLICY": "local_only",
            "CLOUD_FALLBACK_ENABLED": "false",
            "QUALITY_RESCUE_CLOUD_ENABLED": "false",
            "NARRACAO_MIN_TIER": "standard",
            "OLLAMA_NUM_CTX_NARRATION": "4096",
            "OLLAMA_NUM_PREDICT_NARRATION": "350",
            "OLLAMA_MAX_PROMPT_CHARS": "6000",
            "OLLAMA_MAX_CONTEXT_FILES": "8",
            "OLLAMA_KEEP_ALIVE": "15m",
            "OLLAMA_REQUEST_TIMEOUT": "300",
            "OLLAMA_BASE_URL": "http://127.0.0.1:11434",
            "NARRACAO_SKIP_PROVIDER_PROMPT": "1",
            "PYTHONPATH": f"{REPO};{REPO / 'scripts'}",
            "NARRACAO_API_HOST": "127.0.0.1",
            "NARRACAO_API_PORT": "8787",
        }
    )

    free_port(8787)
    warm(model)

    log_f = open(log_path, "w", encoding="utf-8")
    print(f"Starting API with {model}...", flush=True)
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "api.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8787",
            "--log-level",
            "warning",
        ],
        cwd=str(REPO),
        env=env,
        stdout=log_f,
        stderr=subprocess.STDOUT,
    )
    try:
        if not wait_api(90):
            print("API failed to start", flush=True)
            return 1
        print("API ready — running smoke...", flush=True)
        smoke = subprocess.run(
            [sys.executable, str(REPO / "scripts" / "smoke_manual_turns.py")],
            cwd=str(REPO),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=1200,
        )
        body = (smoke.stdout or "") + (smoke.stderr or "")
        out_path.write_text(body, encoding="utf-8")
        print(body, flush=True)
        print(f"Saved {out_path}", flush=True)
        return smoke.returncode
    finally:
        proc.send_signal(signal.SIGTERM)
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
        log_f.close()
        free_port(8787)


if __name__ == "__main__":
    raise SystemExit(main())
