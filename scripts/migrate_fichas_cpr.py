#!/usr/bin/env python3
"""Adiciona frontmatter CPR às fichas conhecidas e semeia roster do Pack."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from motor.character_creation.faction_roster import seed_faction_roster
from motor.character_creation.persistence import append_frontmatter
from motor.character_creation.tiers import TIER_BY_SLUG
from motor.settings import get_settings

MIGRATION_MAP = {
    "fichas/techie - ryan_wireghost_voss.md": {"role": "tech"},
    "fichas/nomad - lena_valk_kane.md": {"role": "nomad"},
    "fichas/solo - jax_razor_kane.md": {"role": "solo"},
    "fichas/fixer - kaz_the_broker_takahashi.md": {"role": "fixer"},
    "fichas/medtech - stephania_doc_voss.md": {"role": "medtech"},
    "fichas/solo - reina_bearclaw_morales.md": {"role": "solo"},
    "fichas/netrunner - alex_specter_kane.md": {"role": "netrunner"},
    "fichas/npc/reyes.md": {"role": "npc", "faction": "pack_badlands", "faction_role": "leader"},
    "fichas/npc/tio_gringo.md": {"role": "npc", "faction": "pack_badlands", "faction_role": "smith"},
    "fichas/npc/lira.md": {"role": "npc", "faction": "pack_badlands"},
    "fichas/npc/mara_recruit.md": {"role": "npc", "faction": "pack_badlands"},
    "fichas/npc/elias_recruit.md": {"role": "npc", "faction": "pack_badlands"},
    "fichas/npc/tomas_recruit.md": {"role": "npc", "faction": "pack_badlands"},
    "fichas/npc/sasha.md": {"role": "npc", "faction": "pack_badlands"},
}


def main() -> int:
    settings = get_settings()
    root = settings.campanha_root
    backup = root / "fichas" / "_backup_pre_cpr"
    backup.mkdir(parents=True, exist_ok=True)

    for rel, extra in MIGRATION_MAP.items():
        path = root / rel
        if not path.exists():
            print(f"skip missing {rel}")
            continue
        slug = path.stem.split(" - ", 1)[-1] if " - " in path.stem else path.stem
        tier = TIER_BY_SLUG.get(slug, "npc_reference")
        meta = {
            "id": slug,
            "type": "character" if tier in {"protagonist", "crew_full"} else "npc",
            "tier": tier,
            **{k: str(v) for k, v in extra.items()},
        }
        shutil.copy2(path, backup / path.name)
        append_frontmatter(path, meta)
        print(f"ok {rel} -> tier={tier}")

    result = seed_faction_roster("pack_badlands", settings=settings)
    print(f"roster created={result.created} skipped={result.skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())