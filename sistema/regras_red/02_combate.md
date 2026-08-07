---
version: 1.0.0
status: stable
last_updated: 2026-08-07
source: Cyberpunk RED core (resumo operacional)
---

# Combate — MVP

**Pré-requisito:** [01_core.md](01_core.md) · dano em [03_ferimentos.md](03_ferimentos.md).  
**Escopo MVP:** 1 vs 1 / poucos alvos, um ataque por vez, stealth attack.  
**Adiado (Fase 2):** autofire, suppressive fire, combate em grupo completo, veículos em combate, martial arts detalhado.

---

## 1. Fluxo simplificado

```text
1. Há combate / ameaça imediata?
2. Iniciativa se a ordem importar (REF + 1d10)
3. No turno: 1 ação de ataque relevante (MVP) + movimento razoável
4. Resolver ataque → dano → estado
5. Narrar resultado
```

Fora de combate tático (emboscada já resolvida, alvos inconscientes sem risco): usar [01_core](01_core.md) “quando rolar”.

---

## 2. Ataque

```text
Total = STAT + Skill de combate + 1d10 + mods
```

| Tipo | Skills típicas (RED) |
| ---- | -------------------- |
| Arma de fogo | Handgun, Shoulder Arms, etc. (conforme ficha) |
| Melee / faca | Melee Weapon, Brawling, Martial Arts |
| Arremesso | Athletics / skill de arremesso da ficha |

### Alvo do total

| Situação | Resolver contra |
| -------- | --------------- |
| Alvo **não** se esquiva / está desprevenido de forma clara | **DV** da arma/situação (core range/DV table) ou DV 13–15 típico de tiro/melee sob pressão |
| Alvo ativo em combate | **Oposto:** ataque vs **Evasion** (DEX + Evasion + 1d10) ou skill de defesa da ficha |
| Alvo **surpreso** / não ciente (pós stealth bem-sucedido) | Vantagem: sem Evasion **ou** DV mais baixo; **ainda precisa de ataque** (não é auto-kill) |

Mods comuns (só se a ficção justificar): cobertura do alvo, alcance, luz, ferimento (SW −2), mira, surpresa.

---

## 3. Cobertura e alcance (básico)

| Fator | Efeito MVP |
| ----- | ---------- |
| Cobertura parcial | +DV ao atacante **ou** SP extra / miss chance narrativo alinhado ao core |
| Cobertura total | Não dá para acertar sem flanquear / destruir cobertura |
| Alcance extremo | Aumentar DV ou impedir tiro (arma) |
| Melee sem alcance | Precisa fechar distância (movimento / teste) |

Detalhes de range bands por arma → ficha + core (Fase 2 tabela dedicada).

---

## 4. Stealth attack (ponte)

Não confundir:

```text
Não ser detectado  ≠  Invisível  ≠  Morte automática
```

**Pipeline:**

1. **Stealth / hide / silence** (core skill) vs **Perception / Awareness** do alvo ou vigia — oposto ([01_core](01_core.md)).  
2. Fatores: [house_rules/regras_campanha.md](../house_rules/regras_campanha.md).  
3. Se **detectado:** combate normal / alarme.  
4. Se **não detectado:** ataque com vantagem de surpresa (sem Evasion ou DV facilitado) + dano normal ([03](03_ferimentos.md)).  
5. Alvo com HP alto / armadura pesada pode **sobreviver** ao primeiro golpe → continua a cena.

Ryan competente + preparação + drones = **mods legítimos** e DV realistas, não skip de passo 1–4.

---

## 5. Drones em combate (MVP)

- Controlar drone: skill/tech da ficha (Techie / Electronic Security / Weapon Systems conforme ficha).  
- Ataque do drone: conforme arma/montagem do drone **ou** auxílio (recon, jam, distração = mods para Ryan/aliados).  
- **Warden:** terrestre, proteção/utilidade (F03) — **não** resolve como drone aéreo.  
- Detalhe de campanha: house rules.

---

## 6. O que registrar após o combate

- HP / SW / morte de PC ou NPC relevante  
- SP / ablação se armadura foi atingida  
- Munição se a ficha ou a cena importar  
- Heat / consequências se barulho/alarme  
- No resumo: `Ruleset: 1.0.0` + 1 linha de outcome mecânico se houver ferimento

---

## Changelog

### 1.0.0 — 2026-08-07

- MVP combate: ataque, Evasion/DV, cobertura básica, stealth attack, drones ponte.
