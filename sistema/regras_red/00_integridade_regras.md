---
version: 1.0.0
status: stable
last_updated: 2026-08-07
source: Cyberpunk RED core (resumo operacional) + house rules da campanha
---

# Integridade das regras

**Finalidade:** hierarquia, cutoff e proibições.  
**SoT RAW:** `base/Cyberpunk Red.pdf` (em dúvida, abrir o livro).  
**Resumos em `regras_red/`** = atalhos de mesa/IA — **não** substituem o core book.

---

## 1. Hierarquia

```text
1. RAW (Cyberpunk RED core + DLCs usados na mesa)
2. HOUSE RULES (sistema/house_rules/) — explícitas
3. DECISÃO PROVISÓRIA (só na sessão; vira house rule só se o jogador confirmar no Finalizar)
```

Em conflito: **nível superior vence**.  
Provisório **não** se cola silenciosamente no RAW.

---

## 2. MECHANICAL_RULESET_CUTOFF

| Campo | Valor |
| ----- | ----- |
| **ID** | F18 · Ruleset **v1.0.0** |
| **Última sessão pré-camada** | **016** (e anteriores) |
| **Primeira sessão com camada** | **017+** (quando este ruleset estiver no branch) |
| **Canon 001–016** | **Intacto** — não re-rolar, não “corrigir” kills/scavs/jobs |

```text
PASSADO (≤016) → CANON CONSOLIDADO → REGRAS v1.0.0 → FUTURO (017+)
```

---

## 3. Ordem de resolução (ação com risco)

```text
1. INTENÇÃO
2. AÇÃO
3. RISCO (há falha / oposição / custo grave?)
4. REGRA (qual módulo?)
5. FICHA (STAT, Skill, gear)
6. MODIFICADORES (só justificados)
7. ROLAGEM (se necessário)
8. RESULTADO
9. CONSEQUÊNCIA
10. ATUALIZAÇÃO DE ESTADO (resumo / ficha / ledgers)
11. NARRAÇÃO
```

- Narrar o desfecho **depois** da resolução.  
- **Proibido:** decidir o sucesso na prosa e depois inventar um d10 que “confirme”.  
- Em operação tática, manter motor de cena **resultado primeiro** ([diretrizes_narrador](../diretrizes_narrador.md) N1b/N8) **com** o resultado mecânico já obtido.

---

## 4. Proibições

| Proibido | Por quê |
| -------- | ------- |
| Inventar bônus/penalidades “intuitivos” sem regra | Quebra integridade |
| Misturar RED / 2020 / 2077 | Sistemas diferentes |
| Sucesso automático sob **risco real** só por ficha alta | Anti-super-herói |
| Rolagem para ação **trivial** | Dice-spam |
| Retcon de outcomes pré-cutoff | F18 |
| Colar house rule dentro de arquivo RAW sem marcar | Contamina SoT |
| Carregar `regras_red/` inteiro no tier-0 | Sandbox esquece |

---

## 5. Módulos MVP (v1.0.0)

| Arquivo | Uso |
| ------- | --- |
| [01_core.md](01_core.md) | Testes, DV, opostos, Luck, quando rolar |
| [02_combate.md](02_combate.md) | Combate básico + ponte stealth attack |
| [03_ferimentos.md](03_ferimentos.md) | HP, SP, SW, Death Save, First Aid |
| [../house_rules/regras_campanha.md](../house_rules/regras_campanha.md) | Stealth, drones, campanha |
| [../versionamento_regras.md](../versionamento_regras.md) | Versões |

Fases 2+ (armas detalhadas, Maker, NET, veículos, roles): ver [plans/add-cyberpunk-red-mechanics.md](../../plans/add-cyberpunk-red-mechanics.md).

---

## Changelog

### 1.0.0 — 2026-08-07

- MVP: integridade, cutoff F18, ordem de resolução, proibições.
