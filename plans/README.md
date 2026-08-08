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
| [add-cyberpunk-red-mechanics.md](add-cyberpunk-red-mechanics.md) | `done` (fases 0–5) | Ruleset **v1.3.0** · camada mecânica completa |
| [auditoria_combates_canonicos.md](auditoria_combates_canonicos.md) | `done` | Observação I001/I002/J001/T008… · **sem retcon** |
| [agent_security.md](agent_security.md) | `active` | Agents WIREGHOST (Vault/Profissional/Honeypot/**Arbiter**) · F19 · in-fiction |
| ~~add_cyberpunk_mecanichs.md~~ | `cancelled` | Typo + conteúdo superado — ver link no arquivo |

---

## Fluxo

```text
draft em plans/  →  revisão  →  approved  →  in_progress  →  implementação  →  done
```

Plan mode do Grok (`sessions/.../plan.md`) é rascunho de sessão; **plano canônico de trabalho** = arquivo em `plans/` após aprovação.
