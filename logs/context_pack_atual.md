# Context Pack atual (tier-0)

**Finalidade:** único arquivo **mínimo** que a IA deve ler/re-ler para não esquecer o estado.  
**Gerado após:** sessão **033** · **Próxima:** **034** (`sessao_resumo_034.md`)  
**Branch:** `feature/linha-estavel`  
**Atualizado:** ~06 de Agosto de 2026 (tarde) — tenda · Pack

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
   - **A sós** (tenda, banho, cama, banco do Mule em estrada): uma fala, um fôlego, diegética e fluida. Pode ter mais corpo. Quieta pode. Selo de duas frases não serve. Chip, Reyes e hop não entram nesta boca. Ela responde a ele ou traz uma coisa dela. Uma. Sem menu.
2. **Não ecoar** o PC: ≤2 linhas **só** para confirmar a ação dele. Esse teto não mede a fala do NPC. SOP multi-passo → outcomes (N8). Resultado-primeiro **só** no ramo de rádio/ops/combate.
3. **Delta** = **maior parte** (~≥60%). Nos ramos Pack social e a sós: SHOW + fala do ramo = delta. A fala desses ramos é diegética e fluida. Corpo: 3–6 linhas é **piso**, e pode ter mais. O extra é lugar, gesto e calor, não discurso. A mesma mão entra numa frase só e não volta no turno seguinte. O lugar muda. Não precisa de burst nem relógio.
4. **VIAGEM limpa (N9):** sem anomalia no caminho → **fechar chegada** se o destino está no nó, na nota de saída ou num card de [set_lugares.md](../sistema/set_lugares.md). Fora desses três: dizer isso uma vez. Não criar lugar, pessoa nem evento.
5. **Anti-máquina:** sem *nome de regra* na prosa. Humor, medo, cansaço, recusa = obrigatório. No ramo 2 e 3 a vida é no primeiro turno: corpo ou uma coisa dela já escrita. Agenda de plot fica calada nessa boca. “Três coisas” = ultimato de condições, não teto de frase. Ryan pode cortar; ninguém copia o corte. Trava: `[Voz: ramo antes da frase. Ryan pode cortar. NPC não copia o corte.]`
6. Fonte de pressão: momento importante → nó do **META-ROTEIRO** e a nota de saída (escondida não congela quem a nota diz que a cena veio resolver; sem nó e sem nota, não inventar o evento; linha de AGENDA não é reação). Senão **AGENDA DA CENA** → [arco_ativo](../board/arco_ativo.md) (L1 + off-screen + §7 SHOW) → pendências → `event_queue` (F10).
7. Local novo / ação no terreno → bloco **AMBIENTE** ([cena_ambientacao](../sistema/cena_ambientacao_ganchos.md)). Checklist interno; o fato entra numa situação (N13). Não gavetas na tela (`Cobertura:`, `EM:`). Não omitir o dado escrito. Indefinido não se completa.
8. Escorregou? `[Motor de cena]` / `[Anti-eco]` · Estagnou? `[Avançar cena]` / `[Pressão]` · Lugar opaco? `[Ambientar]`.
9. **Chat novo:** este pack + handoff; **não** continuar threads longos degradados.
10. **Rodapé OOC:** depois da cena, linha em branco + `ctrl N/90`. +2 por resposta sua. Boot = `ctrl 2/90`. Perdeu = `ctrl ?/90`. Não narrar; não é chrome/Agent; ninguém na cena vê.

Detalhe: [motor_cena_1pager.md](../sistema/motor_cena_1pager.md) · N13: [diretrizes_narrador.md](../sistema/diretrizes_narrador.md) §5.2

---

## NOW

