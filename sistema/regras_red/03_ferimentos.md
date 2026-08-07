---
version: 1.0.0
status: stable
last_updated: 2026-08-07
source: Cyberpunk RED core (resumo operacional)
---

# Ferimentos — MVP

**Pré-requisito:** [02_combate.md](02_combate.md) · [01_core.md](01_core.md).  
Em dúvida (cirurgia, drogas, critical injuries table completa) → core book.

---

## 1. Hit Points (HP)

Fórmula RED:

```text
HP = 10 + 5 × floor( (BODY + WILL) / 2 )
```

Usar BODY e WILL **da ficha**. Se a ficha já listar HP, preferir o valor da ficha se coerente com a fórmula; se divergir de forma óbvia, anotar no Finalizar (não retcon silencioso).

---

## 2. Dano vs armadura (SP)

1. Determinar localização se importar (corpo vs cabeça) — MVP: **corpo** por default salvo headshot declarado/com regra.  
2. Rolar **dano da arma** (ficha / core).  
3. Subtrair **SP** da armadura na localização.  
4. HP perdidos = dano restante (mínimo 0 se SP absorveu tudo).  
5. **Ablação:** se dano atravessou (HP perdidos > 0) ou conforme core para hits na armadura — no MVP: **−1 SP** na localização quando o hit causa HP damage (alinhar ao core se divergir na mesa).

Cabeça: SP de head armor; regras de headshot do core se a mesa for usar (declarar).

---

## 3. Seriously Wounded (SW)

```text
Se HP atuais ≤ metade do HP máximo → Seriously Wounded
```

- Penalidade típica core: **−2** em ações (enquanto SW).  
- Narrar dor, sangue, mobilidade reduzida — **e** aplicar o −2.

---

## 4. HP ≤ 0 — Death Saves

Quando HP chegam a 0 ou menos:

1. Personagem **fora de combate** / inconsciente conforme gravidade.  
2. **Death Save:** rolar conforme core (BODY-based; falhas acumulam).  
3. Estabilizar com **First Aid** / **Paramedic** / Medtech **antes** de morte definitiva.  
4. NPC mook: pode morrer no 0 HP sem Death Save (ritmo de mesa) — **PC e NPCs nomeados** usam Death Save.

---

## 5. First Aid / cura (MVP)

| Ação | Skill | Efeito resumido |
| ---- | ----- | --------------- |
| Estabilizar (HP ≤ 0 / crítico) | First Aid / Paramedic | Para Death Saves / estabiliza — DV e efeito exatos no core |
| Cura de campo | First Aid / Paramedic | Recupera HP limitados (core); não full heal de combate |
| Cirurgia / chrome | Surgery / Medtech / ripper | Fora do MVP detalhado; Stitch/Doc quando cena exigir |

Cada tentativa relevante = teste [01_core](01_core.md) se houver risco (tempo, combate, falha piora).

---

## 6. O que atualizar no estado

| Mudou | Onde |
| ----- | ---- |
| HP / SW do PC | Ficha se mantida; **sempre** nota no `sessao_resumo` se combate importou |
| SP / ablação | Ficha / resumo |
| Morte de NPC nomeado | Consequências / board se impacto permanente |
| HL / chrome | Só se instalação (Fase 3 detalha; MVP: não inventar HL) |

Checklist Finalizar: [comandos_jogador.md](../comandos_jogador.md) § C.

---

## Changelog

### 1.0.0 — 2026-08-07

- MVP: HP, SP/ablação, SW, Death Save, First Aid resumo, onde registrar.
