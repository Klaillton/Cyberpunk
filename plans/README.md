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
| [add-cyberpunk-red-mechanics.md](add-cyberpunk-red-mechanics.md) | `approved` | Camada mecânica RED, cutoff, Finalizar, fases MVP→expansão |
| ~~add_cyberpunk_mecanichs.md~~ | `cancelled` | Typo + conteúdo superado — ver link no arquivo |

---

## Fluxo

```text
draft em plans/  →  revisão  →  approved  →  in_progress  →  implementação  →  done
```

Plan mode do Grok (`sessions/.../plan.md`) é rascunho de sessão; **plano canônico de trabalho** = arquivo em `plans/` após aprovação.
