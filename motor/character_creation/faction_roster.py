from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import json

from motor.character_creation.persistence import append_frontmatter
from motor.settings import Settings, get_settings


@dataclass
class RosterSeedResult:
    faction_id: str
    created: list[str]
    skipped: list[str]


def _load_roster(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def roster_template_path(faction_id: str, settings: Settings | None = None) -> Path:
    cfg = settings or get_settings()
    return cfg.repo_root / "data" / "factions" / f"{faction_id}_roster.json"


def seed_faction_roster(
    faction_id: str,
    *,
    settings: Settings | None = None,
    dry_run: bool = False,
) -> RosterSeedResult:
    cfg = settings or get_settings()
    template_path = roster_template_path(faction_id, cfg)
    if not template_path.exists():
        raise FileNotFoundError(f"Roster nao encontrado: {template_path}")

    payload = _load_roster(template_path)
    default_tier = str(payload.get("default_tier", "npc_reference"))
    created: list[str] = []
    skipped: list[str] = []

    for role in payload.get("roles", []):
        npc_id = str(role.get("default_npc") or "").strip().lower()
        sheet_rel = str(role.get("sheet_path") or "").strip()
        if not npc_id or not sheet_rel:
            continue
        sheet_path = cfg.campanha_root / sheet_rel
        if sheet_path.exists():
            if not dry_run and not sheet_path.read_text(encoding="utf-8").startswith("---"):
                append_frontmatter(
                    sheet_path,
                    {
                        "id": npc_id,
                        "type": "npc",
                        "tier": default_tier,
                        "faction_role": str(role.get("id", "")),
                    },
                )
            skipped.append(npc_id)
            continue

        if dry_run:
            created.append(npc_id)
            continue

        sheet_path.parent.mkdir(parents=True, exist_ok=True)
        label = str(role.get("label", npc_id))
        content = _default_reference_sheet(npc_id, label, faction_id)
        sheet_path.write_text(content, encoding="utf-8")
        created.append(npc_id)

    return RosterSeedResult(faction_id=faction_id, created=created, skipped=skipped)


def _default_reference_sheet(npc_id: str, label: str, faction_id: str) -> str:
    title = label if label else npc_id.replace("_", " ").title()
    return "\n".join(
        [
            "---",
            f"id: {npc_id}",
            "type: npc",
            "tier: npc_reference",
            f"faction: {faction_id}",
            f"faction_role: {npc_id}",
            "---",
            "",
            f"# {title}",
            "",
            f"**Tipo:** {label}",
            f"**Facção / contexto:** {faction_id}",
            "**Status:** Ativo",
            "",
            "## Personalidade",
            "",
            "- ",
            "",
            "## Aparência / voz (rápido)",
            "",
            "- ",
            "",
            "## Eventos narrativos",
            "",
            "| Data (aprox.) | Evento |",
            "| ------------- | ------ |",
            "|               |        |",
            "",
            "## Relação com a crew",
            "",
            "- **Ryan:**",
            "",
            "## Notas para o narrador",
            "",
            "- ",
            "",
        ]
    )