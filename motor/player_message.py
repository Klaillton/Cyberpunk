from __future__ import annotations

import re
from dataclasses import dataclass, field

_TAG_RE = re.compile(
    r"^\[(ação|acao|fala|beat)\]\s*(.*)$",
    re.IGNORECASE,
)
_BEAT_INLINE_RE = re.compile(r"\*([^*]+)\*")
_PREFIX_RE = re.compile(
    r"^\[(?:HISTORIA|HISTÓRIA)\]\s*VOCE:\s*",
    re.IGNORECASE,
)


@dataclass
class ParsedPlayerMessage:
    raw: str
    actions: list[str] = field(default_factory=list)
    speeches: list[str] = field(default_factory=list)
    beats: list[str] = field(default_factory=list)

    @property
    def has_structure(self) -> bool:
        return bool(self.actions or self.speeches or self.beats)


def _strip_player_prefix(text: str) -> str:
    cleaned = text.strip()
    cleaned = _PREFIX_RE.sub("", cleaned)
    cleaned = re.sub(r"^VOCE:\s*", "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def _normalize_tag(kind: str) -> str:
    lowered = kind.lower().replace("á", "a").replace("ã", "a")
    if lowered == "acao":
        return "action"
    if lowered == "fala":
        return "speech"
    if lowered == "beat":
        return "beat"
    return "action"


def _parse_underscore_line(line: str) -> tuple[list[str], list[str], list[str]]:
    speeches: list[str] = []
    beats: list[str] = []
    rest = line.lstrip("_").strip()
    for beat in _BEAT_INLINE_RE.findall(rest):
        token = beat.strip()
        if token:
            beats.append(token)
    speech = _BEAT_INLINE_RE.sub("", rest).strip()
    speech = speech.strip('"').strip()
    if speech:
        speeches.append(speech)
    return [], speeches, beats


def _classify_line(line: str) -> tuple[str, list[str], list[str], list[str]]:
    stripped = line.strip()
    if not stripped:
        return "skip", [], [], []

    tag_match = _TAG_RE.match(stripped)
    if tag_match:
        kind = _normalize_tag(tag_match.group(1))
        content = tag_match.group(2).strip().strip('"')
        if not content:
            return "skip", [], [], []
        if kind == "action":
            return kind, [content], [], []
        if kind == "speech":
            return kind, [], [content], []
        return kind, [], [], [content]

    if stripped.startswith("_"):
        actions, speeches, beats = _parse_underscore_line(stripped)
        return "mixed", actions, speeches, beats

    if re.fullmatch(r'"[^"]+"', stripped):
        return "speech", [], [stripped.strip('"')], []

    if re.fullmatch(r"\*[^*]+\*", stripped):
        return "beat", [], [], [stripped.strip("*").strip()]

    beats = [token.strip() for token in _BEAT_INLINE_RE.findall(stripped) if token.strip()]
    remainder = _BEAT_INLINE_RE.sub("", stripped).strip()
    speeches: list[str] = []
    actions: list[str] = []
    if remainder:
        quoted = re.findall(r'"([^"]+)"', remainder)
        if quoted:
            speeches.extend(item.strip() for item in quoted if item.strip())
            remainder = re.sub(r'"[^"]+"', "", remainder).strip(" ,.;")
        if remainder:
            actions.append(remainder)

    if speeches or beats:
        return "mixed", actions, speeches, beats
    return "action", [stripped], [], []


def parse_player_message(raw: str) -> ParsedPlayerMessage:
    text = _strip_player_prefix(raw)
    parsed = ParsedPlayerMessage(raw=raw)

    for line in text.splitlines():
        _kind, actions, speeches, beats = _classify_line(line)
        parsed.actions.extend(actions)
        parsed.speeches.extend(speeches)
        parsed.beats.extend(beats)

    if not parsed.has_structure and text:
        parsed.actions.append(text)

    return parsed


def format_player_message_for_prompt(parsed: ParsedPlayerMessage) -> str:
    parts: list[str] = [
        "O jogador separou acao, fala e beats. Tudo abaixo JA aconteceu — narre apenas o que vem DEPOIS.",
        "Nao repita frases do jogador. Falas entre aspas ja foram ditas em voz alta.",
    ]
    if parsed.actions:
        parts.append("")
        parts.append("### Acoes (executadas)")
        parts.extend(f"- {item}" for item in parsed.actions)
    if parsed.speeches:
        parts.append("")
        parts.append("### Falas (ja ditas — reacao de NPCs, sem ecoar)")
        parts.extend(f'- "{item}"' for item in parsed.speeches)
    if parsed.beats:
        parts.append("")
        parts.append("### Beats (gesto/tom)")
        parts.extend(f"- *{item}*" for item in parsed.beats)
    if not parsed.has_structure:
        parts.append("")
        parts.append(f"### Entrada bruta\n- {parsed.raw.strip()}")
    return "\n".join(parts)