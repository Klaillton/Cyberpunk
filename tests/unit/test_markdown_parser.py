from __future__ import annotations

from motor.markdown.chunker import chunk_document
from motor.markdown.parser import parse_markdown_document


SAMPLE = """---
id: lena_valk_kane
type: npc
---

# Lena "Valk" Kane

Intro curta sobre a piloto.

## Background

Motorista estoica do Pack Badlands.

## Estado Atual

| Campo | Valor |
| ----- | ----- |
| Humor | Focada |
"""


def test_parse_frontmatter_and_sections() -> None:
    doc = parse_markdown_document(path=__import__("pathlib").Path("fichas/nomad - lena_valk_kane.md"), text=SAMPLE)
    assert doc.frontmatter["id"] == "lena_valk_kane"
    assert doc.title == 'Lena "Valk" Kane'
    assert len(doc.sections) >= 2
    titles = [section.title for section in doc.sections]
    assert "Background" in titles
    assert "Estado Atual" in titles


def test_chunk_document_splits_sections() -> None:
    doc = parse_markdown_document(path=__import__("pathlib").Path("sample.md"), text=SAMPLE)
    chunks = chunk_document(doc)
    assert chunks
    assert any("Motorista estoica" in chunk.text for chunk in chunks)