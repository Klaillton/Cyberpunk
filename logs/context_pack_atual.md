# Context Pack atual (tier-0)

**Finalidade:** único arquivo **mínimo** que a IA deve ler/re-ler para não esquecer o estado.  
**Gerado após:** sessão **028** · **Próxima:** **029** (`sessao_resumo_029.md`)  
**Branch:** `feature/linha-estavel`  
**Atualizado:** ~04 de Agosto de 2026 (fim de tarde) — Pack · tenda Ryan/Valk · chip aberto

> **Não é o board.** Detalhe em `board/board_campanha.md`.  
> **Arco + off-screen (L1):** [board/arco_ativo.md](../board/arco_ativo.md) — sob demanda / se estagnar.  
> Fatos estáveis: [sistema/fatos_duros.md](../sistema/fatos_duros.md).  
> Comandos: [sistema/comandos_jogador.md](../sistema/comandos_jogador.md).  
> Ambientação: [cena_ambientacao_ganchos.md](../sistema/cena_ambientacao_ganchos.md).

---

## MOTOR (todo turno de RP)

1. **Boca — ramo antes da frase.** O ramo de cima não vaza para o de baixo. Quem fala muda o vocabulário, não o ramo. Um exemplo dentro de cada ramo, no bloco Boca e em [arco §7.1](../board/arco_ativo.md).
   - **Rádio / operação / combate** (job, ou o Pack ouvindo o trabalho): curta, seca, pessoa. Resultado primeiro.
   - **Pack social** (refeitório, oficina, pátio, corredor, Reyes, Mule parado): conversa. Uma fala de gente, corpo no meio. Cada um pela ficha.
   - **A sós** (tenda, banho, cama): uma fala, um fôlego. Quieta pode. Selo de duas frases não serve. Chip, Reyes e hop não entram nesta boca.
2. **Não ecoar** o PC: ≤2 linhas **só** para confirmar a ação dele. Esse teto não mede a fala do NPC. SOP multi-passo → outcomes (N8). Resultado-primeiro **só** no ramo de rádio/ops/combate.
3. **Delta** = **maior parte** (~≥60%). Nos ramos Pack social e a sós: SHOW + fala do ramo = delta. Corpo nesses ramos: 3–6 linhas é **piso**. Não precisa de burst nem relógio.
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
| Data in-game | **~04/08/2026** |
| Período | Fim de tarde |
| Região | **Badlands / Pack** |
| Local específico | Tenda Ryan/Valk. Chip E015 **lacre aberto** (token) |
| Facção / base local | Pack Nômade Badlands |
| Cena / gancho | Chip aberto; debrief Reyes pendente; hop NC **05/08 após 21h** |
| Prioridade | (1) Debrief Reyes (2) Hop NC 05/08 noite (3) Não forçar Sparrow/Steel |
| Segredos ativos | Casas modulares — pack geral sem revelação completa; convite NC a Sasha/Lira ainda delicado |

### SET NOW

`sistema/set_lugares.md` § **tenda**. Não abrir o arquivo inteiro.

Tenda Ryan/Valk no Pack. Banho = espaço próprio da tenda (melhoria do Ryan), não box comunitário. Mesa baixa. Chip já lido.

## NORTE (orientação, não quest log)

> Horizontes. **Não** é trilho. Se o pack divergir do `arco_ativo`, **vence este pack**.

| Horizonte | Norte |
| --------- | ----- |
| **Curto** (hoje / sessão) | Debrief Reyes do corte 027. Preparar hop NC. |
| **Médio** (1–3 sessões) | Hop NC **05/08 após 21h** (E015, token no chip). Sparrow/Steel/Kaz **não** forçar. Voltar ao Pack depois. |
| **Longo** (campanha) | Pack casas/Node/olaria. Doc E011. Crew NC. |
| **Fora agora** | Base militar. Raid Cutter. Reabrir jantar 023 / SOP Condor / caixa 101 / canyon. |

### Cena de abertura sugerida (029)

**Não continuar o chat da 028.**  
04/08 fim de tarde, Pack, tenda. Chip **aberto** (token). Debrief Reyes pendente. Valk = residual quente. Não reabrir jantar 023 nem SOP Condor nem a caixa da 101 nem o canyon.

---

## AGENDA DA CENA (anti-estagnação)

| # | Gancho (1 linha) | Quem age se idle | Se Ryan idle / mood ≥3 turnos → o narrador faz |
| - | ---------------- | ---------------- | ---------------------------------------------- |
| 1 | Debrief Reyes (corte 027) | Reyes / Valk | Reyes puxa o debrief no pátio / oficina |
| 2 | Token do chip / hop NC 05/08 após 21h | Mundo / intermediário | Relógio do hop; sem voz; sem ping antigo |
| 3 | Folga Pack até a janela | Valk / Pack | SHOW tenda ou refeitório; sem reabrir canyon |

