# Context Pack atual (tier-0)

**Finalidade:** único arquivo **mínimo** que a IA deve ler/re-ler para não esquecer o estado.  
**Gerado após:** sessão **018** · **Próxima:** **019** (`sessao_resumo_019.md`)  
**Branch:** `feature/linha-estavel`  
**Atualizado:** ~26 de Julho de 2026 (tarde / início de noite) — Badlands, perto de NC

> **Não é o board.** Detalhe em `board/board_campanha.md`.  
> **Arco + off-screen (L1):** [board/arco_ativo.md](../board/arco_ativo.md) — sob demanda / se estagnar.  
> Fatos estáveis: [sistema/fatos_duros.md](../sistema/fatos_duros.md).  
> Comandos: [sistema/comandos_jogador.md](../sistema/comandos_jogador.md).  
> Ambientação: [cena_ambientacao_ganchos.md](../sistema/cena_ambientacao_ganchos.md).

---

## MOTOR (todo turno de RP)

1. **Não ecoar** o PC (≤2 linhas). Se descreveu procedimento/SOP → pular para **resultado**.  
2. **Delta** = **maior parte** da resposta (~≥60%): intel, NPC, tempo com efeito, pressão AGENDA.  
3. Em `OPERAÇÃO` / `VIAGEM`: **resultado primeiro** (não espelhar o plano).  
4. **VIAGEM limpa (N9):** sem anomalia/AGENDA no caminho → **fechar chegada** (sem filler de marcha).  
5. Fonte de pressão: **AGENDA DA CENA** → [arco_ativo](../board/arco_ativo.md) (L1 + off-screen + §7 SHOW) → pendências → `event_queue` (F10).  
6. Local novo / ação no terreno → bloco **AMBIENTE** ([cena_ambientacao](../sistema/cena_ambientacao_ganchos.md)).  
7. Escorregou? `[Motor de cena]` / `[Anti-eco]` · Estagnou? `[Avançar cena]` / `[Pressão]` · Lugar opaco? `[Ambientar]`.  
8. **Chat novo:** este pack + handoff; **não** continuar o thread web VIII (~120 msgs).

Detalhe: [motor_cena_1pager.md](../sistema/motor_cena_1pager.md)

---

## NOW

| Campo | Valor |
| ----- | ----- |
| Data in-game | **~26/07/2026** |
| Período | Tarde / início de noite (luz baixa) |
| Região | **Badlands** (borda / aproximação NC) |
| Local específico | Em deslocamento / prestes a **zona industrial abandonada** (cobertura + rotas de fuga) |
| Facção / base local | Nenhum (viagem; Pack atrás) |
| Cena / gancho | Plano combinado: Mule + Ryan/Valk/Lira/Sasha → industrial; **pesquisa Agent agora**; **ad amanhã cedo** se fizer sentido |
| Prioridade | (1) Chegada industrial + AMBIENTE (2) **B2** — resposta de **Lina “Sparrow” Park** e/ou **Marcus “Steel” Rivera** (NPCs; residual Sparrow sem resposta está **atrasado**) (3) pesquisa; sem ops solo isolado |
| Segredos ativos | Casas modulares — pack geral sem revelação completa; convite NC a Sasha/Lira ainda delicado/secreto entre elas |

### Cena de abertura sugerida

**Chegada — zona industrial abandonada (Badlands/borda NC).**  
Mule com os quatro. Luz baixa. Canal da **Lina “Sparrow” Park** ainda só residual (ela **não** respondeu — SoT: **resolver B2**).  
**Sparrow = NPC pessoa**, não sistema/drone. Bloco **AMBIENTE** + 1 batida + gancho. O que Ryan faz?

---

## AGENDA DA CENA (anti-estagnação)

