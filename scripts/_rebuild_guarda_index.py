# -*- coding: utf-8 -*-
"""Rebuild crew_guarda_roupas.md index: occasion categories, #IDs, quick names, anchors."""
from pathlib import Path
import re

path = Path(r"C:\workspace\Cyberpunk\fichas\crew_guarda_roupas.md")
text = path.read_text(encoding="utf-8")
lines = text.splitlines(keepends=True)

start_idx = None
for i, l in enumerate(lines):
    if l.startswith("# BADLANDS"):
        start_idx = i
        break
if start_idx is None:
    raise SystemExit("Could not find # BADLANDS")

looks = []
i = start_idx
current_h1 = None
while i < len(lines):
    l = lines[i]
    if l.startswith("# ") and not l.startswith("## "):
        current_h1 = l[2:].strip()
        i += 1
        continue
    if l.startswith("## "):
        h2 = l[3:].strip()
        arquivo = None
        quando = ""
        vibe = ""
        j = i + 1
        while j < len(lines) and not lines[j].startswith("## ") and not (
            lines[j].startswith("# ") and not lines[j].startswith("## ")
        ):
            m = re.search(r"\*\*Arquivo:\*\*\s*`([^`]+)`", lines[j])
            if m:
                arquivo = m.group(1)
            m2 = re.search(r"\*\*Combina com[^*]*:\*\*\s*(.+)", lines[j])
            if m2:
                vibe = m2.group(1).strip().rstrip("  ")
            if lines[j].startswith("### Quando usar"):
                if j + 1 < len(lines):
                    quando = lines[j + 1].strip()
            j += 1
        if arquivo:
            looks.append(
                {
                    "h1": current_h1 or "",
                    "h2": h2,
                    "file": arquivo,
                    "quando": quando,
                    "vibe": vibe,
                    "header_line": i,
                }
            )
        i = j
        continue
    i += 1

print(f"Parsed looks: {len(looks)}")


def cat_slug(cat: str) -> str:
    """ASCII slug for anchors (avoid accent corruption)."""
    table = str.maketrans(
        {
            "á": "a",
            "à": "a",
            "ã": "a",
            "â": "a",
            "é": "e",
            "ê": "e",
            "í": "i",
            "ó": "o",
            "ô": "o",
            "õ": "o",
            "ú": "u",
            "ç": "c",
            "Á": "a",
            "É": "e",
            "Í": "i",
            "Ó": "o",
            "Ú": "u",
            "Ç": "c",
        }
    )
    s = cat.translate(table).lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def categorize(look):
    h1 = look["h1"].lower()
    h2 = look["h2"].lower()
    f = look["file"].lower()
    q = look["quando"].lower()

    # Filename prefixes win (most reliable)
    if f.startswith("piece_"):
        return "Peças (completar)"
    if f.startswith("intimate_"):
        return "Íntimo / nightwear"
    if f.startswith("medical_") or "scrubs" in f or "nurse" in f or "lab_coat" in f:
        return "Medical / clínico"
    if f.startswith("swim_") or "swim" in f:
        return "Swim / praia"
    if f.startswith("gym_") or "training" in f or "tennis" in f:
        return "Gym / treino"
    if f.startswith("sleep_") or f.startswith("lounge_"):
        return "Lounge / sleep / casa"
    if f.startswith("special_") or "school" in f or "latex" in f:
        return "Especial / costume"
    if "stealth" in f or f.startswith("combat_"):
        return "Combate / stealth / job"
    if f.startswith("tech_") or f.startswith("media_") or "netrunner" in f:
        return "Tech / media"
    if f.startswith("evening_"):
        return "Evening / gala"
    if f.startswith("club_"):
        return "Club / noite"
    if f.startswith("formal_"):
        return "Formal / office"
    if f.startswith("soft_") or f.startswith("fantasy_") or "steampunk" in f:
        return "Soft / pack / fantasia"
    if f.startswith("badlands_") or f.startswith("utility_"):
        return "Badlands / campo"
    if f.startswith("street_") or "rain" in f or "weather" in f:
        return "Street / Night City"
    if f.startswith("casual_"):
        return "Casual"

    # H1 section fallbacks (after filename)
    if "medical" in h1 or "clínico" in h1 or "clinico" in h1:
        return "Medical / clínico"
    if "swim" in h1 or "praia" in h1:
        return "Swim / praia"
    if "gym" in h1 or "treino" in h1 or "treino" in h2 or "gym" in h2:
        return "Gym / treino"
    if "lounge" in h1 or ("sleep" in h1 and "swim" not in h1) or "casa" in h1:
        return "Lounge / sleep / casa"
    if "especial" in h1:
        return "Especial / costume"
    if "stealth" in h1 or ("combate" in h1 and "gym" not in f):
        # combat/treino H1 can hold gym_* already handled by filename
        if "gym" in h2 or "tennis" in h2 or "marcial" in h2 or "training" in f:
            return "Gym / treino"
        return "Combate / stealth / job"
    if h1.startswith("tech") or "media" in h1:
        return "Tech / media"
    if "evening" in h1 or "gala" in h1:
        return "Evening / gala"
    if "clube" in h1 or "club" in h1:
        return "Club / noite"
    if "formal" in h1:
        return "Formal / office"
    if "soft" in h1 or "fantasia" in h1 or "pack" in h1:
        return "Soft / pack / fantasia"
    if "badlands" in h1 or "campo" in h1:
        return "Badlands / campo"
    if "street" in h1 or "night city" in h1:
        return "Street / Night City"
    if h1.startswith("casual"):
        return "Casual"

    if any(x in q for x in ["clínica", "hospital", "stitch", "plantão"]):
        return "Medical / clínico"
    if any(x in q for x in ["praia", "piscina"]):
        return "Swim / praia"
    if any(x in q for x in ["treino", "academia", "sparring"]):
        return "Gym / treino"
    if any(x in q for x in ["casa", "safehouse", "pijama", "sleep"]):
        return "Lounge / sleep / casa"
    if any(x in q for x in ["clube", "night out"]):
        return "Club / noite"
    if any(x in q for x in ["gala", "jantar alto"]):
        return "Evening / gala"
    return "Casual"


