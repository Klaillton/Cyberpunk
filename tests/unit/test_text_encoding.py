from __future__ import annotations

from motor.text_encoding import repair_mojibake


def test_repair_mojibake_fixes_utf8_decoded_as_latin1() -> None:
    broken = "O rÃ¡dio chiou e o habitÃ¡culo vibrou â€” sÃ³ vento."
    fixed = repair_mojibake(broken)
    assert "rádio" in fixed
    assert "habitáculo" in fixed
    assert "só" in fixed
    assert "—" in fixed or "-" in fixed


def test_repair_mojibake_leaves_clean_text_untouched() -> None:
    clean = "O rádio chiou e o habitáculo vibrou — só vento."
    assert repair_mojibake(clean) == clean