| Campo | Valor |
| ----- | ----- |
| Data in-game | **~06/08/2026** |
| Período | Tarde |
| Região | **Pack Badlands** |
| Local específico | Tenda dos dois. Residual íntimo alto. Dia passado quieto com Valk. Debrief Reyes feito. Destilaria com alívio pronta (primeiro ciclo sob Elias). |
| Facção / base local | Pack |
| Cena / gancho | Descanso residual. Rotina Pack. |
| Prioridade | (1) Descanso (2) Destilaria primeiro aquecimento se puxar (3) Canal reserva quieto |
| Segredos ativos | Casas modulares — pack geral sem revelação completa; convite NC a Sasha/Lira fechado por Valkirya |

### SET NOW

Tenda. Porta fechada: Ryan e Valkirya. Residual alto. Warden perto. Pill no fundo do Mule (garagem). Vespas no Mule. Debrief feito. Destilaria parada até primeiro ciclo.

Pack deixado na saída: [context_pack_pack.md](context_pack_pack.md). **Não** abrir no boot nem no Refresh.

## NORTE (orientação, não quest log)

> Horizontes. **Não** é trilho. Se o pack divergir do `arco_ativo`, **vence este pack**.

| Horizonte | Norte |
| --------- | ----- |
| **Curto** (hoje / sessão) | Descanso residual na tenda. Destilaria primeiro ciclo se puxar. |
| **Médio** (1–3 sessões) | Canal reserva com Kaz e Sparrow. Crew e safehouse esperam em NC, fora desta cena. |
| **Longo** (campanha) | Pack casas/Node/olaria. Doc E011. Crew NC. |
| **Fora agora** | Base militar. Raid Cutter. Reabrir jantar 023 / SOP Condor / caixa 101 / canyon. |

### Cena de abertura sugerida (034)

**Não continuar o chat da 033.**  
06/08 tarde, tenda. Residual íntimo alto. Dia passou quieto. Debrief feito. Destilaria pronta. Não reabrir jantar 023 nem SOP Condor nem a caixa da 101 nem o canyon nem a base.

---

## AGENDA DA CENA (anti-estagnação)

| # | Gancho (1 linha) | Quem age se idle | Se Ryan idle / mood ≥3 turnos → o narrador faz |
| - | ---------------- | ---------------- | ---------------------------------------------- |
| 1 | Descanso residual | Valk | Na tenda: braço, fome, ou cuidar dele. Sem hop na boca. |
| 2 | Destilaria primeiro ciclo | Elias | Se puxar: observa o peso/apito. Não força. |
| 3 | Canal reserva | ninguém nesta tenda | Existe. Mensagem fica no servidor. Não chama aqui. |

| Campo | Valor |
| ----- | ----- |
| **Modo atual** | Descanso Pack |
| **Turnos sem delta (estimado)** | 0 |
| **Região / local (NOW)** | Pack · tenda |
| **Arco L1** | Debrief feito · destilaria prática · [arco_ativo.md](../board/arco_ativo.md) |

## META-ROTEIRO (regra estável)

Preparo do narrador. O jogador não é obrigado a ficar no nó. Não entra na boca. Não vira menu nem gaveta. A regra não muda a cada momento. Muda o nó.

Momento importante tem duas partes.

- **Estado:** onde, com quem, o que já aconteceu.
- **Motor:** por que a cena existe, o que pode mudar, o que uma ação faz.

Cada coisa no nó é uma classe só: **fato**, **o que a pessoa sabe**, **hipótese**, **oculto** ou **indefinido**. Campo vazio é indefinido. Indefinido não se narra. Hipótese não vira fato no meio do turno. Oculto não sai na fala de quem não sabe.

Ação relevante muda o estado, ou mantém a situação por uma razão que já está no nó. O mesmo estado, sem condição nova, não é resposta. Ação que não está no nó se julga no estado escrito. Fora do nó valem o objetivo grande e o custo já escrito.

