---
version: 1.1.0
status: stable
last_updated: 2026-10-03
source: Cyberpunk RED core (resumo operacional) + campanha
---

# Referência rápida — 1 página

**Ruleset atual:** ver [versionamento_regras.md](../versionamento_regras.md) (**1.4.0**). Sessões 017–028 ficam em 1.3.0.  
**Cutoff:** sessões ≤016 canon; **017+** estas regras (F18).  
**Auditoria combates pré-camada (só observação):** [plans/auditoria_combates_canonicos.md](../../plans/auditoria_combates_canonicos.md) — **sem retcon**.

---

## Quando rolar

| Situação | Ação |
| -------- | ---- |
| Trivial / sem risco | Não rolar |
| Risco / oposição / custo grave | Rolar |

```text
Total = STAT + Skill + 1d10 [+ mods]  vs  DV  ou  oposto
```

Antes do total: chrome da ficha. **Número** soma. **Função** acontece e não vira dado. [05](05_cyberware.md) §4.

Apresentar: d10 · STAT · Skill · mods · `Chrome:` · total · DV/oposto · resultado · consequência.

---

## DV atalho

| DV | Rótulo |
| -- | ------ |
| 9 | Everyday |
| 13 | Challenging |
| 15 | Difficult |
| 17 | Professional |
| 21 | Heroic |
| 24 | Incredible |
| 29 | Legendary |

**d10:** 10 = +1d10 · 1 = −1d10 (fumble).

---

## Combate (1 linha)

Iniciativa `REF+1d10` + Kerenzikov **+2** se a ficha tiver · Ataque: skill da arma + o +2 de REF se tiver Kerenzikov · vs DV ou Evasion · Dano − SP → HP · SW em ½ HP (−2, salvo Pain Editor ligado) · Death Save se HP ≤ 0.

**Armas Ryan:** [ryan_loadout.md](../../fichas/ryan_loadout.md) (dano/ROF).  
**Mule:** [vehicle - the_mule.md](../../fichas/vehicle%20-%20the_mule.md) · [09](09_veiculos.md).

---

## Stealth

Não detectado ≠ invisível ≠ auto-kill. Stealth vs Perception → depois ataque com surpresa. [house](../house_rules/regras_campanha.md).

---

## Drones e Agents (fatos)

| ID | Regra |
| -- | ----- |
| F03 | Warden **drone** terrestre — **não voa** |
| F12 | Vespas Hornet/Vesper/Barbed |
| F16 | Condor/Corujas no **Pack** |
| F19 | Vault **implant** · Profissional **subdermal** · Honeypot **visível** · Arbiter/Watchdog · [agent_security](../../plans/agent_security.md) · ≠ Warden drone |

---

## Roles (crew)

| Role | Quem | Doc |
| ---- | ---- | --- |
| Maker | Ryan | [07](07_roles.md) · [08](08_techie.md) |
| Moto | Valk | [07](07_roles.md) · [09](09_veiculos.md) |
| Combat Awareness | Jax, Reina | [07](07_roles.md) |
| Interface | Alex | [07](07_roles.md) · [10](10_netrunning.md) |
| Medicine | Stitch | [07](07_roles.md) · [03](03_ferimentos.md) |
| Operator | Kaz | [07](07_roles.md) |
| Credibility | Echo | [07](07_roles.md) · [echo_exposicao](../echo_exposicao.md) |
| Charismatic Impact **6** | Leopold / Prometheus | [07](07_roles.md) · ficha rockerboy |

---

## NET (1 linha)

Interface rank → NET Actions/turno · ação vs DV do nó/ICE · programas do deck · alarme → meat. [10](10_netrunning.md).

---

## HL / eddies

- Chrome na jogada: [05](05_cyberware.md) §4 — número ou função. Ryan: **HL histórico 78** / **Humanidade atual 63/70** (pós-Doc; residual E011). SP de Subdermal/Skinweave = o SP já escrito, sem somar de novo.  
- Dinheiro: [economia.md](../../economia.md) (faixa 1,5k–4k eb estimada).

---

## Índice de módulos

| # | Arquivo |
| - | ------- |
| 00 | [Integridade / cutoff](00_integridade_regras.md) |
| 01 | [Core](01_core.md) |
| 02 | [Combate](02_combate.md) |
| 03 | [Ferimentos](03_ferimentos.md) |
| 04 | [Armas (categorias)](04_armas.md) |
| 05 | [Cyberware](05_cyberware.md) |
| 06 | [Skills](06_skills.md) |
| 07 | [Roles](07_roles.md) |
| 08 | [Techie](08_techie.md) |
| 09 | [Veículos](09_veiculos.md) |
| 10 | [Netrunning](10_netrunning.md) |
| 11 | **Este arquivo** |

---

## Ordem de resolução

```text
INTENÇÃO → RISCO → REGRA → FICHA (chrome: número ou função) → MODS → ROLAGEM → RESULTADO → ESTADO → NARRAÇÃO
```

---

## Changelog

### 1.1.0 — 2026-10-03

- Atalho da jogada abre o chrome. Kerenzikov e Pain Editor na linha de combate.

### 1.0.0 — 2026-08-07

- Página de referência consolidada (Fase 4).
