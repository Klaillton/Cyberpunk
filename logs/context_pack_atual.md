# Context Pack atual (tier-0)

**Finalidade:** único arquivo **mínimo** que a IA deve ler/re-ler para não esquecer o estado.  
**Gerado após:** sessão **017** · **Próxima:** **018** (`sessao_resumo_018.md`)  
**Branch:** `feature/linha-estavel`  
**Atualizado:** 24 de Julho de 2026 (final de tarde / início de noite)

> **Não é o board.** Detalhe em `board/board_campanha.md`.  
> **Arco + off-screen (L1):** [board/arco_ativo.md](../board/arco_ativo.md) — sob demanda / se estagnar.  
> Fatos estáveis: [sistema/fatos_duros.md](../sistema/fatos_duros.md).  
> Comandos: [sistema/comandos_jogador.md](../sistema/comandos_jogador.md).

---

## MOTOR (todo turno de RP)

1. **Não ecoar** o PC (≤2 linhas). Se descreveu procedimento/SOP → pular para **resultado**.  
2. **Delta** = **maior parte** da resposta (~≥60%): intel, NPC, tempo com efeito, pressão AGENDA.  
3. Em `OPERAÇÃO` / `VIAGEM`: **resultado primeiro** (não espelhar o plano).  
4. **VIAGEM limpa (N9):** sem anomalia/AGENDA no caminho → **fechar chegada** (sem filler de marcha).  
5. Fonte de pressão: **AGENDA DA CENA** → [arco_ativo](../board/arco_ativo.md) (L1 + off-screen + §7 SHOW) → pendências → `event_queue` (F10).  
6. Local novo / ação no terreno → bloco **AMBIENTE** ([cena_ambientacao](../sistema/cena_ambientacao_ganchos.md)).  
7. Escorregou? `[Motor de cena]` / `[Anti-eco]` · Estagnou? `[Avançar cena]` / `[Pressão]` · Lugar opaco? `[Ambientar]`.

Detalhe: [motor_cena_1pager.md](../sistema/motor_cena_1pager.md) · [cena_ambientacao_ganchos.md](../sistema/cena_ambientacao_ganchos.md)

---

## NOW

| Campo | Valor |
| ----- | ----- |
| Data in-game | **24/07/2026** |
| Período | Final de tarde / início de noite |
| Região | **Badlands** |
| Local específico | Cânion com fio de água corrente (acampamento leve) |
| Facção / base local | Nenhum (em deslocamento) |
| Cena / gancho | Acampamento noturno no cânion após tentativa de contato NC sem resposta |
| Prioridade | Manhã 25/07 — decidir se permanece, tenta contato de novo ou muda de posição; manter discrição |
| Segredos ativos | Casas modulares — pack geral ainda sem revelação oficial completa |

### Cena de abertura sugerida

**Manhã 25/07 — Cânion.** Canais ainda mudos. Ryan, Valk, Lira e Sasha no acampamento leve. Vespas em perímetro. O que Ryan faz?

---

## AGENDA DA CENA (anti-estagnação)

| # | Gancho (1 linha) | Quem age se idle | Se Ryan idle / mood ≥3 turnos → o narrador faz |
| - | ---------------- | ---------------- | ---------------------------------------------- |
| 1 | **B1** Decisão manhã 25/07: fica / 2º ping Steel-Sparrow / move posição | Valk | Valk **fala** preferência + horário (discrição); 1 alternativa |
| 2 | **B2** Off-screen: Steel/Sparrow (relógio 25–26/07) — silêncio tem estado, não é vazio | Mundo / rádio | 1 batida: ACK parcial, “não agora”, ruído útil, **ou** silêncio *com custo de tempo* — ver [arco_ativo](../board/arco_ativo.md) §3.3 |
| 3 | Lira (aberta) / Sasha (reservada) — residual **com fala** | Lira | 1 pergunta audível (drone / amanhã / Pack); Sasha reage; **sem** murmúrio vazio |

| Campo | Valor |
| ----- | ----- |
| **Modo atual** | DOWNTIME / VIAGEM (acampamento) |
| **Turnos sem delta (estimado)** | 0 |
| **Região / local (NOW)** | Badlands · Cânion (acampamento leve) |
| **Arco L1** | E015 espera pós-ping · [arco_ativo.md](../board/arco_ativo.md) |

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
| **Novo** | Modelo 3D externo da base militar coletado (21/07) |
| **Novo** | Lira + Sasha no acampamento 24/07 (todos no Mule); Lira com abertura reforçada |
| **F18** | Ruleset **v1.3.0** · 017+ · sem retcon 001–016 · [regras_red](../sistema/regras_red/00_integridade_regras.md) · [ryan_loadout](../fichas/ryan_loadout.md) |
| **F19** | Agents: Vault implant + Profissional subdermal + Honeypot visível + Arbiter/Watchdog (≠ Warden drone) · [agent_security](../plans/agent_security.md) |

Lista completa: [fatos_duros.md](../sistema/fatos_duros.md).

---

## Pendências quentes

| ID | Uma linha |
| -- | --------- |
| **E015** | Viagem NC (c/ Valk) — ping Steel/Sparrow 24/07 **sem resposta**; off-screen: Kaz monta crew; Steel/Sparrow no relógio 25–26/07 ([arco_ativo](../board/arco_ativo.md)) |
| **E019** | Olaria + desidratador + cogeração forja — ideia delegada ao Pack (23/07) |
| **E012** | Interno + móveis casas; possível revelação/escala |
| E007 | Badlands Node |
| E008 | Vigilância residual Raffen |
| E011 | Visita Doc **Moreau** (Elisa); Valk junto |
| E001/E006 | Biotechnica latente |
| Tutoria | Valk + Sasha/Lira (Lira aberta após 24/07, Sasha reservada; ambas no acampamento) |
| Novo | Enxame mini-drones (ideia + sondagem materiais) |
| Novo | Modelo 3D da base militar (estudo posterior) |

---

## O que acabou de acontecer (017 — 1 parágrafo)

24/07: saída do Pack, parada intermediária com intimidade Ryan×Valk, conversa e drone-play com Lira, tentativas de contato Steel e Sparrow (mensagem `RVW30sG1mBL_P?`) sem resposta, deslocamento até cânion com água, acampamento, banho e refeição, final de tarde/noite no local. Canais em recepção passiva e mudos.

Detalhe: [sessao_resumo_017.md](sessao_resumo_017.md)

---

## Confirmação de boot (formato fixo)

```
Boot OK · 24/07/2026 final de tarde · Cânion Badlands · prioridade: manhã 25/07 decidir posição/contato · próximo resumo: 018 · Ruleset 1.3.0
```

Hierarquia: **RAW/repo > sandbox > memória de chat**.
