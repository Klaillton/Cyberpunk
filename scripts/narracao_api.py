#!/usr/bin/env python3
"""
Servidor local para front-end de narracao solo + API de chat.

Delega para FastAPI (uvicorn). Mantido por compatibilidade com scripts e testes legados.

Uso:
  python scripts/narracao_api.py
  python -m api.main

Abre:
  http://127.0.0.1:8787/
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
for path in (_REPO_ROOT, _REPO_ROOT / "scripts"):
    entry = str(path)
    if entry not in sys.path:
        sys.path.insert(0, entry)

from api.main import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())