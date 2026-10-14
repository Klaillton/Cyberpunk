# Context Pack atual (tier-0)

**Finalidade:** único arquivo **mínimo** que a IA deve ler/re-ler para não esquecer o estado.  
**Gerado após:** sessão **029** · **Próxima:** **030** (`sessao_resumo_030.md`)  
**Branch:** `feature/linha-estavel`  
**Atualizado:** ~05 de Agosto de 2026 (noite) — Mule · luzes de Night City à vista

> **Não é o board.** Detalhe em `board/board_campanha.md`.  
> **Arco + off-screen (L1):** [board/arco_ativo.md](../board/arco_ativo.md) — sob demanda / se estagnar.  
> Fatos estáveis: [sistema/fatos_duros.md](../sistema/fatos_duros.md).  
> Comandos: [sistema/comandos_jogador.md](../sistema/comandos_jogador.md).  
> Ambientação: [cena_ambientacao_ganchos.md](../sistema/cena_ambientacao_ganchos.md).

---

## MOTOR (todo turno de RP)

1. **Boca — ramo antes da frase.** O ramo de cima não vaza para o de baixo. Quem fala muda o vocabulário, não o ramo. Um exemplo dentro de cada ramo, no bloco Boca e em [arco §7.1](../board/arco_ativo.md).
   - **Rádio / operação / combate** (job, ou o Pack ouvindo o trabalho): curta, seca, pessoa. Resultado primeiro.
   - **Pack social** (refeitório, oficina, pátio, corredor, Reyes, Mule parado): conversa diegética e fluida. Uma fala de gente, corpo no meio. Pode ter mais corpo. Cada um pela ficha.
   - **A sós** (tenda, banho, cama, banco do Mule em estrada): uma fala, um fôlego, diegética e fluida. Pode ter mais corpo. Quieta pode. Selo de duas frases não serve. Chip, Reyes e hop não entram nesta boca. A frase pede, provoca, responde ou desvia.
2. **Não ecoar** o PC: ≤2 linhas **só** para confirmar a ação dele. Esse teto não mede a fala do NPC. SOP multi-passo → outcomes (N8). Resultado-primeiro **só** no ramo de rádio/ops/combate.
3. **Delta** = **maior parte** (~≥60%). Nos ramos Pack social e a sós: SHOW + fala do ramo = delta. A fala desses ramos é diegética e fluida. Corpo: 3–6 linhas é **piso**, e pode ter mais. O extra é lugar, gesto e calor, não discurso. A mesma mão entra numa frase só. Não precisa de burst nem relógio.
4. **VIAGEM limpa (N9):** sem anomalia/AGENDA no caminho → **fechar chegada** (sem filler de marcha).
5. **Anti-máquina:** sem *nome de regra* na prosa. Humor, medo, cansaço, recusa = obrigatório. “Três coisas” = ultimato de condições, não teto de frase. Ryan pode cortar; ninguém copia o corte. Trava: `[Voz: ramo antes da frase. Ryan pode cortar. NPC não copia o corte.]`
6. Fonte de pressão: **AGENDA DA CENA** → [arco_ativo](../board/arco_ativo.md) (L1 + off-screen + §7 SHOW) → pendências → `event_queue` (F10).
7. Local novo / ação no terreno → bloco **AMBIENTE** ([cena_ambientacao](../sistema/cena_ambientacao_ganchos.md)). Checklist interno; saída = uma situação (N13). Não gavetas na tela (`Cobertura:`, `EM:`). Não omitir o dado.
8. Escorregou? `[Motor de cena]` / `[Anti-eco]` · Estagnou? `[Avançar cena]` / `[Pressão]` · Lugar opaco? `[Ambientar]`.
9. **Chat novo:** este pack + handoff; **não** continuar threads longos degradados.
10. **Rodapé OOC:** depois da cena, linha em branco + `ctrl N/90`. +2 por resposta sua. Boot = `ctrl 2/90`. Perdeu = `ctrl ?/90`. Não narrar; não é chrome/Agent; ninguém na cena vê.

Detalhe: [motor_cena_1pager.md](../sistema/motor_cena_1pager.md) · N13: [diretrizes_narrador.md](../sistema/diretrizes_narrador.md) §5.2

---

## NOW

