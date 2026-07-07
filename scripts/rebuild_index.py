#!/usr/bin/env python3
"""Reconstrói SQLite + FAISS a partir dos Markdown da campanha."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
for entry in (str(_REPO_ROOT), str(_REPO_ROOT / "scripts")):
    if entry not in sys.path:
        sys.path.insert(0, entry)

from motor.index.faiss_index import FaissIndex  # noqa: E402
from motor.markdown.sync_engine import SyncEngine  # noqa: E402
from motor.settings import get_settings  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild SQLite + FAISS index")
    parser.add_argument("--campanha-root", type=Path, default=None, help="Raiz dos arquivos Markdown")
    args = parser.parse_args()

    settings = get_settings()
    if args.campanha_root:
        settings.campanha_root = args.campanha_root.resolve()

    sync = SyncEngine(settings)
    report = sync.full_sync()
    vectors = FaissIndex(settings).rebuild()

    print(
        "Index rebuild concluido:",
        f"docs={report.documents_synced}",
        f"chunks={report.chunks_written}",
        f"aliases={report.aliases_written}",
        f"removed={report.files_removed}",
        f"vectors={vectors}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())