| # | Gancho (1 linha) | Quem age se idle | Se Ryan idle / mood ≥3 turnos → o narrador faz |
| - | ---------------- | ---------------- | ---------------------------------------------- |
| 1 | Chegada industrial: cobertura, saídas, linha de rádio, riscos | Mundo / Valk | Bloco AMBIENTE + Valk marca ponto de estacionamento/extração |
| 2 | **B2 (atrasado):** **Sparrow** (Lina Park) residual **sem resposta** — relógio 25–26 já passou | Contato NPC / rádio | **Resolver:** resposta dela, “não agora”, ou silêncio útil **com custo** — proibido só “canal ainda respira” |
| 3 | Pesquisa Agent agora; ad amanhã; Valk **não** aceita Ryan isolado sem plano de extração | Valk | Cobra escopo da pesquisa ou fecha janela de tempo |

| Campo | Valor |
| ----- | ----- |
| **Modo atual** | VIAGEM → OPERAÇÃO (chegada industrial) |
| **Turnos sem delta (estimado)** | 0 |
| **Região / local (NOW)** | Badlands · zona industrial (chegada) |
| **Arco L1** | E015 aproximação NC · B2 canal pendente · [arco_ativo.md](../board/arco_ativo.md) |

---

## Fatos duros em vigor (não negociar)

| ID | Resumo |
| -- | ------ |
| F01–F02 | Branch `feature/linha-estavel`; arquivos = SoT |
| **F03** | Warden = drone **terrestre** scorpion (**não voa**) |
| **F04** | **Stitch** = Stephania (crew); **Doc** = Elisa Moreau (passado) |
| **F14** | **Scout** (pack) ≠ **Jax "Razor" Kane** (crew NC) |
| **F15** | Valk **não** chama Ryan de “herói” / “herói solitário” |
| F07 | Ryan × Valk consolidados (atrato ops 018 resolvido em parte; seguem juntos) |
| F08 | Mule = de Valk; equipe Valk + Mule |
| **F11** | Casas modulares — pack geral sem revelação oficial completa |
| **L01–L03** | Pack: Reyes, Tio Gringo, Container A, time produção no segredo parcial |
| **Novo** | Lira + Sasha na viagem; Sasha com abertura forte (018); Lira cooperativa |
| **F18** | Ruleset **v1.3.0** · 017+ · sem retcon 001–016 |
| **F19** | Agents: Vault / Profissional / Honeypot / Arbiter/Watchdog ≠ Warden |
| **F20** | **Sparrow** = Lina Park (NPC); **Steel** = Marcus Rivera (NPC) — **não** sistemas |

Lista completa: [fatos_duros.md](../sistema/fatos_duros.md).

---

## Pendências quentes

| ID | Uma linha |
| -- | --------- |
| **E015** | Aprox. NC — industrial + pesquisa; **Lina “Sparrow” Park** residual sem resposta (B2); **Marcus “Steel” Rivera** mudo; Kaz escondido · [fichas](../fichas/npc/lina_park.md) |
| **E019** | Olaria/cogeração — Pack (Lira pode levar ideia ao voltar) |
| **E012** | Casas interno / revelação pack |
| E007 | Badlands Node |
| E008 | Raffen residual |
| E011 | Doc Moreau (c/ Valk) em NC |
| E001/E006 | BT latente |
| Tutoria / Lira-Sasha | Ambas no Mule; Sasha: não sumir sem avisar |
| Ad | Planejado para **amanhã cedo** (se ainda fizer sentido após pesquisa) |

---

## O que acabou de acontecer (018 — 1 parágrafo)

24–26/07: cânion → viagem multi-dia (caça, conversa Sasha, Agent: Sparrow residual sem ACK, OPSEC alta); atrito Ryan×Valk sobre ops solo; plano final: todos no Mule para zona industrial abandonada — pesquisa agora, ad amanhã. Thread RP web encerrado por comprimento/qualidade.

Detalhe: [sessao_resumo_018.md](sessao_resumo_018.md)

---

## Confirmação de boot (formato fixo)

```
Boot OK · ~26/07/2026 tarde · Badlands/borda NC · industrial · prioridade: AMBIENTE + B2 (Sparrow/Steel NPCs) + pesquisa · próximo resumo: 019 · Ruleset 1.3.0
```

Hierarquia: **RAW/repo > sandbox > memória de chat**.
