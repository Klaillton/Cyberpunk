from __future__ import annotations

import re
from pathlib import Path
from motor.markdown.parser import parse_markdown_document
from motor.markdown.campaign_paths import is_campaign_content_path
from motor.npc import build_npc_asset_response, find_sheet_by_name, normalize_name
from motor.settings import Settings, get_settings


def _campaign_path(settings: Settings, rel_path: str) -> Path:
    return settings.campanha_root / rel_path


def _read_text(settings: Settings, rel_path: str) -> str:
    path = _campaign_path(settings, rel_path)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _parse_board_npcs(board_text: str) -> list[dict[str, str]]:
    section_match = re.search(
        r"^##\s+NPCs Importantes\s*\n(.*?)(?=^##\s+|\Z)",
        board_text,
        re.MULTILINE | re.DOTALL,
    )
    if not section_match:
        return []

    rows: list[dict[str, str]] = []
    lines = section_match.group(1).splitlines()
    for line in lines:
        if not line.startswith("|") or "---" in line or "Nome" in line:
            continue
        cols = [re.sub(r"\*\*", "", col).strip() for col in line.strip("|").split("|")]
        if len(cols) < 4:
            continue
        name, role, relation, notes = cols[0], cols[1], cols[2], cols[3]
        if not name or name.lower() == "nome":
            continue
        rows.append(
            {
                "name": name,
                "role": role,
                "relation": relation,
                "notes": notes,
                "source": "board",
            }
        )
    return rows


def _infer_gender(text: str, name: str) -> str:
    lowered = text.lower()
    if any(token in lowered for token in (" ela ", " mulher", " feminin", " parceira ")):
        return "female"
    if "lena" in name.lower() or "valk" in name.lower() or "mara" in name.lower():
        return "female"
    if "sasha" in name.lower() or "lira" in name.lower() or "lina" in name.lower():
        return "female"
    return "male"


def _npc_summary_from_sheet(sheet_path: Path) -> str:
    if not sheet_path.exists():
        return ""
    doc = parse_markdown_document(sheet_path)
    for section in doc.sections:
        title = section.title.lower()
        if title in {"personalidade", "resumo", "background", "aparência / voz (rápido)", "aparencia / voz (rapido)"}:
            bullets = [line[2:].strip() for line in section.content.splitlines() if line.strip().startswith("- ")]
            if bullets:
                return bullets[0]
            lines = [line.strip() for line in section.content.splitlines() if line.strip() and not line.startswith("|")]
            if lines:
                return lines[0]
    intro = " ".join(line.strip() for line in doc.intro_lines if line.strip())
    return intro[:220] + ("…" if len(intro) > 220 else "")


def _name_lookup_variants(name: str) -> list[str]:
    variants: list[str] = []
    seen: set[str] = set()

    def add(value: str) -> None:
        cleaned = re.sub(r"\s+", " ", value.strip())
        if not cleaned:
            return
        key = cleaned.lower()
        if key in seen:
            return
        seen.add(key)
        variants.append(cleaned)

    add(name)
    add(re.sub(r'"[^"]+"', " ", name))
    add(re.sub(r"'[^']+'", " ", name))

    lowered = name.lower()
    if "valk" in lowered or "lena" in lowered:
        add('Lena "Valk" Kane')
        add("lena valk kane")
    if "reyes" in lowered:
        add("reyes")
    if "gringo" in lowered:
        add("tio gringo")

    return variants


def _resolve_sheet_path(settings: Settings, name: str, board_notes: str = "") -> Path | None:
    link_match = re.search(r"\(([^)]+\.md)\)", board_notes)
    if link_match:
        rel = link_match.group(1).replace("../", "").replace("../../", "")
        if is_campaign_content_path(rel):
            candidate = settings.campanha_root / rel
            if candidate.exists():
                return candidate

    for variant in _name_lookup_variants(name):
        sheet = find_sheet_by_name(variant, settings)
        if sheet is not None and sheet.exists():
            return sheet
    return None


def build_npc_catalog(settings: Settings | None = None) -> dict:
    cfg = settings or get_settings()
    board = _read_text(cfg, "board/board_campanha.md")
    board_npcs = _parse_board_npcs(board)
    seen: set[str] = set()
    catalog: list[dict] = []

    for entry in board_npcs:
        name = entry["name"]
        key = normalize_name(name)
        if key in seen:
            continue
        seen.add(key)

        sheet_path = _resolve_sheet_path(cfg, name, entry.get("notes", ""))
        sheet_rel = ""
        summary = entry.get("notes", "")
        if sheet_path and sheet_path.exists():
            sheet_rel = str(sheet_path.relative_to(cfg.campanha_root)).replace("\\", "/")
            sheet_summary = _npc_summary_from_sheet(sheet_path)
            if sheet_summary:
                summary = sheet_summary

        gender = _infer_gender(summary + " " + entry.get("role", ""), name)
        assets = build_npc_asset_response(name, gender, cfg)

        catalog.append(
            {
                "id": key,
                "name": name,
                "role": entry.get("role", ""),
                "relation": entry.get("relation", ""),
                "summary": summary,
                "gender": gender,
                "sheetPath": sheet_rel,
                "imageUrl": assets["imageUrl"],
                "tokenUrl": assets["tokenUrl"],
                "hasImage": assets["hasImage"],
                "hasSheet": bool(sheet_rel),
                "featured": True,
            }
        )

    npc_dir = cfg.campanha_root / "fichas" / "npc"
    if npc_dir.exists():
        for path in sorted(npc_dir.glob("*.md")):
            rel = path.relative_to(cfg.campanha_root).as_posix()
            if not is_campaign_content_path(rel):
                continue
            doc = parse_markdown_document(path)
            display_name = doc.title.split("—")[0].strip() if "—" in doc.title else doc.title
            key = normalize_name(display_name)
            if key in seen:
                continue
            seen.add(key)
            summary = _npc_summary_from_sheet(path)
            gender = _infer_gender(summary, display_name)
            assets = build_npc_asset_response(display_name, gender, cfg)
            catalog.append(
                {
                    "id": key,
                    "name": display_name,
                    "role": "",
                    "relation": "",
                    "summary": summary,
                    "gender": gender,
                    "sheetPath": str(path.relative_to(cfg.campanha_root)).replace("\\", "/"),
                    "imageUrl": assets["imageUrl"],
                    "tokenUrl": assets["tokenUrl"],
                    "hasImage": assets["hasImage"],
                    "hasSheet": True,
                    "featured": False,
                }
            )

    catalog.sort(key=lambda item: (not item["featured"], item["name"].lower()))
    return {
        "count": len(catalog),
        "npcs": catalog,
        "sources": ["board/board_campanha.md", "fichas/", "relacionamentos/mapa_relacional_geral.md"],
    }