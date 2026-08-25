# Context Pack atual (tier-0)

**Finalidade:** único arquivo **mínimo** que a IA deve ler/re-ler para não esquecer o estado.  
**Gerado após:** sessão **022** · **Próxima:** **023** (`sessao_resumo_023.md`)  
**Branch:** `feature/linha-estavel`  
**Atualizado:** ~31 de Julho de 2026 (tarde) — Pack Badlands

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
9. **Rodapé OOC:** depois da cena, linha em branco + `ctrl N/90`. +2 por resposta sua. Boot = `ctrl 2/90`. Perdeu = `ctrl ?/90`. Não narrar; não é chrome/Agent; ninguém na cena vê.

Detalhe: [motor_cena_1pager.md](../sistema/motor_cena_1pager.md)

---

## NOW

| Campo | Valor |
| ----- | ----- |
| Data in-game | **~31/07/2026** |
| Período | Tarde (Pack) |
| Região | **Badlands / Pack** |
| Local específico | Setor de veículos / oficina (Mule recém-vistorado) |
| Facção / base local | Pack Nômade Badlands |
| Cena / gancho | Recon base concluído; intermediário ad ainda aberto; voo Condor pré-programado ~02/08 |
| Prioridade | (1) Intermediário ad (48–72h) (2) Voo Condor +58h / 4h (3) Decisão de entrada na base |
| Segredos ativos | Casas modulares — pack geral sem revelação completa; convite NC a Sasha/Lira ainda delicado |

### Cena de abertura sugerida

**Pack — tarde/noite 31/07.**  
Módulo refrigerado e pré-programado. Sasha/Lira cuidam da liberação do Condor. Perímetro externo da base mapeado e abandonado. Intermediário do ad ainda sem contato.

---

## AGENDA DA CENA (anti-estagnação)

| # | Gancho (1 linha) | Quem age se idle | Se Ryan idle / mood ≥3 turnos → o narrador faz |
| - | ---------------- | ---------------- | ---------------------------------------------- |
| 1 | Intermediário do ad (48–72h a partir de 30/07 ~17h) | Mundo / fixer | Nota de tempo ou burst |
| 2 | Voo Condor pré-programado (~02/08, 4h) | Sasha/Lira / Tio | Lembra da janela ou pede checagem da mochila |
| 3 | Base: intel externa ok; entrada ainda aberta | Valk | Valk cobra se entra solo, com time, ou espera |

| Campo | Valor |
| ----- | ----- |
| **Modo atual** | DOWNTIME / Pack (pós-recon) |
| **Turnos sem delta (estimado)** | 0 |
| **Região / local (NOW)** | Badlands · Pack |
| **Arco L1** | E015 (intermediário pendente) · [arco_ativo.md](../board/arco_ativo.md) |

---

## Fatos duros em vigor (não negociar)

| ID | Resumo |
| -- | ------ |
| F01–F02 | Branch `feature/linha-estavel`; arquivos = SoT |
| **F03** | Warden = drone **terrestre** scorpion (**não voa**) |
| **F04** | **Stitch** = Stephania (crew); **Doc** = Elisa Moreau (passado) |
| **F14** | **Scout** (pack) ≠ **Jax "Razor" Kane** (crew NC) |
| **F15** | Valk **não** chama Ryan de “herói” / “herói solitário” |
| F07 | Ryan × Valk consolidados (**acordo comunicação ops 019** + intimidade 020/021/022) |
| F08 | Mule = de Valk; equipe Valk + Mule |
| **F11** | Casas modulares — pack geral sem revelação oficial completa |
| **L01–L03** | Pack: Reyes, Tio Gringo, Container A, time produção no segredo parcial |
| **Novo** | Lira + Sasha: residual positivo 019/022 (favor Condor) |
| **F18** | Ruleset **v1.3.0** · 017+ · sem retcon 001–016 |
| **F19** | Agents: Vault / Profissional / Honeypot / Arbiter/Watchdog ≠ Warden |
| **F20** | **Sparrow** = Lina Park (NPC); **Steel** = Marcus Rivera (NPC) — **não** sistemas |

Lista completa: [fatos_duros.md](../sistema/fatos_duros.md).

---

## Pendências quentes

| ID | Uma linha |
| -- | --------- |
| **E015** | 1º pacote ad coletado (30/07); intermediário 48–72h; residual **Lina Park** sem ACK; **Marcus Rivera** mudo; Kaz escondido |
| **Módulo Condor** | Refrigeração ok; pré-programado +58h / 4h; Sasha/Lira liberam |
| **Base militar** | Perímetro externo mapeado (abandonado); entrada (solo ou time) ainda aberta |
| **E019** | Olaria/cogeração — Pack (background) |
| **E012** | Casas interno / revelação pack |
| Ideia Reyes | Assistente cobra mimética (conceito; tempo livre) |

---

## O que acabou de acontecer (022 — 1 parágrafo)

31/07 Pack: refrigeração passiva do módulo Condor concluída; Condor reservado +58h/4h e pré-programado; Sasha/Lira aceitam liberar o voo. Ryan+Valk fizeram recon externo completo da base militar (quatro lados, sem entrada): abandonada, sem EM, sem rastros. Acordo 019 reforçado. Mule limpo e vistorado. Intermediário do ad ainda sem contato.

Detalhe: [sessao_resumo_022.md](sessao_resumo_022.md)

---

## Confirmação de boot (formato fixo)

```
Boot OK · ~31/07/2026 tarde · Pack Badlands · prioridade: intermediário ad + voo Condor ~02/08 + decisão base · próximo resumo: 023 · Ruleset 1.3.0
```

Hierarquia: **RAW/repo > sandbox > memória de chat**.