def quick_name(look):
    h2 = re.sub(r"^\d+\s*[·\-\.]\s*", "", look["h2"])
    name = re.sub(r"\s*\([^)]*\)\s*", " ", h2).strip()
    # strip prior look-id style
    name = re.sub(r"^look-\d+\s*", "", name, flags=re.I)
    if len(name) > 42:
        name = name[:40] + "…"
    return name


cat_order = [
    "Badlands / campo",
    "Street / Night City",
    "Casual",
    "Combate / stealth / job",
    "Tech / media",
    "Gym / treino",
    "Lounge / sleep / casa",
    "Íntimo / nightwear",
    "Formal / office",
    "Club / noite",
    "Evening / gala",
    "Soft / pack / fantasia",
    "Medical / clínico",
    "Swim / praia",
    "Especial / costume",
    "Peças (completar)",
]

for look in looks:
    look["cat"] = categorize(look)
    look["quick"] = quick_name(look)

by_cat = {c: [] for c in cat_order}
for look in looks:
    by_cat.setdefault(look["cat"], []).append(look)

id_num = 1
ordered = []
for cat in cat_order:
    for look in by_cat.get(cat, []):
        look["id"] = id_num
        look["id3"] = f"{id_num:03d}"
        look["anchor"] = f"look-{look['id3']}"
        ordered.append(look)
        id_num += 1
for look in looks:
    if "id" not in look:
        look["id"] = id_num
        look["id3"] = f"{id_num:03d}"
        look["anchor"] = f"look-{look['id3']}"
        ordered.append(look)
        id_num += 1

print("By category:")
for c in cat_order:
    n = len([x for x in ordered if x["cat"] == c])
    if n:
        print(f"  {c}: {n}")

idx = []
idx.append("## Índice rápido\n")
idx.append("\n")
idx.append(
    f"**Looks catalogados:** {len(ordered)} · cada **#** é um conjunto "
    f"(clique no nome → ficha completa).\n"
)
idx.append("\n")
idx.append(
    "**Como usar na cena:** diga o número (`#047`) ou o **nome rápido**. "
    "Categorias = ocasião. **Vibe** = *Combina com (sugestão)* — **não** default de personagem.\n"
)
idx.append("\n")
idx.append("### Categorias (ocasião)\n")
idx.append("\n")
for cat in cat_order:
    items = [x for x in ordered if x["cat"] == cat]
    if not items:
        continue
    slug = cat_slug(cat)
    idx.append(
        f"- [{cat}](#cat-{slug}) "
        f"({items[0]['id3']}–{items[-1]['id3']}, {len(items)} looks)\n"
    )
idx.append("\n")

