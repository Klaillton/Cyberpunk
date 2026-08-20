# Context Pack atual (tier-0)

**Finalidade:** único arquivo **mínimo** que a IA deve ler/re-ler para não esquecer o estado.  
**Gerado após:** sessão **021** · **Próxima:** **022** (`sessao_resumo_022.md`)  
**Branch:** `feature/linha-estavel`  
**Atualizado:** ~30 de Julho de 2026 (noite) — Pack Badlands · dormindo na rede

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
9. **Rodapé OOC:** depois da cena, linha em branco + `ctrl N/90`. +2 por resposta sua. Boot = `ctrl 2/90`. Perdeu = `ctrl ?/90`. Não narrar; não é chrome/Agent; ninguém na cena vê; não expandir; não mudar o ritmo por causa do número.

Detalhe: [motor_cena_1pager.md](../sistema/motor_cena_1pager.md)

---

## NOW

| Campo | Valor |
| ----- | ----- |
| Data in-game | **~30/07/2026** |
| Período | Noite (Pack) · dormindo na rede |
| Região | **Badlands / Pack** |
| Local específico | Rede perto da tenda (área das tendas) |
| Facção / base local | Pack Nômade Badlands |
| Cena / gancho | 1º pacote do ad coletado; intermediário em 48–72h; refrigeração módulo pendente; plano base militar com Valk |
| Prioridade | (1) Intermediário ad (48–72h) (2) Refrigeração módulo + 2º voo (3) Esboço plano base militar |
| Segredos ativos | Casas modulares — pack geral sem revelação completa; convite NC a Sasha/Lira ainda delicado |

### Cena de abertura sugerida

**Pack — manhã 31/07.**  
Módulo de sinal funcionou (1º pacote anônimo recebido). Ad continua no ar. Intermediário possível em 48–72h. Ryan vai melhorar refrigeração (isobutano). Valk monta esboço do plano da base militar. Residual íntimo alto.

---

## AGENDA DA CENA (anti-estagnação)

| # | Gancho (1 linha) | Quem age se idle | Se Ryan idle / mood ≥3 turnos → o narrador faz |
| - | ---------------- | ---------------- | ---------------------------------------------- |
| 1 | Refrigeração módulo (isobutano) + possível 2º voo | Valk / Tio | Valk pergunta se o módulo já está pronto ou Tio oferece o isobutano |
| 2 | Intermediário do ad (48–72h a partir de 30/07 ~17h) | Mundo / fixer | Nota de tempo ou burst |
| 3 | Esboço plano base militar (Valk) | Valk | Valk apresenta rascunho ou cobra definição de time |

| Campo | Valor |
| ----- | ----- |
| **Modo atual** | DOWNTIME / Pack (pós-coleta) |
| **Turnos sem delta (estimado)** | 0 |
| **Região / local (NOW)** | Badlands · Pack |
| **Arco L1** | E015 (1º pacote recebido; intermediário pendente) · [arco_ativo.md](../board/arco_ativo.md) |

---

## Fatos duros em vigor (não negociar)

| ID | Resumo |
| -- | ------ |
| F01–F02 | Branch `feature/linha-estavel`; arquivos = SoT |
| **F03** | Warden = drone **terrestre** scorpion (**não voa**) |
| **F04** | **Stitch** = Stephania (crew); **Doc** = Elisa Moreau (passado) |
| **F14** | **Scout** (pack) ≠ **Jax "Razor" Kane** (crew NC) |
| **F15** | Valk **não** chama Ryan de “herói” / “herói solitário” |
| F07 | Ryan × Valk consolidados (**acordo comunicação ops 019** + intimidade 020/021) |
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
| **E015** | 1º pacote ad coletado (30/07); intermediário 48–72h; residual **Lina Park** sem ACK; **Marcus Rivera** mudo; Kaz escondido |
| **Módulo Condor** | Teste + ajustes ok; refrigeração (isobutano) pendente para 2º voo |
| **Base militar** | Esboço de plano com Valk; Ryan decide entrada solo após ver de perto |
| **E019** | Olaria/cogeração — Pack (background) |
| **E012** | Casas interno / revelação pack |
| Ideia Reyes | Assistente cobra mimética (conceito evoluiu; tempo livre) |

---

## O que acabou de acontecer (021 — 1 parágrafo)

29–30/07 Pack: Teste integrado + ajustes do módulo Condor concluídos. Rede construída. Intimidade forte. Em 30/07 o Condor voou na janela 15h–17h e coletou o 1º pacote do ad anônimo (mensagem: não forçar Sparrow/Steel; intermediário em 48–72h). Ad permanece no ar. Débito de 300 ed aplicado. Refrigeração marcada para 31/07; Valk fica com o esboço do plano da base militar. Dormiram na rede.

Detalhe: [sessao_resumo_021.md](sessao_resumo_021.md)

---

## Confirmação de boot (formato fixo)

```
Boot OK · ~30/07/2026 noite · Pack Badlands · prioridade: intermediário ad 48–72h + refrigeração módulo + plano base · próximo resumo: 022 · Ruleset 1.3.0
```

Rodapé da mesma resposta (OOC):

```
ctrl 2/90
```

Hierarquia: **RAW/repo > sandbox > memória de chat**.
