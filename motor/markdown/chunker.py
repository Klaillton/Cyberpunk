from __future__ import annotations

from dataclasses import dataclass

from motor.markdown.parser import MarkdownDocument, MarkdownSection

MAX_CHUNK_CHARS = 1500
OVERLAP_CHARS = 100


@dataclass(frozen=True)
class TextChunk:
    section: str | None
    chunk_index: int
    text: str


def _split_long_text(section_title: str | None, text: str, start_index: int) -> list[TextChunk]:
    if len(text) <= MAX_CHUNK_CHARS:
        return [TextChunk(section=section_title, chunk_index=start_index, text=text)]

    chunks: list[TextChunk] = []
    start = 0
    index = start_index
    while start < len(text):
        end = min(start + MAX_CHUNK_CHARS, len(text))
        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks.append(TextChunk(section=section_title, chunk_index=index, text=chunk_text))
            index += 1
        if end >= len(text):
            break
        start = max(end - OVERLAP_CHARS, start + 1)
    return chunks


def _flatten_sections(sections: list[MarkdownSection]) -> list[tuple[str | None, str]]:
    pairs: list[tuple[str | None, str]] = []
    for section in sections:
        content = section.content.strip()
        if content:
            pairs.append((section.title or None, content))
        for child_title, child_text in _flatten_sections(section.children):
            pairs.append((child_title, child_text))
    return pairs


def chunk_document(doc: MarkdownDocument) -> list[TextChunk]:
    chunks: list[TextChunk] = []
    index = 0

    intro = "\n".join(doc.intro_lines).strip()
    if intro:
        chunks.extend(_split_long_text(doc.title or None, intro, index))
        index = chunks[-1].chunk_index + 1 if chunks else 0

    for section_title, section_text in _flatten_sections(doc.sections):
        section_chunks = _split_long_text(section_title, section_text, index)
        chunks.extend(section_chunks)
        if section_chunks:
            index = section_chunks[-1].chunk_index + 1

    if not chunks and doc.title:
        chunks.append(TextChunk(section=None, chunk_index=0, text=doc.title))

    return chunks