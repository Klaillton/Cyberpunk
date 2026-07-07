from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from motor.markdown.tree import parse_markdown_tree, render_section_tree


_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


@dataclass(frozen=True)
class MarkdownSection:
    title: str
    level: int
    content: str
    children: list[MarkdownSection] = field(default_factory=list)


@dataclass(frozen=True)
class MarkdownDocument:
    path: str
    frontmatter: dict[str, Any]
    title: str
    intro_lines: list[str]
    sections: list[MarkdownSection]


def _parse_simple_frontmatter(block: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key:
            continue
        if value.lower() in {"true", "false"}:
            data[key] = value.lower() == "true"
        else:
            data[key] = value
    return data


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    frontmatter = _parse_simple_frontmatter(match.group(1))
    body = text[match.end() :]
    return frontmatter, body


def _to_sections(nodes: list[dict[str, object]]) -> list[MarkdownSection]:
    sections: list[MarkdownSection] = []
    for node in render_section_tree(nodes):
        sections.append(
            MarkdownSection(
                title=str(node.get("title", "")).strip(),
                level=int(node.get("level", 2)),
                content=str(node.get("content", "")).strip(),
                children=_to_sections(list(node.get("children", []))),
            )
        )
    return sections


def parse_markdown_document(path: Path, text: str | None = None) -> MarkdownDocument:
    raw = text if text is not None else path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(raw)
    tree = parse_markdown_tree(body)
    title = str(tree.get("title", "")).strip() or path.stem
    intro = [str(line) for line in tree.get("introLines", [])]
    sections = _to_sections(list(tree.get("sections", [])))
    return MarkdownDocument(
        path=str(path).replace("\\", "/"),
        frontmatter=frontmatter,
        title=title,
        intro_lines=intro,
        sections=sections,
    )


def document_to_json(doc: MarkdownDocument) -> str:
    payload = {
        "path": doc.path,
        "frontmatter": doc.frontmatter,
        "title": doc.title,
    }
    return json.dumps(payload, ensure_ascii=False)