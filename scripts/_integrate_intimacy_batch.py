# -*- coding: utf-8 -*-
"""Integra lote nightwear/lingerie/formal/ousado no catalogo + move WS skip->usado."""
from __future__ import annotations

import shutil
from pathlib import Path

WS_SKIP = Path(
    r"E:\DataBackup\UsersBackup\Images\Women Style\99_pool_nao_catalogado\skipados"
)
CREW = Path(r"C:\workspace\Cyberpunk\imagens\crew\guarda_roupas")
MD = Path(r"C:\workspace\Cyberpunk\fichas\crew_guarda_roupas.md")

# src filename in skipados -> (crew_name, quick, category, pieces, quando, vibe)
# vibe = soft note only (not default locked)
MAP: dict[str, tuple[str, str, str, str, str, str]] = {
    # Sleep / lounge
    "SKIP__0aefbcca83efbc23790a8c11fe1f4c17.jpg": (
        "sleep_oversized_tee_dress_blue.jpg",
        "Camisetão-vestido azul",
        "sleep",
        "Camiseta oversized azul-acinzentada usada como mini-vestido; bolsos laterais",
        "Casa, safehouse, manhã, intimidade casual",
        "qualquer",
    ),
    "SKIP__0e7627b888f98cfdb90511b6f35d762c.jpg": (
        "sleep_plush_onesie_cow.jpg",
        "Onesie plush vaca",
        "sleep",
        "Onesie/macacão plush P&B com capuz e orelhas",
        "Sleep fofo, humor, downtime pack",
        "qualquer",
    ),
    "SKIP__1bf3e3957bf3a80ffb90fd69e4e48a3d.jpg": (
        "sleep_black_cami_shorts.jpg",
        "Cami + short pretos",
        "sleep",
        "Top cami preto com renda + short combinando",
        "Pijama elegante, intimidade",
        "qualquer / Valk",
    ),
    "SKIP__003bb0a00acd6dc252114933e60f8ad0.jpg": (
        "sleep_white_lace_slip.jpg",
        "Slip branco renda",
        "sleep",
        "Camisola/slip branca com renda e amarração lateral",
        "Sleep ousado-leve, intimidade",
        "Valk",
    ),
    "SKIP__03b06706693d1742088401b1fcb349a7.jpg": (
        "sleep_pink_babydoll_robe.jpg",
        "Babydoll rosa + robe",
        "sleep",
        "Babydoll rosa renda + robe sheer rosa babados",
        "Sleep fashion, intimidade",
        "Reina / Valk",
    ),
    "SKIP__download_3_crew.png": (
        "sleep_black_sheer_babydoll.png",
        "Babydoll sheer preto",
        "sleep",
        "Babydoll preto renda + tule transparente",
        "Intimidade, nightwear ousado",
        "Valk",
    ),
    "SKIP__download_crew.png": (
        "sleep_star_sweater_set.png",
        "Moletom estrela + short",
        "sleep",
        "Moletom cinza/preto com estrela + short renda + pantufas (opcional)",
        "Casa, pijama fofo, qualquer personagem",
        "qualquer",
    ),
    "SKIP__download_6_.png": (
        "sleep_black_offshoulder_boyshort.png",
        "Tee ombro + boyshort",
        "sleep",
        "Camiseta preta ombro a ombro + boyshort preto com cruz",
        "Casa, intimidade casual ousada",
        "Alex / Valk",
    ),
    "SKIP__108b1ceaf17432a27c4cf9dc647308a7.jpg": (
        "lounge_bra_cardigan_shorts.jpg",
        "Sutiã lounge + cardigan",
        "sleep",
        "Sutiã branco 'LOUNGE' + short moletom cinza + cardigan bege",
        "Casa, manhã, lounge íntimo",
        "qualquer",
    ),
    "SKIP__897fc65eb1d6de1b5b39f6ea8657cd4c.jpg": (
        "intimate_black_sheer_robe.jpg",
        "Robe sheer + sutiã",
        "intimate",
        "Robe preto transparente renda + sutiã preto",
        "Intimidade, pós-banho ousado",
        "Valk",
    ),
    # Intimate sets (subcategoria sutiã/calcinha / lingerie peça)
    "SKIP__1e4511b80d6edea53fd2da4e53c24842.jpg": (
        "intimate_burgundy_lace_set.jpg",
        "Set vinho renda",
        "intimate",
        "Top crop vinho renda + calcinha combinando (cruz no peito)",
        "Intimidade Ryan/Valk ou cena íntima; completar com robe se quiser",
        "Valk",
    ),
    "SKIP__download_4_crew.png": (
        "intimate_knit_crop_thong.png",
        "Tricô crop + fio",
        "intimate",
        "Suéter/tricô crochê ombro de fora + calcinha fio preta",
        "Intimidade / look ousado incompleto (ref)",
        "Valk / Alex",
    ),
    "SKIP__download_7_.png": (
        "intimate_sheer_shirt_thong.png",
        "Camisa sheer + fio",
        "intimate",
        "Camisa roxa/azul semi-transparente + calcinha fio renda preta",
        "Intimidade, manhã ousada",
        "Valk",
    ),
    # Club / ousado
    "SKIP__download_8_.png": (
        "club_black_leather_harness_mini.png",
        "Halter couro + mini",
        "club",
        "Top halter couro preto com argola + mini saia rebites + botas altas",
        "Clube, night out ousado",
        "Alex (combina bem)",
    ),
    "SKIP__download_5_.png": (
        "street_bikini_micro_denim.png",
        "Top off + micro denim",
        "club",
        "Top branco off-shoulder + micro short jeans + fio preto por baixo",
        "Street ousado, verão extremo, intimidade casual",
        "Alex / Valk",
    ),
    "SKIP__9e5cbdfb15f3da819b2567fb8621f081.jpg": (
        "club_black_chain_mermaid.jpg",
        "Vestido preto correntes",
        "club",
        "Vestido preto sereia cut-outs + correntes douradas",
        "Clube high-end, corpo",
        "Reina / Valk",
    ),
    # Formal
    "SKIP__1d87935a06605c7d3f8a1448829b943a.jpg": (
        "formal_shirt_leather_harness.jpg",
        "Camisa + calça couro",
        "formal",
        "Camisa cinza social + calça couro preta + cinto multi + botas",
        "Formal ousado, job de rua high-end, corpo",
        "Alex / Valk",
    ),
    "SKIP__5d6791b1460a19b03e5bd85c88a72d39.jpg": (
        "formal_black_red_tie_suit.jpg",
        "Terno preto gravata vermelha",
        "formal",
        "Blazer + camisa + gravata vermelha + calça pretos + luvas",
        "Formal andrógino, evento, poder",
        "Alex / qualquer",
    ),
    "SKIP__68a8c6d68d30d4f2d294f902a97bf2ac.jpg": (
        "formal_shirt_tie_harness.jpg",
        "Camisa + gravata + harness",
        "formal",
        "Camisa branca manga curta + gravata preta + harness/cinto peito + calça",
        "Formal fetish-light, clube corp",
        "Alex",
    ),
    "SKIP__dfe791ad468d304c98f04bf432080ab9.jpg": (
        "formal_steampunk_brown_coat.jpg",
        "Casaco steampunk marrom",
        "formal",
        "Casaco/colete marrom com detalhes metal + camisa branca babados",
        "Fantasia steampunk, formal dark",
        "qualquer",
    ),
    # Evening / fantasy / Reina
    "SKIP__897eea543c71a4fad5f3db8bdbdc5938.jpg": (
        "evening_pink_nightgown_cape.jpg",
        "Vestido rosa + capa",
        "evening",
        "Vestido longo rosa claro ombro a ombro + capa rosa",
        "Gala soft, nightwear elegante",
        "Reina (combina bem)",
    ),
    "SKIP__fcf4cd95df72a133221bba095a849692.jpg": (
        "evening_black_star_gown.jpg",
        "Gown preto estrelas",
        "evening",
        "Vestido longo preto one-shoulder + estrelas/ouro + fenda (sheet)",
        "Gala, fantasia celestial",
        "Reina (combina bem)",
    ),
    "SKIP__3cffb28ceb07597fd702f1a0b7c6bfdb.jpg": (
        "fantasy_winter_blue_cape.jpg",
        "Gown inverno azul",
        "fantasy",
        "Vestido azul gelo + capa pele + botas + cintos (sheet design)",
        "Fantasia inverno, evento raro",
        "Reina / qualquer",
    ),
    "SKIP__5adf6b27b775426694a07394050ae50b.jpg": (
        "evening_white_feather_gown.jpg",
        "Gown branco penas",
        "evening",
        "Vestido branco prata com ombros em pena/asa e bordado",
        "Gala, fantasia angelical",
        "Reina",
    ),
    "SKIP__2b5a226ca78e9be7348d9fb2e6c0ee02.jpg": (
        "fantasy_white_red_rose_gown.jpg",
        "Vestido branco e vermelho",
        "fantasy",
        "Corset branco + saia camadas branca/vermelha + rosas",
        "Fantasia, evento, gala dramática",
        "Reina",
    ),
    "SKIP__de962373aad2f1712b9dee23e46ad1aa.jpg": (
        "special_white_gold_angel_mini.jpg",
        "Mini angelical branca",
        "special",
        "Corset branco/ouro + mini babados + meias 7/8 (sheet)",
        "Costume, especial, clube temático",
        "Reina",
    ),
    "SKIP__e0145d9e7c73430bb7489984adb1423b.jpg": (
        "evening_lilac_star_gown.jpg",
        "Gown lilás estrelas",
        "evening",
        "Vestido lilás/prata fluido com correntes e fenda",
        "Gala, fantasia",
        "Reina",
    ),
    "SKIP__ec9386c1724da6bdbe617a369d824fcc.jpg": (
        "evening_white_corset_gown.jpg",
        "Gown branco corset",
        "evening",
        "Vestido branco longo com corset e ombro de fora",
        "Gala romântica, fantasia",
        "Reina / Valk",
    ),
    # Street / combat fashion
    "SKIP__142464be4a263c260f52acf4a300b27b.jpg": (
        "street_purple_crop_combat.jpg",
        "Crop roxo + calça",
        "street",
        "Crop/colete roxo + calça roxa larga + arm wraps pretos",
        "Street combate fashion, pack ousado",
        "Alex / Valk",
    ),
    "SKIP__b81f21a5f87aa607bd2de49c6e8c71f0.jpg": (
        "street_plaid_crop_cargo.jpg",
        "Flannel + crop + cargo",
        "street",
        "Jaqueta flannel vermelha + crop cinza + cargo preta com tiras",
        "Street, pack, dia a dia ousado",
        "Alex / qualquer",
    ),
}

