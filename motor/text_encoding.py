from __future__ import annotations

_MOJIBAKE_MARKERS = ("Ã", "â€", "â€™", "â€œ", "â€")


def repair_mojibake(text: str) -> str:
    """Recover UTF-8 text that was decoded as Latin-1/CP1252 (common on Windows)."""
    if not text or not any(marker in text for marker in _MOJIBAKE_MARKERS):
        return text
    for encoding in ("cp1252", "latin-1"):
        try:
            return text.encode(encoding).decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
    return text