| Campo | Valor |
| ----- | ----- |
| **Modo atual** | Pack tarde → DOWNTIME / debrief |
| **Turnos sem delta (estimado)** | 0 |
| **Região / local (NOW)** | Badlands · Pack · tenda Ryan/Valk |
| **Arco L1** | E015 (chip aberto · hop NC 05/08 21h) · [arco_ativo.md](../board/arco_ativo.md) |

**Trava 023 (não reabrir):** base = mensagem → manhã seguinte; 019 em vigor. **Não** reabrir o jantar como briga. **Não** reabrir SOP Condor como tutorial. **Não** reabrir o canyon do corte.

### SOP Condor (SoT 020–022 — não carimbar na prosa)

- Condor = transporte cego. Coleta = Agent na mochila. Ar = silêncio + abort mínimo. **Unmanned.** Spec: [drone - condor.md](../fichas/drone%20-%20condor.md).
- Sasha/Lira = voo/visual no **gancho/visor**. Não abrem módulo. Não anunciam pacote.
- Valk no gancho ok; **não** autentica o Agent.
- Ryan recupera o Agent. Só ele diz se veio pacote.

### Boca (boot — ramo antes da frase)

NOW = tenda a sós → **ramo 3**. Pátio / Reyes / refeitório → **ramo 2**. Residual íntimo **alto** na tenda. No job, ramo 1. Chat **023** não se herda.

1. **Rádio / ops / combate** — curta, seca, pessoa. Resultado primeiro. *“Mule no leste, abort no rádio. Eu no volante. Tu marca a janela.”*
2. **Pack social** — conversa; uma fala de gente; corpo no meio; cada um pela ficha. Reyes: *“Camp eu não tenho. Corredor, sim. O céu amanhã me diz onde corto — um, não um raid. Tu some de novo no mesmo dia. A 101 não é minha estrada.”*
3. **A sós** — uma fala, um fôlego. Quieta pode. Selo de duas frases não serve. Chip, Reyes e hop fora desta boca. Modelo de fôlego (copia o tamanho e o corpo no meio da frase; não repete esta cena): *“Você fala fico como se eu fosse te expulsar. Não vou. Fiquei este tempo todo com você pra você não levantar no automático, e agora que levantou ainda está aqui. Tá bom. Fica. Eu gosto quando você para de tratar o corpo como ferramenta que precisa ir embora. O resto do mundo espera do lado de fora. Aqui ainda é só isso.”*

Quem fala muda o vocabulário, não o ramo. “Três coisas”, “sem isso eu não top”, “eu decido”, “herói” e tom de CO são conteúdo proibido — não escolhem o tamanho. 019 = **perguntar uma vez** antes de vetar. Detalhe: [arco_ativo §7.1](../board/arco_ativo.md).

---

## Fatos duros em vigor (não negociar)

| ID | Resumo |
| -- | ------ |
| F01–F02 | Branch `feature/linha-estavel`; arquivos = SoT |
| **F03** | Warden = drone **terrestre** scorpion (**não voa**) |
| **F04** | **Stitch** = Stephania (crew); **Doc** = Elisa Moreau (passado) |
| **F06** | Crew NC inclui **Echo** (Media) — off-screen; ≠ Steel Rivera |
| **F14** | **Scout** (pack) ≠ **Jax "Razor" Kane** (crew NC) |
| **F15** | Valk **não** chama Ryan de “herói” / “herói solitário” |
| **F16** | Condor + 3 Corujas = unmanned; spec [condor](../fichas/drone%20-%20condor.md) · [corujas](../fichas/drone%20-%20corujas.md) |
| **F21** | Handle = **Valkirya**. **Valk** e **Morena** = só Ryan (carinho; Morena é a usual). **Lena** = nome. “Morena” na boca dele é ela, não NPC nova |
| F07 | Ryan × Valk consolidados (**acordo 019 = perguntar, não cobrar**) |
| F08 | Mule = de Valk; equipe Valk + Mule |
| **F11** | Casas modulares — pack geral sem revelação oficial completa |
| **F18** | Ruleset **v1.3.0** · 017+ · sem retcon 001–016 |
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

## O que acabou de acontecer (028 — 1 parágrafo)

04/08: volta do corte; sono; tenda (banho próprio + intimidade); refeitório; chip E015 aberto (token hop NC 05/08 21h). Reyes não encontrado. Freeze: fim de tarde, tenda.

Detalhe: [sessao_resumo_028.md](sessao_resumo_028.md)

---

## Confirmação de boot (formato fixo)

```
Boot OK · ~04/08/2026 fim de tarde · Pack · tenda Ryan/Valk · Valk = residual quente · boca ramo 3 (tenda; Pack = ramo 2) · chip aberto (token) · hop NC 05/08 21h · debrief Reyes pendente · próximo resumo: 029 · Ruleset 1.3.0
```

Hierarquia: **RAW/repo > sandbox > memória de chat**.