| Campo | Valor |
| ----- | ----- |
| Data in-game | **~05/08/2026** |
| Período | Noite |
| Região | **Estrada / Mule** (luzes de Night City à vista) |
| Local específico | Mule. Valkirya no volante. Warden no corpo. Chip E015 **lacre aberto** (token) no Warden (compartimento morto). Pill no fundo do Mule (médio; **não é mochila**). Vespas no Mule. |
| Facção / base local | Pack Nômade Badlands (saindo) |
| Cena / gancho | Janela do hop NC **05/08 após 21h**. Ainda não é o ponto. Debrief Reyes pendente na volta. |
| Prioridade | (1) Ponto do hop (2) Debrief na volta (3) Não forçar Sparrow/Steel |
| Segredos ativos | Casas modulares — pack geral sem revelação completa; convite NC a Sasha/Lira fechado por Valkirya |

### SET NOW

`sistema/set_lugares.md` § **mule** (ou estrada). Não abrir o arquivo inteiro.

Mule em movimento. Valkirya no volante. Banco do Ryan. Warden no corpo. Pill no fundo do Mule. Vespas no Mule. Luzes de NC à vista. Ainda não é o ponto.

Pack deixado na saída: [context_pack_pack.md](context_pack_pack.md). **Não** abrir no boot nem no Refresh.

## NORTE (orientação, não quest log)

> Horizontes. **Não** é trilho. Se o pack divergir do `arco_ativo`, **vence este pack**.

| Horizonte | Norte |
| --------- | ----- |
| **Curto** (hoje / sessão) | Chegar ao ponto do hop NC 05/08 após 21h. |
| **Médio** (1–3 sessões) | Hop NC (E015, token no chip). Sparrow/Steel/Kaz **não** forçar. Voltar ao Pack. Debrief Reyes. |
| **Longo** (campanha) | Pack casas/Node/olaria. Doc E011. Crew NC. |
| **Fora agora** | Base militar. Raid Cutter. Reabrir jantar 023 / SOP Condor / caixa 101 / canyon. |

### Cena de abertura sugerida (030)

**Não continuar o chat da 029.**  
05/08 noite, Mule, luzes de NC à vista. Ainda não é o ponto. Valkirya no volante. Residual íntimo alto. Não reabrir jantar 023 nem SOP Condor nem a caixa da 101 nem o canyon.

---

## AGENDA DA CENA (anti-estagnação)

| # | Gancho (1 linha) | Quem age se idle | Se Ryan idle / mood ≥3 turnos → o narrador faz |
| - | ---------------- | ---------------- | ---------------------------------------------- |
| 1 | Ponto do hop NC (token no chip) | Mundo / intermediário | Relógio do hop; sem voz; sem ping antigo |
| 2 | Debrief Reyes na volta | Reyes / Valk | Reyes puxa o debrief no pátio / oficina na volta |
| 3 | Estrada a sós até o ponto | Valk | SHOW banco / volante; sem reabrir canyon |

| Campo | Valor |
| ----- | ----- |
| **Modo atual** | Estrada → hop |
| **Turnos sem delta (estimado)** | 0 |
| **Região / local (NOW)** | Estrada · Mule · luzes NC à vista |
| **Arco L1** | E015 (chip aberto · hop NC 05/08 21h) · [arco_ativo.md](../board/arco_ativo.md) |

**Trava 023 (não reabrir):** base = mensagem → manhã seguinte; 019 em vigor. **Não** reabrir o jantar como briga. **Não** reabrir SOP Condor como tutorial. **Não** reabrir o canyon do corte.

### SOP Condor (SoT 020–022 — não carimbar na prosa)

- Condor = transporte cego. Coleta = Agent na mochila. Ar = silêncio + abort mínimo. **Unmanned.** Spec: [drone - condor.md](../fichas/drone%20-%20condor.md).
- Sasha/Lira = voo/visual no **gancho/visor**. Não abrem módulo. Não anunciam pacote.
- Valk no gancho ok; **não** autentica o Agent.
- Ryan recupera o Agent. Só ele diz se veio pacote.

### Boca (boot — ramo antes da frase)

NOW = Mule a sós em estrada → **ramo 3**. Pátio / Reyes / refeitório → **ramo 2**. Residual íntimo **alto**. No job, ramo 1. Chat **023** não se herda.

1. **Rádio / ops / combate** — curta, seca, pessoa. Resultado primeiro. *“Mule no leste, abort no rádio. Eu no volante. Tu marca a janela.”*
2. **Pack social** — conversa diegética e fluida; uma fala de gente; corpo no meio; pode ter mais corpo; cada um pela ficha. Reyes: *“Camp eu não tenho. Corredor, sim. O céu amanhã me diz onde corto — um, não um raid. Tu some de novo no mesmo dia. A 101 não é minha estrada.”*
3. **A sós** — uma fala, um fôlego, diegética e fluida. Pode ter mais corpo. Quieta pode. Selo de duas frases não serve. Chip, Reyes e hop fora desta boca. Modelo de fôlego (copia o tamanho e o corpo no meio; não copia o assunto nem esta cena): *“Continua.” A palma fica na nuca. “Se eu rir, a gente sai da estrada.”* **Teste:** a frase pede, provoca, responde ou desvia. A mesma mão entra numa frase só. As 3–6 linhas são o lugar (calor, poeira, motor), e o corpo pode passar disso.