Nota de saída (`sistema/roteiro_pendencias.md`; no job, a seção do próprio job): a cena, o job ou a decisão dependem de uma pessoa quando a nota diz que resolver esse papel é o motivo. Escondida, off-screen ou “não forçar” não a congela. Avaliar a nota. Se a cena existe para resolver esse papel, a pessoa pode aparecer, ou deixar de estar escondida, por uma saída já escrita. Se o jogador está noutra coisa, ou o motivo de estar escondida não é o assunto, ela não entra. Se ele pede o papel que a cena veio resolver, ou a janela que ele marcou fecha, jogar uma saída da nota. O terceiro silêncio da mesma pendência não é resposta. Se nenhuma pessoa já escrita serve e a nota nomeia alguém de fora do roster, entra esse NPC do job, recorrente ou só deste job. Sem nota, não inventar pessoa, lugar, facção ou trama para destravar. A nota é o que torna novo em escrito. Hipótese não vira fato no meio do turno.

Destino no nó, na nota ou num card de `set_lugares.md` está escrito: a viagem fecha nele. Fora dos três, dizer uma vez. Não criar rua. Lugar que não está no nó, na nota nem num card não aparece.

Nó grande resolvido: escrever o próximo nó neste bloco antes da cena seguinte. Frase no chat não é nó. Rascunho curto basta, com hipótese marcada e campo vazio indefinido. Chegar com o nó em branco é o travamento. O fechamento grava a nota seguinte. Nota seguinte em branco bloqueia o sim.

Lembrança e cena: o que está escrito se repete. Campo vazio continua vazio. Não nasce pessoa, facção, pista nem decisão. Cor cabe num distrito já listado: luz, ruído, um quarto, uma fila. Cor não responde pergunta, não entra no card e não volta.

Preparo: ao criar job, card de lugar-nó, ou a nota que resolve uma situação. O produto é a nota, antes da cena. Teto e campos em `sistema/roteiro_pendencias.md`. Frase no chat não é nota.

Fecho: pessoa de uma cena vira uma linha em quem ela serviu, com “não volta”. Lugar de cor não promove. Lugar que uma decisão futura usa ganha card. O que a cena respondeu deixa de ser indefinido.

Porta: `fechada` ou `aberta`, na nota desta cena. Sem nota, vale o card. Fechada: só quem a nota pôs. Aberta: corpos já escritos, função sem nome. Aberta sem corpos, a abertura para. Corpo não traz plot e não nasce NPC novo no turno.

Vida já na ficha, e viagem cujo destino já está escrito, não ganham nó cheio. Linha de AGENDA não é reação do nó.

### Nó atual

Nota longa: [roteiro_pendencias.md](../sistema/roteiro_pendencias.md) § rotina. Debrief fechado.

**Estado.** Fato: 06/08 tarde, tenda. Residual alto. Debrief Reyes feito (8 hostis reportados, sem raid, base fora). Destilaria com alívio de peso + disco, pronta, barril parado. Canal reserva existe, não usado. Crew/safehouse off-screen NC.

**Porta.** Fechada. `tenda`. Ryan e Valkirya.

**Saída.** Nenhuma obrigatória. Destilaria primeiro ciclo se Elias puxar ou Ryan for. Rotina Pack.

**Trava 023 (não reabrir):** base = mensagem → manhã seguinte; 019 em vigor. **Não** reabrir o jantar como briga. **Não** reabrir SOP Condor como tutorial. **Não** reabrir o canyon do corte.

### SOP Condor (SoT 020–022 — não carimbar na prosa)

- Condor = transporte cego. Coleta = Agent na mochila. Ar = silêncio + abort mínimo. **Unmanned.** Spec: [drone - condor.md](../fichas/drone%20-%20condor.md).
- Sasha/Lira = voo/visual no **gancho/visor**. Não abrem módulo. Não anunciam pacote.
- Valk no gancho ok; **não** autentica o Agent.
- Ryan recupera o Agent. Só ele diz se veio pacote.

### Boca (boot — ramo antes da frase)

