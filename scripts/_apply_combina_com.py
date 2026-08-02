# -*- coding: utf-8 -*-
"""Propaga **Combina com (sugestão):** em todas as fichas do crew_guarda_roupas.md."""
from __future__ import annotations

import re
from pathlib import Path

MD = Path(r"C:\workspace\Cyberpunk\fichas\crew_guarda_roupas.md")

OVERRIDES: dict[str, str] = {
    "club_black_leather_harness_mini.png": "Alex",
    "evening_pink_nightgown_cape.jpg": "Reina",
    "evening_black_star_gown.jpg": "Reina",
    "sleep_star_sweater_set.png": "qualquer",
    "intimate_burgundy_lace_set.jpg": "Valk / intimidade",
    "fantasy_white_red_rose_gown.jpg": "Reina",
    "fantasy_winter_blue_cape.jpg": "Reina / fantasia",
    "evening_white_feather_gown.jpg": "Reina",
    # ex-ref_pool
    "formal_white_shirt_black_pants.jpg": "Valk / qualquer",
    "intimate_white_tee_panties.jpg": "Valk / intimidade",
    "formal_black_blazer_mini.jpg": "Alex",
    "intimate_black_sheer_babydoll_ref.jpg": "Valk / intimidade",
    "evening_black_mermaid_glitter.jpg": "Reina",
    "sleep_plush_onesie_panda.jpg": "qualquer",
    "evening_black_cape_corset.jpg": "Reina / Alex",
    "sleep_pink_lace_robe_set.jpg": "Reina / Valk",
    "formal_black_suit_red_tie_power.jpg": "Alex",
    "special_black_harness_bodysuit.jpg": "Alex / cena especial",
    "sleep_white_floral_cami_set.jpg": "Valk / qualquer",
}


def vibe_for(filename: str) -> str:
    if filename in OVERRIDES:
        return OVERRIDES[filename]
    f = filename.lower()
    if f.startswith("intimate_") or "babydoll" in f or "sheer_robe" in f or "panties" in f:
        return "Valk / intimidade"
    if f.startswith("sleep_") or f.startswith("lounge_"):
        if any(x in f for x in ("sheer", "slip", "lace_slip", "cami", "lingerie")):
            return "Valk / intimidade"
        return "qualquer"
    if f.startswith("club_") or "latex" in f:
        return "Alex"
    if f.startswith("evening_") or f.startswith("fantasy_"):
        return "Reina"
    if f.startswith("formal_"):
        if "harness" in f or "leather" in f or "tie" in f or "suit" in f or "pantsuit" in f:
            return "Alex"
        return "qualquer"
    if f.startswith("medical_") or "nurse" in f or "scrubs" in f:
        return "Stitch / qualquer"
    if f.startswith("tech_") or f.startswith("media_"):
        return "Echo / qualquer"
    if f.startswith("badlands_") or f.startswith("combat_") or f.startswith("stealth_"):
        return "Valk / Alex / pack"
    if f.startswith("soft_"):
        return "Reina / qualquer"
    if f.startswith("gym_") or f.startswith("training_"):
        return "qualquer"
    if f.startswith("street_"):
        if any(x in f for x in ("mini", "leather", "micro", "corset", "allblack")):
            return "Alex / Valk"
        return "qualquer"
    if f.startswith("special_"):
        return "cena especial"
    if f.startswith("piece_"):
        return "qualquer"
    if f.startswith("swim_"):
        return "qualquer"
    if f.startswith("utility_") or "romper" in f:
        return "Valk / pack"
    return "qualquer"


HEADER_NOTE = """
**Combina com (sugestão):** vibe de personalidade/cena — **não** é obrigatório e **não** é default de personagem. Quem veste o look é decisão da **cena / ficha**.

- `intimate_*` e nightwear ousado: ok para intimidade (ex. Ryan/Valk) e para qualquer outra se a cena pedir.
- Club/formal ousado: costuma combinar com **Alex**; gala/soft com **Reina**; utilitário/pack com **Valk** — sempre opcional.
"""


def main() -> None:
    text = MD.read_text(encoding="utf-8")

    # Fix common mojibake if present
    fixes = {
        "suti�": "sutiã",
        "�ntimo": "íntimo",
        "p�s-banho": "pós-banho",
        "�": "ã",  # careful - too broad? skip generic
        "Combina com (sugest�o)": "Combina com (sugestão)",
        "n�o": "não",
        "personagem.": "personagem.",
    }
    for a, b in fixes.items():
        if a != "�":
            text = text.replace(a, b)

    # Insert canonical note after first --- following intro, or after focus block
    if "**Combina com (sugestão):** vibe de personalidade" not in text:
        # after acessórios paragraph
        anchor = "**Peças incompletas:**"
        if anchor in text:
            text = text.replace(
                anchor,
                HEADER_NOTE.strip() + "\n\n" + anchor,
                1,
            )

    # Process each **Arquivo:** block
    # Pattern: **Arquivo:** `file` then optional Nome rápido lines, maybe Combina
    pattern = re.compile(
        r"(\*\*Arquivo:\*\*\s*`([^`]+)`\s*\n)"
        r"((?:\*\*Nome rápido:\*\*[^\n]*\n)*)"
        r"((?:\*\*Categoria:\*\*[^\n]*\n)*)"
        r"((?:\*\*Combina com[^\n]*\n)*)",
        re.MULTILINE,
    )

    def repl(m: re.Match) -> str:
        arquivo_line = m.group(1)
        fname = m.group(2)
        nome = m.group(3) or ""
        cat = m.group(4) or ""
        # drop old combina
        vibe = vibe_for(fname)
        combina = f"**Combina com (sugestão):** {vibe}  \n"
        return f"{arquivo_line}{nome}{cat}{combina}"

    new_text, n = pattern.subn(repl, text)
    print(f"Updated/inserted Combina com on {n} Arquivo blocks")

    # Notas de narração — ensure bullet
    note_bullet = (
        "12. **Combina com (sugestão)** em cada look é só vibe de personalidade/cena — "
        "**nunca** trava personagem. `intimate_*` serve intimidade (Ryan/Valk etc.) sem excluir outras."
    )
    if "Combina com (sugestão)** em cada look" not in new_text:
        if "## Notas de narração" in new_text:
            # append before end of file after notes section - find last numbered note
            if "11. Scrubs:" in new_text:
                new_text = new_text.replace(
                    "11. Scrubs:",
                    "11. Scrubs:",
                )
            # add after note 11 block - simpler append to notes
            m = re.search(
                r"(## Notas de narração\n(?:.*\n)*?)(\n# |\Z)",
                new_text,
                re.MULTILINE,
            )
            if m:
                block = m.group(1)
                if note_bullet not in block:
                    new_text = (
                        new_text[: m.start(1)]
                        + block.rstrip()
                        + "\n"
                        + note_bullet
                        + "\n"
                        + new_text[m.end(1) :]
                    )

    MD.write_text(new_text, encoding="utf-8")
    print("Wrote", MD)


if __name__ == "__main__":
    main()