Quem fala muda o vocabulário, não o ramo. “Três coisas”, “sem isso eu não top”, “eu decido”, “herói” e tom de CO são conteúdo proibido — não escolhem o tamanho. 019 = **perguntar uma vez** antes de vetar. Detalhe: [arco_ativo §7.1](../board/arco_ativo.md).

**Quem está nesta boca:** Valkirya, ramo 3. Quieta, direta, humor seco. Residual alto: uma frase quente que não é ordem. Não chama de herói (F15). Cartão: [vozes.md](../sistema/vozes.md). Reyes, Sasha, Lira, Tio e Rusty ficam no Pack até a volta.

---

## Fatos duros em vigor (não negociar)

| ID | Resumo |
| -- | ------ |
| F01–F02 | Branch `feature/linha-estavel`; arquivos = SoT |
| **F03** | Warden = drone **terrestre** scorpion (**não voa**). A mochila é ele |
| **F12** | Vespas = Hornet, Vesper, Barbed. Pequenas. Não são mochila |
| **F25** | Pill = mula besouro-bola, médio. **Não é mochila.** Nesta viagem: fundo do Mule |
| **F04** | **Stitch** = Stephania (crew); **Doc** = Elisa Moreau (passado) |
| **F06** | Crew NC inclui **Echo** (Media) — off-screen; ≠ Steel Rivera |
| **F14** | **Scout** (pack) ≠ **Jax "Razor" Kane** (crew NC) |
| **F15** | Valk **não** chama Ryan de “herói” / “herói solitário” |
| **F16** | Condor + 3 Corujas = unmanned; spec [condor](../fichas/drone%20-%20condor.md) · [corujas](../fichas/drone%20-%20corujas.md) |
| **F21** | Handle = **Valkirya**. **Valk** e **Morena** = só Ryan (carinho; Morena é a usual). **Lena** = nome. “Morena” na boca dele é ela, não NPC nova |
| F07 | Ryan × Valk consolidados (**acordo 019 = perguntar, não cobrar**) |
| F08 | Mule = de Valk; equipe Valk + Mule |
| **F11** | Casas modulares — pack geral sem revelação oficial completa |
| **F18** | Ruleset atual **v1.4.0** (chrome = número ou função). 017–028 jogadas em 1.3.0, sem retcon. 001–016 pré-camada |
| **F19** | Agents: Vault / Profissional / Honeypot / Arbiter/Watchdog ≠ Warden |
| **F20** | **Sparrow** = Lina Park (NPC); **Steel** = Marcus Rivera (NPC) |

Lista completa: [fatos_duros.md](../sistema/fatos_duros.md).

---

## Pendências quentes

| ID | Uma linha |
| -- | --------- |
| **E015** | Chip **aberto** (token um uso); hop NC **05/08 após 21h**; Lina Park sem ACK; Marcus Rivera mudo; Kaz escondido |
| **Cutter / E008** | Corte 04/08 feito (recon). 7 visíveis; lona morta. Debrief Pack pendente. |
| **Base militar** | Perímetro externo mapeado; **não entra agora**; gatilho = mensagem → manhã seguinte |
| **E019** | Olaria/cogeração — Pack (background) |
| **E012** | Casas interno / revelação pack |

---

## O que acabou de acontecer (029 — 1 parágrafo)

05/08: forja com Tio (flange, válvula, embreagem torno); almoço (porta Sasha/Lira fechada por Valk); rede; saída sem debrief (aviso via Rusty); estrada a sós; traço de pintle/HMG (Ryan se depreciou por não ter automatizado antes; Valk cortou o nome). Freeze: noite, Mule, luzes de NC à vista. Ainda não é o ponto.

Detalhe: [sessao_resumo_029.md](sessao_resumo_029.md)

---

## Confirmação de boot (formato fixo)

```
Boot OK · ~05/08/2026 noite · Mule · luzes de Night City à vista · Valk = residual quente · boca ramo 3 (Mule a sós; Pack = ramo 2) · chip aberto (token) · hop NC 05/08 21h · debrief Reyes pendente · próximo resumo: 030 · Ruleset 1.4.0
```

Hierarquia: **RAW/repo > sandbox > memória de chat**.
