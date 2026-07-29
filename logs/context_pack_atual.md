# Context Pack atual (tier-0)

**Finalidade:** único arquivo **mínimo** que a IA deve ler/re-ler para não esquecer o estado.  
**Gerado após:** sessão **014** · **Próxima:** **015** (`sessao_resumo_015.md`)  
**Branch:** `feature/linha-estavel`  
**Atualizado:** 21 de Julho de 2026

> **Não é o board.** Detalhe em `board/board_campanha.md`.  
> Fatos estáveis: [sistema/fatos_duros.md](../sistema/fatos_duros.md).  
> Comandos: [sistema/comandos_jogador.md](../sistema/comandos_jogador.md).  
> 1pager: [sistema/motor_cena_1pager.md](../sistema/motor_cena_1pager.md).

---

## MOTOR (todo turno de RP)

1. **Não ecoar** o PC (≤2 linhas). Se descreveu procedimento/SOP → pular para **resultado**.  
2. **Delta** = **maior parte** da resposta (~≥60%): intel, NPC, tempo com efeito, pressão AGENDA.  
3. Em `OPERAÇÃO` / `VIAGEM`: **resultado primeiro** (não espelhar o plano).  
4. Fonte de pressão: **AGENDA DA CENA** → pendências → `event_queue` (F10).  
5. Escorregou? `[Motor de cena]` / `[Anti-eco]` · Estagnou? `[Avançar cena]` / `[Pressão]`.

Detalhe: [diretrizes_narrador.md](../sistema/diretrizes_narrador.md) §7.1 · [motor_cena_1pager.md](../sistema/motor_cena_1pager.md)

---

## NOW

| Campo | Valor |
| ----- | ----- |
| Data in-game | **21/07/2026** |
| Período | Tarde |
| Região | **Badlands** |
| Local específico | Em deslocamento — observação leve de base militar |
| Facção / base local | Pack Badlands (hospedagem) |
| Cena / gancho | Ryan saiu sozinho para observação (máscara + Vespas + Warden). Voltar antes do escuro. |
| Prioridade | Observação base militar · Preparação viagem NC · Tutoria Sasha/Lira |
| Segredos ativos | Casas modulares — time produção + Tio Gringo sabem; pack geral ainda aguarda revelação oficial completa |

### Cena de abertura sugerida

**Tarde 21/07 — Badlands.** Ryan em deslocamento a pé para observação leve de base militar. Condições de Valk: rádio, Warden, voltar antes do escuro, virar se cheirar errado. Vespas + Warden em formação.

---

## Fatos duros em vigor (não negociar)

| ID | Resumo |
| -- | ------ |
| F01–F02 | Branch `feature/linha-estavel`; arquivos = SoT |
| **F03** | Warden = drone **terrestre** scorpion (**não voa**) |
| **F04** | **Stitch** = Stephania (crew); **Doc** = Elisa Moreau (passado) |
| **F14** | **Scout** (pack) ≠ **Jax "Razor" Kane** (crew NC) |
| **F15** | Valk **não** chama Ryan de “herói” / “herói solitário” (promessa 14/07; gatilho ativo) |
| F07 | Ryan × Valk consolidados; decisão conjunta de ir a Night City |
| F08 | Mule = de Valk; equipe Valk + Mule |
| **F11** | Casas modulares — pack geral ainda sem revelação oficial completa |
| **L01** | No Pack: Reyes líder; Tio Gringo forja |
| **L02** | E010 concluída; Container A no pack; Node andando |
| **L03** | Time de produção + Tio Gringo conhecem o projeto |
| **Novo** | Condor + Corujas operacionais (drones miméticos) |

Lista completa: [fatos_duros.md](../sistema/fatos_duros.md).

---

## Pendências quentes

| ID | Uma linha |
| -- | --------- |
| **E015** | Viagem / assuntos Ryan em Night City (com Valk) |
| **E012** | Interno + móveis casas; possível revelação/escala |
| **E013** | Caçada aves concluída (referência drones usada) |
| E007 | Badlands Node |
| E008 | Vigilância residual Raffen |
| E011 | Visita Doc **Moreau** (Elisa); Valk junto |
| E001/E006 | Biotechnica latente |
| Tutoria | Valk + Sasha/Lira (assistentes; intimidade: Lira aberta, Sasha reservada) |
| Novo | Enxame mini-drones (ideia + sondagem materiais) |

---

## AGENDA DA CENA (anti-estagnação)

> Schema genérico — instâncias do **NOW atual** (Badlands · trânsito / observação). Ao mudar de local, **reescrever**.  
> Motor: [diretrizes_narrador.md](../sistema/diretrizes_narrador.md) §7.1 · Comando: `[Avançar cena]` / `[Pressão]`.

| # | Gancho (1 linha) | Quem age se idle | Se Ryan idle / mood ≥3 turnos → o narrador faz |
| - | ---------------- | ---------------- | ---------------------------------------------- |
| 1 | Observação leve da base (janela até o escuro) | Mundo / drones | Fato perceptível (movimento, silhueta, rádio, tempo) sem forçar combate |
| 2 | Condições de Valk (rádio, Warden, virar se cheirar errado) | Valk (canal rádio se plausível) ou lembrete diegético | Pressão de tempo / check-in / risco se a luz baixar |
| 3 | Volta ao Pack antes do anoitecer · E015 em background | Pack off-screen (F10) | Rumor/lembrete só se canal (rádio, Condor, retorno) |

| Campo | Valor |
| ----- | ----- |
| **Modo atual** | OPERAÇÃO |
| **Turnos sem delta (estimado)** | 0 |
| **Região / local (NOW)** | Badlands · em deslocamento → base militar (observação leve) |

---

## O que acabou de acontecer (014 — 1 parágrafo)

Manhã 21/07: intimidade + café com Valk; ideia do enxame de mini-drones a partir de formigas; sondagem com Tomas (látex) e Mara (resina/seiva); Ryan se puxa do hiperfoco; decide sair sozinho para observação leve de base militar sob condições de Valk. Saiu equipado (máscara + Vespas + Warden).

Detalhe: [sessao_resumo_014.md](sessao_resumo_014.md)

---

## Carga de contexto (tiers)

| Tier | Quando | O que ler |
| ---- | ------ | --------- |
| **0** | Sempre / `[Refresh contexto]` | **Este arquivo** → `fatos_duros` → `board` se divergir |
| **1** | Cena Badlands Pack / trânsito | `event_queue.md`, `ryan_relacionamentos.md`, Valk, `npc_agencia_cena.md` se delegação/agência · Motor de cena §7.1 |
| **2** | Sob demanda | `registro_arquivos.md` → ficha, pulso, guarda-roupa… |

---

## RAW (sandbox falhou?)

Base: `https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/`

| Arquivo |
| ------- |
| `logs/context_pack_atual.md` |
| `sistema/fatos_duros.md` |
| `board/board_campanha.md` |
| `logs/handoff_atual.md` |
| `logs/sessao_resumo_014.md` |
| `sistema/comandos_jogador.md` |

---

## Confirmação de boot (formato fixo)

```
Boot OK · 21/07/2026 · Badlands (em trânsito) · prioridade: observação base militar + preparação NC · próximo resumo: 015
```

Hierarquia: **RAW/repo > sandbox > memória de chat**.

---

## Referências

- [Handoff](handoff_atual.md) · [Board](../board/board_campanha.md) · [Dashboard](../sistema/dashboard_contexto.md)
- [Comandos](../sistema/comandos_jogador.md) · [Agência NPC](../sistema/npc_agencia_cena.md) · [Motor de cena](../sistema/diretrizes_narrador.md)
