# -*- coding: utf-8 -*-
"""
Organiza E:\\...\\Women Style em pastas por tipo de roupa.
- usados/ = imagem igual (MD5) a um arquivo do catalogo crew
- skipados/ = nao entrou no catalogo
Nomes legiveis: USADO__nome_catalogo.ext ou SKIP__descricao_ou_hash.ext
"""
from __future__ import annotations

import hashlib
import re
import shutil
from pathlib import Path

WS = Path(r"E:\DataBackup\UsersBackup\Images\Women Style")
CREW = Path(r"C:\workspace\Cyberpunk\imagens\crew\guarda_roupas")

# Tipo <- prefixos / keywords do nome no catalogo
TYPE_RULES: list[tuple[str, str, tuple[str, ...]]] = [
    ("01_sleep_casa", "Sleep / casa / pijama", ("sleep_", "lounge_")),
    ("02_lingerie_intimo", "Lingerie / intimo (look)", ("lingerie", "latex", "special_latex", "special_sheer")),
    ("03_biker_gym", "Biker / gym / treino", ("gym_", "training_", "biker")),
    ("04_bermuda_formal", "Bermuda alfaiataria / formal verao", ("bermuda", "culotte", "wideleg_crop")),
    ("05_short_jeans_casual", "Short jeans / casual", ("casual_", "denim_short", "skort", "overalls")),
    ("06_medical", "Medical / scrubs / jaleco", ("medical_", "scrubs", "nurse", "lab_coat")),
    ("07_macacao_jumpsuit", "Macacao / romper / jumpsuit", ("romper", "jumpsuit", "onesie", "overall")),
    ("08_club_noite", "Club / noite ousada", ("club_",)),
    ("09_evening_gala", "Evening / gala", ("evening_",)),
    ("10_swim", "Swim / praia", ("swim_",)),
    ("11_formal_office", "Formal / office / terno", ("formal_", "media_", "threepiece", "pantsuit")),
    ("12_soft_pack", "Soft / pack / fantasia", ("soft_", "fantasy_", "steampunk", "badlands_floral")),
    ("13_street_nc", "Street / Night City", ("street_", "rain_", "weather_", "tech_")),
    ("14_combate_stealth", "Combate / stealth", ("combat_", "stealth_", "badlands_tactical", "badlands_utility", "badlands_crop", "badlands_casual")),
    ("15_pecas", "Pecas / camadas", ("piece_",)),
    ("16_especial", "Especial / costume", ("special_",)),
]


def md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def classify_crew_name(name: str) -> str:
    n = name.lower()
    for folder, _title, keys in TYPE_RULES:
        for k in keys:
            if k in n:
                return folder
    return "99_outros_catalogados"


def safe_name(s: str) -> str:
    s = s.strip().replace(" ", "_")
    s = re.sub(r"[^\w.\-]+", "_", s, flags=re.UNICODE)
    s = re.sub(r"_+", "_", s)
    return s[:120]


