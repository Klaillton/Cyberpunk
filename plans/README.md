# Planos de trabalho (`plans/`)

**Finalidade:** controlar **o que estamos construindo** (sistema, processo, mecânica, tooling) — **não** o estado narrativo da campanha.

| Tipo de arquivo | Onde mora |
| --------------- | --------- |
| Planos de trabalho / features | **`plans/`** (esta pasta) |
| Estado da campanha (NOW, board, resumos) | `board/`, `logs/`, `event_queue.md`, etc. |
| Regras de jogo (após implementação) | `sistema/regras_red/`, `sistema/house_rules/` |

---

## Convenção

| Campo | Regra |
| ----- | ----- |
| Nome do arquivo | `kebab-case.md` (ex.: `add-cyberpunk-red-mechanics.md`) |
| Idioma no nome | português ou inglês, mas **consistente** e sem typos |
| Status (no topo do plano) | `draft` · `approved` · `in_progress` · `done` · `cancelled` |
| Conteúdo mínimo | objetivo · escopo · não-escopo · fases · arquivos tocados · critérios de sucesso · dependências |
| Atualização | ao mudar de fase, atualizar `status` e data |

### Template rápido

```markdown
# Título

**Status:** draft  
**Atualizado:** YYYY-MM-DD  
**Objetivo:** …

## Escopo / Não-escopo
## Fases
## Arquivos
## Critérios de sucesso
## Dependências
```

---

## Índice

| Plano | Status | Resumo |
| ----- | ------ | ------ |
| [add-cyberpunk-red-mechanics.md](add-cyberpunk-red-mechanics.md) | `done` (fases 0–5) | Ruleset **v1.3.0** neste plano. O ruleset vivo da mesa é **v1.4.0** em `sistema/regras_red/` |
| [auditoria_combates_canonicos.md](auditoria_combates_canonicos.md) | `done` | Observação I001/I002/J001/T008… · **sem retcon** |
| [alex_specter_kane_vida_pessoal.md](alex_specter_kane_vida_pessoal.md) | `done` (folded 2026-10-22) | Vida em NC da Alex. SoT na ficha e na nota §D |
| [stitch_vida_pessoal_dinamica_crew.md](stitch_vida_pessoal_dinamica_crew.md) | `done` (folded 2026-10-22) | Vida, casa, Vlad/Darius e contatos da Stitch. SoT na ficha e na nota §7–10 |
| [echo_vida_pessoal_relacoes.md](echo_vida_pessoal_relacoes.md) | `done` (folded 2026-10-22) | Vida em NC da Echo. SoT na ficha e na nota §D |
| [agent_security.md](agent_security.md) | `active` (2026-08-08) | Agents: implant Vault · subdermal Prof · Honeypot visível · Arbiter/Watchdog · F19 |
| ~~add_cyberpunk_mecanichs.md~~ | `cancelled` | Typo + conteúdo superado — ver link no arquivo |

---

## Fluxo

```text
draft em plans/  →  revisão  →  approved  →  in_progress  →  implementação  →  done
```

Plan mode do Grok (`sessions/.../plan.md`) é rascunho de sessão; **plano canônico de trabalho** = arquivo em `plans/` após aprovação.
