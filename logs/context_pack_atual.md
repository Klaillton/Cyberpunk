# Context Pack atual (tier-0)

**Finalidade:** único arquivo **mínimo** que a IA deve ler/re-ler para não esquecer o estado.  
**Gerado após:** sessão **010** · **Próxima:** **011** (`sessao_resumo_011.md`)  
**Branch:** `feature/linha-estavel`  
**Atualizado:** 13 de Julho de 2026

> **Não é o board.** Detalhe em `board/board_campanha.md`.  
> Fatos estáveis: [sistema/fatos_duros.md](../sistema/fatos_duros.md).  
> Comandos: [sistema/comandos_jogador.md](../sistema/comandos_jogador.md).

---

## NOW

| Campo | Valor |
| ----- | ----- |
| Data in-game | **09/07/2026** |
| Período | Final da tarde → próximo marco **10/07 manhã** |
| Região | **Badlands** |
| Local específico | Acampamento Pack Nômade — oficina / tenda Ryan & Valk |
| Facção / base local | Pack Badlands (hospedagem) |
| Cena / gancho | Scav de **containers** (E010); Valk organiza 2–3 veículos |
| Prioridade | **E010** — scav containers → depois protótipo casas |
| Segredos ativos | Casas modulares — **segredo** no pack (F11, L03) |

### Cena de abertura sugerida

**Manhã 10/07 — área de saída do Pack.** Time de scav de containers. Ryan decide partida (recon, formação).

---

## Fatos duros em vigor (não negociar)

| ID | Resumo |
| -- | ------ |
| F01–F02 | Branch `feature/linha-estavel`; arquivos = SoT |
| **F03** | Warden = drone **terrestre** scorpion (**não voa**) |
| **F04** | **Stitch** = Stephania (crew); **Doc** = Elisa Moreau (passado) |
| F07 | Ryan × Valk consolidados |
| F08 | Mule = de Valk; equipe Valk + Mule |
| **F11** | Casas modulares secretas até revelação |
| **L01** | No Pack: Reyes líder; Tio Gringo forja |
| **L02** | Scav materiais 05/07 OK; containers pendentes (E010); Node andando |
| **L03** | Peças na oficina sem revelar propósito aos alunos/Tio Gringo |

Lista completa: [fatos_duros.md](../sistema/fatos_duros.md).

---

## Pendências quentes

| ID | Uma linha |
| -- | --------- |
| **E010** | Scav containers (10/07) — Valk / 2–3 veículos |
| E012 | Montagem protótipo + revelação (após E010) |
| E007 | Badlands Node (água + biodigestor) |
| E008 | Vigilância residual Raffen |
| E011 | Visita Doc **Moreau** (Elisa); Valk junto — **não** Stitch |
| E001/E006 | Biotechnica latente |

---

## O que acabou de acontecer (010 — 1 parágrafo)

Scav de materiais limpa (Valk, Rusty, Jax); linha de produção de peças (segredo); Node/destilaria/estufa avançando; vínculo Valk reforçado; visita à Doc Moreau prometida.

Detalhe: [sessao_resumo_010.md](sessao_resumo_010.md).

---

## Carga de contexto (tiers)

| Tier | Quando | O que ler |
| ---- | ------ | --------- |
| **0** | Sempre / `[Refresh contexto]` | **Este arquivo** → `fatos_duros` → `board` se divergir |
| **1** | Cena Badlands Pack (agora) | `event_queue.md`, `relacionamentos/ryan_relacionamentos.md` (+ Valk se em cena), `facoes/pack_badlands.md` se conflito local |
| **2** | Sob demanda | `registro_arquivos.md` → ficha, job, pulso, guarda-roupa… |

**Não** carregar a campanha inteira. **Não** carregar pulso Pack se a região do NOW for Night City.

### Se a região mudar

Atualizar só a tabela NOW + tier-1; ver [fatos_duros § contexto local](../sistema/fatos_duros.md).

---

## RAW (sandbox falhou?)

Base: `https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/`

| Arquivo |
| ------- |
| `logs/context_pack_atual.md` |
| `sistema/fatos_duros.md` |
| `board/board_campanha.md` |
| `logs/handoff_atual.md` |
| `event_queue.md` |
| `logs/sessao_resumo_010.md` |
| `sistema/comandos_jogador.md` |

---

## Confirmação de boot (formato fixo)

```
Boot OK · 09/07/2026 · Badlands/Pack · prioridade: E010 scav containers · próximo resumo: 011
```

Hierarquia: **RAW/repo > sandbox > memória de chat**.

---

## Referências

- [Handoff](handoff_atual.md) · [Board](../board/board_campanha.md) · [Dashboard](../sistema/dashboard_contexto.md)
- [Comandos](../sistema/comandos_jogador.md) · [Novo chat](../sistema/novo_chat_procedimento.md)