def ensure(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def unique_dest(dest: Path) -> Path:
    if not dest.exists():
        return dest
    stem, suf = dest.stem, dest.suffix
    i = 2
    while True:
        cand = dest.with_name(f"{stem}_{i}{suf}")
        if not cand.exists():
            return cand
        i += 1


def main() -> None:
    if not WS.is_dir():
        raise SystemExit(f"Women Style not found: {WS}")

    # Flatten: if already organized, gather all files first to temp? 
    # Move everything to flat staging first
    staging = WS / "_staging_all"
    if staging.exists():
        shutil.rmtree(staging)
    ensure(staging)

    files = [p for p in WS.rglob("*") if p.is_file() and p.name.lower() != "leia-me.md"]
    # exclude staging while collecting
    files = [p for p in files if "_staging_all" not in p.parts]

    print(f"Found {len(files)} files under Women Style")

    for p in files:
        dest = unique_dest(staging / p.name)
        shutil.move(str(p), str(dest))

    # remove empty dirs except staging
    for d in sorted(WS.rglob("*"), reverse=True):
        if d.is_dir() and d != staging and d != WS:
            try:
                d.rmdir()
            except OSError:
                pass

    # Map MD5 -> crew filename
    crew_by_md5: dict[str, str] = {}
    if CREW.is_dir():
        for p in CREW.iterdir():
            if p.is_file():
                crew_by_md5[md5(p)] = p.name

    print(f"Crew files hashed: {len(crew_by_md5)}")

    # Known skip descriptive renames (partial)
    SKIP_NAMES: dict[str, tuple[str, str]] = {
        # filename lower -> (folder, nice_name)
        "download (1).png": ("02_lingerie_intimo", "so_sutia_e_calcinha_branca"),
        "download (1)_crew.png": ("02_lingerie_intimo", "so_sutia_e_calcinha_branca"),
        "download (1)_from_crew.png": ("02_lingerie_intimo", "so_sutia_e_calcinha_branca"),
        "download (2).png": ("02_lingerie_intimo", "camisa_crop_e_calcinha"),
        "download (2)_crew.png": ("02_lingerie_intimo", "camisa_crop_e_calcinha"),
        "3e768a051e749e44d020bebcaf65fe0b.jpg": ("02_lingerie_intimo", "micro_bikini_preto"),
        "7a5e8b532d1bbbad6bb8f4daae2b1efb.jpg": ("02_lingerie_intimo", "sling_monokini_vaca"),
        "4e9588b1c661a1364d202fbdb3f6d4f8.jpg": ("03_biker_gym", "so_biker_short_preto"),
        "514d627ab74ab88d9d9b5a422c6acb7b.jpg": ("03_biker_gym", "so_biker_short_tiedye"),
        "d0bd71f35b670c2d080396e8c992f231.jpg": ("09_evening_gala", "chart_10_dress_styles"),
        "4d28573af2aba87097fc68100ca253e2.jpg": ("99_outros_skip", "armadura_mecha"),
        "d36bdfd62ee6e5884e9b2cc5f9515e68.jpg": ("99_outros_skip", "armadura_robo"),
        "146c7604f2f55d85fb402a084df67c23.jpg": ("09_evening_gala", "gown_bola_azul_branco"),
        "e4a059789c4242c0e55966da5feda4f5.jpg": ("09_evening_gala", "gown_rosa_fantasia_sheet"),
        "2911a07ab57bd304f339f19238642e0d.jpg": ("09_evening_gala", "gown_fogo_dourado_sheet"),
        "874333017ea48a4f1e0d155b0ad0a4f8.jpg": ("99_outros_skip", "cargo_verde_calca"),
        "c96ca04886decf47c117d1f782bde5f6.jpg": ("99_outros_skip", "cargo_preto_jaqueta_branca"),
        "0ddba6d25fcbdcf4853d3b5efa49109c.jpg": ("99_outros_skip", "cargo_branco_calca"),
        "faab6ce4473e5276247eade958c56192.jpg": ("99_outros_skip", "cargo_oliva_tatico"),
        "videoframe_1322.png": ("99_outros_skip", "calca_steampunk_videoframe"),
        "download (4).png": ("09_evening_gala", "portrait_gown_branco_incompleto"),
        "download (3).png": ("09_evening_gala", "gown_branco_capuz"),  # may have been used - md5 wins
    }

    stats: dict[str, dict[str, int]] = {}
    titles = {f: t for f, t, _ in TYPE_RULES}
    titles["99_outros_catalogados"] = "Outros (no catalogo, tipo misto)"
    titles["99_outros_skip"] = "Outros skipados (armadura, cargo repetido, etc.)"

    for p in list(staging.iterdir()):
        if not p.is_file():
            continue
        digest = md5(p)
        ext = p.suffix.lower() or ".jpg"
        base_lower = p.name.lower()

        if digest in crew_by_md5:
            crew_name = crew_by_md5[digest]
            folder = classify_crew_name(crew_name)
            dest_dir = WS / folder / "usados"
            ensure(dest_dir)
            new_name = f"USADO__{safe_name(Path(crew_name).stem)}{Path(crew_name).suffix}"
            dest = unique_dest(dest_dir / new_name)
            shutil.move(str(p), str(dest))
            stats.setdefault(folder, {"usados": 0, "skipados": 0})
            stats[folder]["usados"] += 1
            continue

        # skip path
        if base_lower in SKIP_NAMES:
            folder, nice = SKIP_NAMES[base_lower]
        else:
            # heuristic by keywords in original name
            folder, nice = "99_outros_skip", Path(p.name).stem[:40]
            if "download" in base_lower:
                nice = safe_name(Path(p.name).stem)

        dest_dir = WS / folder / "skipados"
        ensure(dest_dir)
        new_name = f"SKIP__{safe_name(nice)}{ext}"
        dest = unique_dest(dest_dir / new_name)
        shutil.move(str(p), str(dest))
        stats.setdefault(folder, {"usados": 0, "skipados": 0})
        stats[folder]["skipados"] += 1

    # remove staging
    try:
        staging.rmdir()
    except OSError:
        # leftover?
        for p in staging.rglob("*"):
            if p.is_file():
                dest = unique_dest(WS / "99_outros_skip" / "skipados" / f"SKIP__resto_{p.name}")
                ensure(dest.parent)
                shutil.move(str(p), str(dest))
        shutil.rmtree(staging, ignore_errors=True)

    # LEIA-ME root + per type
    root_lines = [
        "# Women Style — organizado por tipo de roupa",
        "",
        "Pool de referencia. O catalogo da campanha fica em:",
        "`Cyberpunk/imagens/crew/guarda_roupas/` + `fichas/crew_guarda_roupas.md`.",
        "",
        "## Como ler",
        "",
        "| Pasta | Significado |",
        "| ----- | ----------- |",
        "| `NN_tipo/usados/` | Mesma imagem (MD5) que ja esta no catalogo; nome = slot do catalogo |",
        "| `NN_tipo/skipados/` | Nao entrou no catalogo (incompleto, redundante, armadura, etc.) |",
        "",
        "Prefixos nos arquivos:",
        "- `USADO__` + nome do look no catalogo",
        "- `SKIP__` + descricao curta",
        "",
        "## Tipos e contagem",
        "",
    ]

    for folder in sorted(stats.keys()):
        u = stats[folder]["usados"]
        s = stats[folder]["skipados"]
        title = titles.get(folder, folder)
        root_lines.append(f"- **{folder}** — {title}: usados={u}, skipados={s}")
        # per-folder readme
        d = WS / folder
        ensure(d)
        ensure(d / "usados")
        ensure(d / "skipados")
        (d / "LEIA-ME.md").write_text(
            "\n".join(
                [
                    f"# {title}",
                    "",
                    f"Pasta: `{folder}`",
                    "",
                    f"- **usados/**: {u} (iguais ao catalogo crew)",
                    f"- **skipados/**: {s} (fora do catalogo)",
                    "",
                    "## Criterio",
                    "",
                    "- Usado = MD5 identico a arquivo em `guarda_roupas/`.",
                    "- Skipado = resto do pool neste tipo (ou classificado a mao).",
                    "",
                    "Lingerie: keep = look narravel (cami+short, robe+set).",
                    "Skip lingerie = so sutiã/calcinha soltos.",
                    "Sleep: keep = pijama/robe/onesie completo.",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    root_lines += [
        "",
        "## Criterio resumido",
        "",
        "- **Keep / usado**: look de cena (2+ pecas ou onesie/macacao completo).",
        "- **Skip lingerie**: underwear solto (sutia+fio, monokini extremo).",
        "- **Skip geral**: armadura, chart multi-look, calca cargo repetida.",
        "",
    ]
    (WS / "LEIA-ME.md").write_text("\n".join(root_lines) + "\n", encoding="utf-8")

    print("Done. Stats:")
    for k in sorted(stats.keys()):
        print(f"  {k}: usados={stats[k]['usados']} skipados={stats[k]['skipados']}")
    total_u = sum(v["usados"] for v in stats.values())
    total_s = sum(v["skipados"] for v in stats.values())
    print(f"TOTAL usados={total_u} skipados={total_s}")


if __name__ == "__main__":
    main()
