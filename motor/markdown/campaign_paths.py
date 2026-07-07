from __future__ import annotations

from pathlib import Path

CAMPAIGN_GLOBS = (
    "fichas/**/*.md",
    "board/**/*.md",
    "relacionamentos/**/*.md",
    "facoes/**/*.md",
    "pulso_do_mundo/**/*.md",
    "consequencias/**/*.md",
    "logs/*.md",
    "heat.md",
    "economia.md",
    "reputacao.md",
    "event_queue.md",
)

EXCLUDE_SUBSTRINGS = (
    "template",
    "notas_narrador",
    "/projeto/",
    "/sistema/",
    "/scripts/",
    "/tests/",
)


def should_index_markdown(rel_path: str) -> bool:
    normalized = rel_path.replace("\\", "/").lower()
    if normalized.endswith("readme.md"):
        return False
    return not any(token in normalized for token in EXCLUDE_SUBSTRINGS)


def discover_campaign_files(root: Path) -> list[Path]:
    files: list[Path] = []
    seen: set[str] = set()
    for pattern in CAMPAIGN_GLOBS:
        for path in sorted(root.glob(pattern)):
            if not path.is_file():
                continue
            rel = path.relative_to(root).as_posix()
            if not should_index_markdown(rel):
                continue
            if rel in seen:
                continue
            seen.add(rel)
            files.append(path)
    return files


def infer_doc_type(rel_path: str) -> str:
    normalized = rel_path.replace("\\", "/").lower()
    if "/npc/" in normalized or normalized.startswith("fichas/npc/"):
        return "npc"
    if normalized.startswith("relacionamentos/"):
        return "relationship"
    if normalized.startswith("board/"):
        return "state"
    if normalized.startswith("facoes/"):
        return "faction"
    if normalized.startswith("pulso_do_mundo/"):
        return "pulse"
    if normalized.startswith("consequencias/"):
        return "consequence"
    if normalized.startswith("logs/"):
        return "log"
    if normalized.startswith("fichas/"):
        if "vehicle" in normalized:
            return "vehicle"
        return "character"
    if normalized in {"heat.md", "economia.md", "reputacao.md", "event_queue.md"}:
        return "state"
    return "document"


def entity_id_from_path(rel_path: str, title: str, frontmatter: dict) -> str | None:
    if frontmatter.get("id"):
        return str(frontmatter["id"]).strip()

    stem = Path(rel_path).stem
    if " - " in stem:
        return stem.split(" - ", 1)[1].strip().replace(" ", "_").lower()

    clean = stem.replace(" ", "_").lower()
    if clean.endswith("_relacionamentos"):
        return clean.removesuffix("_relacionamentos")
    return clean


def extract_aliases(title: str, entity_id: str | None) -> list[str]:
    import re

    aliases: list[str] = []
    seen: set[str] = set()

    def add(value: str) -> None:
        clean = value.strip()
        if len(clean) < 2:
            return
        key = clean.lower()
        if key in seen:
            return
        seen.add(key)
        aliases.append(clean)

    for match in re.finditer(r"[\"“]([^\"”]+)[\"”]", title):
        add(match.group(1))

    if entity_id:
        for part in entity_id.split("_"):
            if len(part) >= 3:
                add(part)

    return aliases