NOW = tenda a sós → **ramo 3**. Pátio / Reyes / refeitório → **ramo 2**. Residual íntimo **alto**. Chat **023** não se herda.

1. **Rádio / ops / combate** — curta, seca, pessoa. Resultado primeiro. *“Contato no leste, abort no rádio. Eu na porta. Tu marca o tempo.”*
2. **Pack social** — conversa diegética e fluida; uma fala de gente; corpo no meio; pode ter mais corpo; cada um pela ficha. Reyes: *“Camp eu não tenho. Corredor, sim. O céu amanhã me diz onde corto — um, não um raid. Tu some de novo no mesmo dia. A 101 não é minha estrada.”*
3. **A sós** — uma fala, um fôlego, diegética e fluida. Pode ter mais corpo. Quieta pode. Selo de duas frases não serve. Chip, Reyes e hop fora desta boca. Ela responde a ele ou traz uma coisa dela. Uma. Humor seco, sem despacho, sem menu. Coisa dela nesta cena: braço, fome, o Mule, ou cuidar dele. Hop, horário, lugar, janela, debrief e “ainda não é o ponto” ficam no cartão. Ele veta ou ajusta. Modelo de fôlego (copia o tamanho e o corpo no meio; não copia o assunto nem esta cena): *Ela morde o sorriso e o joelho encosta no dele. “Para de ser bonzinho que eu acostumo.”* **Teste:** a frase responde ou traz essa coisa. A mesma mão entra numa frase só e não volta no turno seguinte. As 3–6 linhas são o lugar mudando (calor, poeira, motor), e o corpo pode passar disso.

Quem fala muda o vocabulário, não o ramo. “Três coisas”, “sem isso eu não topo”, “eu decido”, “herói” e tom de CO são conteúdo proibido — não escolhem o tamanho. 019 = **perguntar uma vez** antes de vetar. Detalhe: [arco_ativo §7.1](../board/arco_ativo.md).

**Quem está nesta boca:** Valkirya, ramo 3. Quieta, direta. Residual alto. Não chama de herói (F15). Cartão: [vozes.md](../sistema/vozes.md). Reyes, Sasha, Lira, Tio e Rusty ficam no Pack.

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
| **E015** | Resolvido. Kaz chamou. Token gasto. Casca do chip no Warden, sem token |
| **Debrief** | **Feito**. Vigilância se precisar. Sem raid. Base fora. |
| **Canal reserva** | Existe. Ryan, Kaz, Sparrow. Mensagem fica no servidor. Steel fora |
| **Steel** | Sem contato. Sem custo escrito |
| **Crew / safehouse** | Off-screen em NC, à espera. Ryan não viu. Não narrar no Pack |
| **Cutter / E008** | Corte 04/08 feito (recon). Debrief **feito**. Célula onde deixou. |
| **Base militar** | Perímetro externo mapeado; **não entra agora**; gatilho = mensagem → manhã seguinte |
| **E019** | Olaria/cogeração — Pack (background) |
| **E012** | Casas interno / revelação pack |
| **Destilaria** | Alívio + disco prontos. Primeiro ciclo sob Elias. |

---

## O que acabou de acontecer (033 — 1 parágrafo)

05/08 noite: volta quieta. Carregou Valk pra tenda. 06/08: forja (torno resolvido com alunos), destilaria (alívio de pressão), debrief Reyes fechado (sem raid, sem base). Resto do dia na tenda. Residual alto.

Detalhe: [sessao_resumo_033.md](sessao_resumo_033.md)

---

## Confirmação de boot (formato fixo)

```
Boot OK · ~06/08/2026 tarde · tenda Pack · Valk = residual · boca ramo 3 (a sós; Pack = ramo 2) · debrief feito · destilaria pronta · canal reserva · próximo resumo: 034 · Ruleset 1.4.0
```

Hierarquia: **RAW/repo > sandbox > memória de chat**.