for cat in cat_order:
    items = [x for x in ordered if x["cat"] == cat]
    if not items:
        continue
    slug = cat_slug(cat)
    idx.append(f'<a id="cat-{slug}"></a>\n')
    idx.append(f"### {cat}\n")
    idx.append("\n")
    idx.append("| # | Nome rápido | Arquivo | Vibe (sugestão) | Quando usar (resumo) |\n")
    idx.append("| -: | ----------- | ------- | --------------- | -------------------- |\n")
    for look in items:
        q = look["quando"].replace("|", "/")
        if len(q) > 60:
            q = q[:57] + "…"
        if not q:
            q = "—"
        v = (look.get("vibe") or "qualquer").replace("|", "/")
        if len(v) > 28:
            v = v[:26] + "…"
        idx.append(
            f"| **{look['id3']}** | [{look['quick']}](#{look['anchor']}) "
            f"| `{look['file']}` | {v} | {q} |\n"
        )
    idx.append("\n")

short_keywords = (
    "short",
    "romper",
    "overall",
    "skort",
    "biker",
    "microshorts",
    "onesie",
    "jumpsuit",
    "bermuda",
)
shorts = [
    x for x in ordered if any(k in x["file"].lower() for k in short_keywords)
]
idx.append("### Índice — Shorts & rompers (atalho)\n")
idx.append("\n")
idx.append("Mesmos **#** do índice principal — silhueta curta / uma peça curta.\n")
idx.append("\n")
idx.append("| # | Nome rápido | Arquivo |\n")
idx.append("| -: | ----------- | ------- |\n")
for look in shorts:
    idx.append(
        f"| **{look['id3']}** | [{look['quick']}](#{look['anchor']}) "
        f"| `{look['file']}` |\n"
    )
idx.append("\n")
idx.append("---\n")
idx.append("\n")

idx_start = None
for i, l in enumerate(lines):
    if l.startswith("## Índice rápido"):
        idx_start = i
        break
if idx_start is None:
    raise SystemExit("Could not find ## Índice rápido")

new_lines = lines[:idx_start] + idx + lines[start_idx:]

by_file = {x["file"]: x for x in ordered}

body_start = None
for i, l in enumerate(new_lines):
    if l.startswith("# BADLANDS"):
        body_start = i
        break

out = new_lines[:body_start]
i = body_start
while i < len(new_lines):
    l = new_lines[i]
    if l.startswith("## "):
        arquivo = None
        j = i + 1
        while j < len(new_lines) and not new_lines[j].startswith("## ") and not (
            new_lines[j].startswith("# ") and not new_lines[j].startswith("## ")
        ):
            m = re.search(r"\*\*Arquivo:\*\*\s*`([^`]+)`", new_lines[j])
            if m:
                arquivo = m.group(1)
                break
            j += 1
        if arquivo and arquivo in by_file:
            look = by_file[arquivo]
            # drop duplicate anchors if re-run
            if out and out[-1].startswith('<a id="look-'):
                out.pop()
            out.append(f'<a id="{look["anchor"]}"></a>\n')
            out.append(f'## {look["id3"]} · {look["quick"]}\n')
            i += 1
            continue
    out.append(l)
    i += 1

final = "".join(out)
final = re.sub(
    r"\*\*26 → ~[\d]+ looks\*\*[^\n]*",
    f"**26 → ~{len(ordered)} looks** · IDs `#001`–`#{ordered[-1]['id3']}`",
    final,
    count=1,
)

# Ensure single **Nome rápido:** after each Arquivo
def inject_quick(match):
    file = match.group(1)
    rest = match.group(2) or ""
    look = by_file.get(file)
    if not look:
        return match.group(0)
    # drop any existing Nome rápido right after arquivo
    rest = re.sub(r"^(?:\*\*Nome rápido:\*\*[^\n]*\n)+", "", rest)
    return (
        f"**Arquivo:** `{file}`  \n"
        f"**Nome rápido:** {look['quick']} · **#{look['id3']}**\n"
        f"{rest}"
    )


final = re.sub(
    r"\*\*Arquivo:\*\*\s*`([^`]+)`\s*\n((?:\*\*Nome rápido:\*\*[^\n]*\n)*)",
    inject_quick,
    final,
)

path.write_text(final, encoding="utf-8")
print(f"Wrote {path} with {len(ordered)} numbered looks")
for look in ordered[:8]:
    print(look["id3"], look["cat"][:20], look["quick"], look["file"])
print("...")
for look in ordered[-5:]:
    print(look["id3"], look["cat"][:20], look["quick"], look["file"])
