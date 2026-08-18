# Context Pack atual (tier-0)

**Finalidade:** único arquivo **mínimo** que a IA deve ler/re-ler para não esquecer o estado.  
**Gerado após:** sessão **020** · **Próxima:** **021** (`sessao_resumo_021.md`)  
**Branch:** `feature/linha-estavel`  
**Atualizado:** ~29 de Julho de 2026 (início da tarde) — Pack Badlands

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
8. **Chat novo:** este pack + handoff; **não** continuar threads longos degradados.

Detalhe: [motor_cena_1pager.md](../sistema/motor_cena_1pager.md)

---

## NOW

| Campo | Valor |
| ----- | ----- |
| Data in-game | **~29/07/2026** |
| Período | Início da tarde (Pack) |
| Região | **Badlands / Pack** |
| Local específico | Pack (caminho oficina → refeitório; módulo na bancada) |
| Facção / base local | Pack Nômade Badlands |
| Cena / gancho | Módulo de sinal Condor pronto (hardware); falta teste integrado + voo 30/07 15h–17h; ad no ar |
| Prioridade | (1) Teste integrado módulo + voo Condor 30/07 (2) Possível 1º pacote do ad (3) Residual Sparrow |
| Segredos ativos | Casas modulares — pack geral sem revelação completa; convite NC a Sasha/Lira ainda delicado |

### Cena de abertura sugerida

**Pack — tarde 29/07 ou manhã 30/07.**  
Módulo de sinal (mochila Condor) montado e dry-fit feito. Dois ajustes menores pendentes. Janela Condor confirmada com Tio Gringo: 30/07 15h–17h. Ad anônimo no ar; primeiro pacote esperado em breve. Residual Lina Park sem ACK. Ryan + Valk com residual íntimo forte pós-020.  
Gancho: teste integrado / ajustes finais / o que Ryan faz até a janela.

---

## AGENDA DA CENA (anti-estagnação)

| # | Gancho (1 linha) | Quem age se idle | Se Ryan idle / mood ≥3 turnos → o narrador faz |
| - | ---------------- | ---------------- | ---------------------------------------------- |
| 1 | Teste integrado módulo + ajustes menores (costura / fluxo) | Valk / Tio | Valk cobra teste ou Tio pergunta se o pássaro voa amanhã |
| 2 | Janela Condor 30/07 15h–17h + possível 1º pacote ad | Mundo / fixer | Nota de tempo ou burst de rede |
| 3 | Residual Lina Park / Pack rotina | Contato / Lira | 1 batida útil de silêncio ou pergunta prática |

| Campo | Valor |
| ----- | ----- |
| **Modo atual** | DOWNTIME / Pack (preparação ops) |
| **Turnos sem delta (estimado)** | 0 |
| **Região / local (NOW)** | Badlands · Pack |
| **Arco L1** | E015 (ad ativo; coleta via Condor preparada) · [arco_ativo.md](../board/arco_ativo.md) |

---

## Fatos duros em vigor (não negociar)

| ID | Resumo |
| -- | ------ |
| F01–F02 | Branch `feature/linha-estavel`; arquivos = SoT |
| **F03** | Warden = drone **terrestre** scorpion (**não voa**) |
| **F04** | **Stitch** = Stephania (crew); **Doc** = Elisa Moreau (passado) |
| **F14** | **Scout** (pack) ≠ **Jax "Razor" Kane** (crew NC) |
| **F15** | Valk **não** chama Ryan de “herói” / “herói solitário” |
| F07 | Ryan × Valk consolidados (**acordo comunicação ops 019** + intimidade 020) |
| F08 | Mule = de Valk; equipe Valk + Mule |
| **F11** | Casas modulares — pack geral sem revelação oficial completa |
| **L01–L03** | Pack: Reyes, Tio Gringo, Container A, time produção no segredo parcial |
| **Novo** | Lira + Sasha: residual positivo 019 mantido |
| **F18** | Ruleset **v1.3.0** · 017+ · sem retcon 001–016 |
| **F19** | Agents: Vault / Profissional / Honeypot / Arbiter/Watchdog ≠ Warden |
| **F20** | **Sparrow** = Lina Park (NPC); **Steel** = Marcus Rivera (NPC) — **não** sistemas |

Lista completa: [fatos_duros.md](../sistema/fatos_duros.md).

---

## Pendências quentes

| ID | Uma linha |
| -- | --------- |
| **E015** | Ad anônimo no ar; módulo Condor pronto; voo 30/07 15h–17h; residual **Lina Park** sem ACK; **Marcus Rivera** mudo; Kaz escondido |
| **Módulo Condor** | Hardware pronto; falta Agent temporário + teste integrado + 2 ajustes menores |
| **E019** | Olaria/cogeração — Pack (background) |
| **E012** | Casas interno / revelação pack |
| E007 | Badlands Node |
| E008 | Raffen residual |
| E011 | Doc Moreau (c/ Valk) em NC |
| Ideia Reyes | Bola-assistente flutuante (conceito; tempo livre) |

---

## O que acabou de acontecer (020 — 1 parágrafo)

28–29/07 Pack: Ryan planejou e construiu módulo de sinal tipo mochila para o Condor (coleta anônima do pacote do ad). Tio Gringo reservou o pássaro para 30/07 15h–17h. Hardware funcional (SDR adaptado, ventilação passiva, placa reconstruída). Dry-fit ok com 2 ajustes menores. Intimidade forte com Valk (noite + manhã). Ideia de assistente flutuante para Reyes registrada como projeto futuro. Sessão fechada no caminho para o refeitório.

Detalhe: [sessao_resumo_020.md](sessao_resumo_020.md)

---

## Confirmação de boot (formato fixo)

```
Boot OK · ~29/07/2026 tarde · Pack Badlands · prioridade: teste módulo + voo Condor 30/07 + possível 1º pacote ad · próximo resumo: 021 · Ruleset 1.3.0
```

Hierarquia: **RAW/repo > sandbox > memória de chat**.
