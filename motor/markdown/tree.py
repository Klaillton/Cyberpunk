from __future__ import annotations

import re


def parse_markdown_heading(line: str) -> tuple[int, str] | None:
    heading_match = re.match(r"^(#{2,6})\s+(.+?)\s*$", line)
    if not heading_match:
        return None
    return len(heading_match.group(1)), heading_match.group(2).strip()


def append_markdown_section(
    stack: list[dict[str, object]], sections: list[dict[str, object]], level: int, title: str
) -> None:
    node: dict[str, object] = {
        "title": title,
        "level": level,
        "content": [],
        "children": [],
    }
    while stack and int(stack[-1]["level"]) >= level:
        stack.pop()
    if stack:
        stack[-1]["children"].append(node)
    else:
        sections.append(node)
    stack.append(node)


def parse_markdown_tree(markdown_text: str) -> dict[str, object]:
    title = ""
    intro_lines: list[str] = []
    sections: list[dict[str, object]] = []
    stack: list[dict[str, object]] = []

    for line in markdown_text.splitlines():
        title_match = re.match(r"^#\s+(.+?)\s*$", line)
        if title_match and not title:
            title = title_match.group(1).strip()
            continue

        heading_info = parse_markdown_heading(line)
        if heading_info:
            append_markdown_section(stack, sections, heading_info[0], heading_info[1])
            continue

        target = stack[-1]["content"] if stack else intro_lines
        target.append(line)

    return {"title": title, "introLines": intro_lines, "sections": sections}


def render_section_tree(nodes: list[dict[str, object]]) -> list[dict[str, object]]:
    rendered: list[dict[str, object]] = []
    for node in nodes:
        rendered.append(
            {
                "title": str(node.get("title", "")).strip(),
                "level": int(node.get("level", 2)),
                "content": "\n".join(str(line) for line in node.get("content", [])).strip(),
                "children": render_section_tree(list(node.get("children", []))),
            }
        )
    return rendered


def extract_references(markdown_text: str, limit: int = 12) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for label, path in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", markdown_text):
        if path.startswith("#"):
            continue
        key = (label.strip(), path.strip())
        if key in seen:
            continue
        seen.add(key)
        refs.append({"label": key[0], "path": key[1]})
        if len(refs) >= limit:
            break
    return refs