# Remaining files - still include with best-effort names after quick generic
EXTRA_UNREAD = [
    "SKIP__9b1ad52965da5fdf299b07307fda17c8.jpg",
    "SKIP__67c52fbf05faf84fb35be041c55af988.jpg",
    "SKIP__70ece3e2ae2ef4da4e8d192117776990.jpg",
    "SKIP__375eebe8fe1df9e3afb4338455f3e7a3.jpg",
    "SKIP__3377ea95cba176a7f50f582eae213f23.jpg",
    "SKIP__096104f0613d833f0c975d118610910e.jpg",
    "SKIP__307099a92dbac46c8febf16f78d625d8.jpg",
    "SKIP__a3e64beeeeb3153e6ba3c11a2d792ab9.jpg",
    "SKIP__b6f508cf4390529e20a8d79608ca0b4f.jpg",
    "SKIP__b956f205c4cf13880d6dbc8360aed005.jpg",
    "SKIP__d1f1ba8cd496f2d1a44a9d8963ff397b.jpg",
]


def main() -> None:
    CREW.mkdir(parents=True, exist_ok=True)
    integrated = []
    missing = []

    for src_name, meta in MAP.items():
        src = WS_SKIP / src_name
        if not src.exists():
            missing.append(src_name)
            continue
        crew_name, quick, cat, pieces, quando, vibe = meta
        dst = CREW / crew_name
        shutil.copy2(src, dst)
        # move to type-appropriate usados in WS if possible
        integrated.append((crew_name, quick, cat, pieces, quando, vibe, src_name))
        print(f"OK {crew_name}")

    # For unread extras: still copy with ref_pool names so user has them
    for src_name in EXTRA_UNREAD:
        src = WS_SKIP / src_name
        if not src.exists():
            missing.append(src_name)
            continue
        stem = src_name.replace("SKIP__", "").split(".")[0][:12]
        ext = src.suffix
        crew_name = f"ref_pool_{stem}{ext}"
        shutil.copy2(src, CREW / crew_name)
        integrated.append(
            (
                crew_name,
                f"Ref pool {stem}",
                "ref",
                "Ref solta do pool — extrair silhueta/peças da imagem",
                "Referência; usar se a cena pedir o estilo",
                "qualquer",
                src_name,
            )
        )
        print(f"OK ref {crew_name}")

    # Append markdown section
    lines = [
        "\n\n# INTIMIDADE / NIGHTWEAR / OUSADO / GALA (lote pool)\n\n",
        "> Subcategoria **íntimo** (`intimate_*`): sutiã/calcinha/sets mínimos — válidos para cenas de intimidade (ex.: Ryan/Valk).  \n",
        "> **Combina com** é só sugestão de vibe, **não** default de personagem.\n\n",
    ]
    for crew_name, quick, cat, pieces, quando, vibe, _src in integrated:
        if cat == "ref":
            continue  # handle refs in bulk
        lines.append(f"## {quick}\n\n")
        lines.append(f"**Arquivo:** `{crew_name}`  \n")
        lines.append(f"**Nome rápido:** {quick}  \n")
        lines.append(f"**Categoria:** {cat}  \n")
        if vibe and vibe != "qualquer":
            lines.append(f"**Combina com (sugestão):** {vibe}  \n")
        lines.append(f"\n![{quick}](../imagens/crew/guarda_roupas/{crew_name})\n\n")
        lines.append("### Descrição visual (roupa)\n")
        lines.append(f"- {pieces}\n\n")
        lines.append("### Quando usar\n")
        lines.append(f"{quando}.\n\n")
        lines.append("---\n\n")

    lines.append("## Refs soltas do pool (ainda sem nome fino)\n\n")
    lines.append(
        "Arquivos `ref_pool_*` — use só se a cena pedir; extrair roupa da imagem.\n\n"
    )
    for crew_name, quick, cat, pieces, quando, vibe, _src in integrated:
        if cat != "ref":
            continue
        lines.append(f"- `{crew_name}` — {pieces}\n")
    lines.append("\n")

    text = MD.read_text(encoding="utf-8")
    # insert before final Notas if present at end, else append
    marker = "## Notas de narração"
    if marker in text:
        text = text.replace(marker, "".join(lines) + marker, 1)
    else:
        text = text + "".join(lines)
    MD.write_text(text, encoding="utf-8")

    print(f"\nIntegrated {len(integrated)} looks; missing {len(missing)}")
    if missing:
        print("MISSING:", missing)


if __name__ == "__main__":
    main()
