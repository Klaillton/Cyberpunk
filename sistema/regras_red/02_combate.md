---
version: 1.1.0
status: stable
last_updated: 2026-08-07
source: Cyberpunk RED core (resumo operacional)
---

# Combate

**Pré-requisito:** [01_core.md](01_core.md) · dano [03_ferimentos.md](03_ferimentos.md) · armas [04_armas.md](04_armas.md).  
**Veículos:** [09_veiculos.md](09_veiculos.md).  
**Loadout Ryan:** [ryan_loadout.md](../../fichas/ryan_loadout.md).

**Adiado (Fases 3–4):** martial arts completo, critical injury table longa, netrunning em combate.

---

## 1. Fluxo

```text
1. Há combate / ameaça imediata?
2. Iniciativa se a ordem importar (REF + 1d10)
3. Turno: movimento razoável + ação de ataque (ou outra)
4. Resolver ataque → dano → estado
5. Narrar resultado (depois da resolução)
```

---

## 2. Ataque

```text
Total = STAT + Skill de combate + 1d10 + mods
```

Skill por categoria: [04_armas](04_armas.md).

| Situação | Resolver contra |
| -------- | --------------- |
| Alvo não se esquiva / desprevenido | **DV** da situação/arma |
| Alvo ativo | **Oposto** vs Evasion (DEX + Evasion + 1d10) |
| Surpreso (stealth OK) | Sem Evasion ou DV facilitado; **ainda rola ataque** |

---

## 3. ROF e autofire (1.1.0)

| ROF | MVP |
| --- | --- |
| 1 | Um ataque |
| 2+ | Declarar quantos tiros (até ROF); cada tiro além do primeiro impõe **penalidade cumulativa** ao total (atalho: **−1 por tiro extra** no mesmo ataque, ou usar regra de autofire do core se a mesa quiser precisão) |
| Autofire / supressão | Ação de **supressão**: alvos sob fogo sofrem −DV ou −2 para agir expostos até se cobrirem (1 round); gasta munição generosa |

**Não inventar ROF** — valor da arma no loadout/core; default 1.

---

## 4. Múltiplos combatentes

- Cada PC / NPC nomeado: iniciativa própria (ou agrupar mooks).  
- **Mooks em grupo:** um init; 1–2 ataques representativos por round ou “onda” com DV fixo.  
- Aliados (Valk, Scout): agem no init; se delegados, ver [npc_agencia_cena](../npc_agencia_cena.md).  
- Não resolver 16 mooks ataque-a-ataque se o foco for o PC — comprimir, mas **não** auto-win sob risco real.

---

## 5. Cobertura, alcance, melee

| Fator | Efeito MVP |
| ----- | ---------- |
| Cobertura parcial | +DV ao atacante |
| Cobertura total | Precisa flanquear / destruir |
| Alcance | [04](04_armas.md) faixas |
| Melee fora de alcance | Precisa fechar (movimento / teste) |

---

## 6. Stealth attack

```text
Não detectado ≠ invisível ≠ morte automática
```

1. Stealth vs Perception ([house](../house_rules/regras_campanha.md)).  
2. Se OK → ataque com vantagem de surpresa.  
3. Dano normal ([03](03_ferimentos.md)); alvo pode sobreviver.  
4. Se falhar → alarme / combate normal.

---

## 7. Drones

- Controle sob pressão: Tech skill ([08_techie](08_techie.md)).  
- Warden F03 terrestre; Vespas loadout; Condor/Corujas pack F16.  
- Stats: [ryan_loadout](../../fichas/ryan_loadout.md).

---

## 8. Veículos em combate

Ponte: [09_veiculos](09_veiculos.md) (atirar de/para veículo, mounts, perseguição).

---

## 9. Registrar após combate

HP/SW/SP, munição se importar, Heat se alarme, `Ruleset: 1.1.0` no resumo.

---

## Changelog

### 1.1.0 — 2026-08-07

- ROF/autofire/supressão, múltiplos combatentes, links 04/08/09/loadout.

### 1.0.0 — 2026-08-07

- MVP ataque, Evasion, stealth attack, drones ponte.
