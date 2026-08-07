# Comandos do Jogador — Playbooks para a IA

**Finalidade:** instruções **passo a passo** que a IA deve seguir ao receber cada comando.  
**Branch canônica:** `feature/linha-estavel`  
**Última atualização:** 29 de Julho de 2026

> Tabela resumida também em [instrucoes_projeto.md](instrucoes_projeto.md).  
> Tier-0: [logs/context_pack_atual.md](../logs/context_pack_atual.md) · [fatos_duros.md](fatos_duros.md).

---

## Regras gerais (todo comando)

1. **Reconhecer** o comando na primeira linha da resposta.
2. **Não narrar cena de RP** até concluir o playbook — exceto se o jogador pediu explicitamente “e continue” no mesmo turno.
3. **Ler arquivo local** primeiro; se faltar, divergir ou sandbox vazio → **RAW**:  
   `https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/<caminho>`
4. Hierarquia: **RAW/repo estável > sandbox local > memória de chat / share**.
5. **Não** commit/push sem confirmação explícita do jogador (salvo o turno já ser “commit e push”).
6. **Não** inventar fatos ausentes dos arquivos (F02).
7. Playbooks são **independentes de região** (Pack / Night City / estrada). Só mudam os **paths** lidos conforme o NOW do context pack / board.

---

## A) `[Refresh contexto]`

**Objetivo:** reancorar o modelo no meio do chat sem recarregar a campanha inteira.

### Passos

| # | Ação |
| - | ---- |
| 1 | Declarar: `Refresh contexto — tier-0.` |
| 2 | Abrir **nesta ordem**: `logs/context_pack_atual.md` (incl. bloco **MOTOR** + **AGENDA**) → `sistema/fatos_duros.md` → (só se pack vazio/contraditório) `board/board_campanha.md`. |
| 3 | Se local falhar: mesmos paths via **RAW**. |
| 4 | **Proibido** neste comando: reler ficha completa, todos os relacionamentos, todos os `sessao_resumo_*`, pasta `pulso_do_mundo` inteira. |
| 5 | Responder **no formato fixo abaixo** (obrigatório) — **inclui linha Motor**. |
| 6 | Se o jogador **não** pediu continue/ação no mesmo turno: perguntar se retoma a cena. |
| 7 | Se o mesmo turno trouxer **ação de RP** após o refresh (ex. `[Refresh]` + marcha/recon): (a) bloco refresh completo (b) narração **já em modo resultado-primeiro** (N1b) — **proibido** ecoar o procedimento do jogador. |

### Formato de resposta obrigatório

```markdown
**Boot refresh OK**
- Data in-game: …
- Região / local / período: …
- Prioridade (E0XX ou livre): …
- Fato duro 1 (ex. F03 Warden terrestre): …
- Fato duro 2 (ex. F04 Stitch ≠ Doc): …
- Motor: N1 sem eco · resultado-primeiro se OPERAÇÃO · AGENDA #… (1 linha do gancho ativo)
- Conflito detectado? Não | Sim — fonte vencedora: RAW/board/pack
```

### Quando sugerir (proativo)

- ~40–50 mensagens relevantes no chat
- Mudança de local ou região
- Fim de combate / job
- Jogador confuso sobre “onde estamos” ou “o que está pendente”
- Estilo eco dominante (sugerir também `[Motor de cena]` ou **chat novo** com handoff)

---

## B) `[Resumo da Sessão]` / `[Criar resumo da sessão atual]`

**Objetivo:** documentar o chat atual **sem** fechar a sessão nem gravar no git automaticamente.

**Sinônimos:** os dois títulos acima = **mesmo playbook**.

### Passos

| # | Ação |
| - | ---- |
| 1 | Declarar o comando. |
| 2 | Ler: `logs/sessao_resumo_template.md` + `sistema/registro_arquivos.md` (próximo número **NNN**). |
| 3 | Extrair do **chat desta sessão** apenas eventos que **ocorreram** (não inventar off-screen; não copiar sessão anterior). |
| 4 | Alinhar cabeçalho (data/local) com `context_pack_atual` / `board`. |
| 5 | Preencher o template: Eventos Principais, Mudanças de Estado, Decisões, Pendências, Observações do Narrador. |
| 6 | Listar **candidatos** a “Arquivos Atualizados Nesta Sessão” (ainda **sem** editar). |
| 7 | **Mostrar o markdown completo** do resumo no chat. |
| 8 | Perguntar o que fazer a seguir: |
| | (a) Só manter no chat |
| | (b) Gravar `logs/sessao_resumo_NNN.md` |
| | (c) Também atualizar estado (board etc.) — preferir então o comando **Finalizar** |
| 9 | **Não** editar board, consequências, handoff ou context pack **neste** comando, a menos que o jogador peça no mesmo turno. |

### Diferença vs Finalizar

| | Resumo (B) | Finalizar (C) |
| - | ---------- | ------------- |
| Gera texto de resumo | Sim | Sim |
| Propaga estado (board, pack, handoff) | Não (salvo pedido extra) | Sim (após confirmação) |
| Encerra sessão operacionalmente | Não | Sim |

---

## C) `[Finalizar sessão e gerar resumo]`

**Objetivo:** fechar a sessão de forma canônica: resumo + **matriz completa de ledgers** + context pack + handoff.

### Passos

| # | Ação |
| - | ---- |
| 1 | Declarar: `Finalizar sessão — playbook completo.` |
| 2 | Ler: `sessao_resumo_template.md`, `registro_arquivos.md` (NNN), `board`, `dashboard_contexto`, `event_queue`, `como_atualizar_arquivos.md`, `context_pack_atual`, `fatos_duros`, **e a matriz de ledgers:** `consequencias/consequencias_persistentes.md`, `heat.md`, `reputacao.md`, `economia.md`, `logs/downtime_ryan.md`, `facoes/` relevantes, `relacionamentos/faccao_relacionamentos.md`, `pulso_procedimento.md` (se data avançou). |
| 3 | Calcular **data início → fim** da sessão e quantos **dias in-game** passaram. |
| 4 | Gerar **rascunho** de `logs/sessao_resumo_NNN.md` (conteúdo como em B), com seções: Rep/Heat/Econ · Downtime · Facções/Consequências · Pulsos (dias) — usar **“sem delta”** quando avaliou e nada mudou. |
| 5 | Montar **tabela de mudanças propostas** (Arquivo → o que muda). **Sempre avaliar** (não pular por omissão): |
| | - Missão/local/NPCs → `board`, `dashboard` |
| | - Impacto permanente / arco → `consequencias` |
| | - Facção / pack / corp → `facoes/`, `faccao_relacionamentos`, `reputacao` |
| | - Exposição → `heat` |
| | - Dinheiro / materiais / projetos pack → `economia` (macro) |
| | - Item criado/consumido/scav/transferido **ou** capacidade nova de ator → `economia.md` § Atores / § Estoque / § Ryan mínimo |
| | - Ryan produziu (oficina, scav, construção) → `logs/downtime_ryan.md` |
| | - NPCs → relacionamentos relevantes |
| | - **1+ dia in-game** → [pulso_procedimento.md](pulso_procedimento.md) (ciclos faltantes ou gap B1 documentado); região atual only |
| | - **Sempre:** `logs/context_pack_atual.md` (incl. **AGENDA DA CENA** do NOW; se **local/região mudou**, reescrever agenda inteira) + `logs/handoff_atual.md` |
| | - `registro_arquivos` se novo resumo ou arquivo |
| 6 | **Mostrar ao jogador:** (1) resumo completo; (2) tabela Arquivo → mudança (incluir linhas “sem delta” se quiser transparência). |
| 7 | **Parar.** Pedir confirmação explícita: aplicar arquivos? commit/push? |
| 8 | **Só após confirmação:** escrever arquivos no workspace. |
| 9 | **Ordem de escrita:** `sessao_resumo_NNN` → board + dashboard → event_queue → consequencias → facoes/ + faccao_rels (se tocado) → relacionamentos NPC/crew → heat + reputacao + economia → downtime_ryan (se projeto) → pulso (se 1+ dia) → **context_pack** → **handoff** → registro. |
| 10 | Responder com: lista de paths **avaliados e** alterados + próximo NNN+1 + lembrete de handoff se chat novo. |
| 11 | Commit/push **somente** se o jogador confirmou. |

### Checklist rápido (colar na cabeça)

```text
[ ] Dias in-game (início → fim)
[ ] Board + dashboard
[ ] Event queue
[ ] Consequências
[ ] Facções / facção_rels
[ ] Heat / reputação / economia macro (delta ou “sem”)
[ ] Estoque / atores / Ryan mínimo (delta ou “sem”)
[ ] Downtime (Ryan produziu?)
[ ] Pulso (ciclos ou gap B1)
[ ] Relacionamentos tocados
[ ] HP / SW / Death Save (se combate)
[ ] SP / ablação (se armadura atingida)
[ ] Inventário tático / munição (se relevante)
[ ] Ruleset version no resumo (ex. Ruleset: 1.0.0) — ver regras_red/00
[ ] Decisões provisórias mecânicas (promover house rule?)
[ ] Context pack (NOW + **AGENDA DA CENA** coerente com local) + handoff
[ ] Resumo lista paths avaliados
```

### Caso especial: só RP, estado canônico igual

Ainda gerar resumo mínimo; preencher seções de ledger com **“sem delta”**; atualizar handoff + context pack; board só se data/local in-game avançou (e aí pulso se dia mudou).

### Se passou 1+ dia in-game na sessão

**Obrigatório** (não opcional): seguir [pulso_procedimento.md](pulso_procedimento.md) na **região atual** (não forçar pulso Pack em NC). Se ciclos não foram rodados durante o RP, rodar faltantes no finalize **ou** documentar gap B1.

---

## D) `[Gerar handoff para novo chat]` / `[Preparar novo chat]`

**Objetivo:** regenerar continuidade colável **sem** obrigar novo `sessao_resumo` nem fechar a sessão.

**Sinônimos:** os dois comandos = **mesmo playbook**.

### Passos

| # | Ação |
| - | ---- |
| 1 | Declarar o comando. |
| 2 | Ler: `sistema/novo_chat_procedimento.md` + `logs/handoff_template.md`. |
| 3 | Ler estado: `board`, `event_queue`, `context_pack_atual`, `fatos_duros`, último `sessao_resumo_*` se existir. |
| 4 | **Sobrescrever** `logs/handoff_atual.md` (nunca criar série `handoff_011.md`). |
| 5 | Checklist do handoff: |
| | - Metadados (após sessão X / próxima Y) |
| | - Links RAW (context pack, board, handoff, última sessão, comandos) |
| | - NOW (região, local, prioridade, segredos) |
| | - O que aconteceu (5–12 bullets) |
| | - Pendências E0XX |
| | - Projetos / NPCs quentes **da cena atual** |
| | - **AGENDA DA CENA** no pack (máx. 3 ganchos do local atual; reescrever se local mudou) |
| | - Regras duras (F03, F04, F11, …) + Motor de cena N1–N9 |
| | - **Prompt de abertura colável** (tier-0 primeiro: context pack; 1 linha: não ecoar / delta / agenda) |
| 6 | Se o NOW mudou: atualizar também `logs/context_pack_atual.md` (NOW + **AGENDA reescrita** se local/região mudou). |
| 7 | Mostrar no chat: confirmação dos arquivos + **Prompt de abertura** para copiar. |
| 8 | Commit/push só com confirmação do jogador. |

### Relação com Finalizar

- **Finalizar (C)** já deve gerar/atualizar handoff + pack no passo 8.
- **Handoff (D)** sozinho serve quando o jogador quer chat novo **sem** fechar com resumo numerado, ou quer regenerar o prompt.

---

## E) Comandos auxiliares

### E1) `[Carregar cena: <tag>]`

Exemplos de tag: `valk`, `pack`, `mule`, `nc`, `kaz`, `stitch`, `job001`.

| # | Ação |
| - | ---- |
| 1 | Declarar tag. |
| 2 | Resolver paths via `registro_arquivos.md` e/ou `mapa_relacional_geral.md` (máx. **1–3 arquivos**). |
| 3 | Ler só esses arquivos (local ou RAW). |
| 4 | Resumir em bullets o que carregou (sem dump completo). |
| 5 | Continuar narração **somente** se o jogador pediu. |

**Não** usar este comando para recarregar a campanha inteira (usar Refresh).

### E2) `[Verificar fato: <afirmação>]`

| # | Ação |
| - | ---- |
| 1 | Identificar o arquivo SoT (fatos_duros, board, ficha, log…). |
| 2 | Abrir local ou RAW. |
| 3 | Citar trecho relevante (curto). |
| 4 | Julgar: **Verdadeiro** / **Falso** / **Parcial** / **Não registrado**. |
| 5 | Se não registrado: dizer que **não existe** no SoT — não inventar. |

### E3) `[Vestindo]` / `[Roupa <modo>]` / `[Roupa <quem> <modo>]`

**Objetivo:** roupa consistente sem abrir o catálogo de ~194 looks.

| Comando | Efeito |
| ------- | ------ |
| `[Vestindo]` | Listar tabela **vestindo agora** (só quem está em cena) |
| `[Roupa street]` / `[Roupa job]` / `[Roupa casa]` / `[Roupa íntimo]` / `[Roupa medical]` / `[Roupa gala]` / `[Roupa formal]` | Pick do **card** do modo para quem está em cena |
| `[Roupa Valk job]` | Pick só para essa personagem |
| `[Roupa arquivo:street_allblack_set.png]` | Fixar look explícito |

| # | Ação |
| - | ---- |
| 1 | Ler [crew_vestindo_agora.md](../fichas/notas_narrador/crew_vestindo_agora.md) + card em [roupa_por_ocasiao.md](../fichas/notas_narrador/roupa_por_ocasiao.md). |
| 2 | Aplicar anti-ontem / últimos 3; pesos **dona** (alto) / pool (médio) / **empréstimo** dona≠ela (baixo); vibe Combina com. |
| 3 | Evitar duas com o **mesmo** arquivo na cena (re-sorteio). |
| 4 | Atualizar estado (origem `dona` ou `empréstimo (Nome)`). |
| 5 | Descrever **1–3 linhas** de roupa e seguir a cena — **não** dump do catálogo. |

**Dona ≠ exclusividade:** outra da casa pode emprestar (polycule/crew).  
**Biblioteca completa** só se o jogador pedir detalhe ou o pick falhar: [crew_guarda_roupas.md](../fichas/crew_guarda_roupas.md).

### E4) `[Vazamento N]` / `[Echo fantasma]` / `[Echo headline]`

**Objetivo:** fixar o nível de exposição da Echo e propagar Heat/Rep.

| Comando | Efeito |
| ------- | ------ |
| `[Echo fantasma]` / `[Vazamento 1]` | Nível 1: Void List + funções; Heat ind. baixo |
| `[Vazamento 2]` | Headline sem rosto |
| `[Echo headline]` / `[Vazamento 3]` | Rosto/handle — **tensão**; ind. alto se for |
| `[Vazamento 0]` | Nada público / engaveta |
| `[Vazamento 4]` | Dossiê / Null / Pack — **crise** |

SoT: [echo_exposicao.md](echo_exposicao.md). Atualizar `heat.md` + `reputacao.md` com 1 linha de delta (ou “sem delta”).

---

## H) `[Agência NPC]` / observação passiva / delegação

**Objetivo:** NPCs falam entre si, decidem micro-ações ou **executam tarefa delegada** sem controlar Ryan e sem repetir o mesmo menu de opções.

**Sinônimos:** `[Agência NPC]` · `*observo em silêncio*` · `espero` · `deixem eles decidirem` · `Valk, planeja…` · `Elias resolve com o Tio Gringo`

**Guia:** [npc_agencia_cena.md](npc_agencia_cena.md)

### Passos

| # | Ação |
| - | ---- |
| 1 | Declarar o gatilho (ambiental / passivo / explícito / **delegação**). |
| 2 | Ler NOW em `context_pack_atual.md` → NPCs presentes. |
| 3 | Abrir ficha + pulso de cada NPC na cena (ex.: Valk → `fichas/nomad - lena_valk_kane.md` + `pulso_do_mundo/crew/valk.md`). |
| 4 | Se **delegação** (Ryan pediu plano/logística): NPC entrega **plano concreto** (horário, rota, equipamento, quem fica onde) — **não** pedir de volta "como você quer planejar". |
| 5 | Se **passivo/ambiental**: 1–2 falas NPC↔NPC ou 1 micro-decisão; narrar só o que Ryan percebe. |
| 6 | **Anti-loop:** se a mesma pergunta/opções já apareceu 2× nesta sessão → avançar com decisão do NPC. |
| 7 | Parar com gancho para Ryan (veto, ajuste, reação) — sem "o que você faz?" genérico. |

### Exemplo rápido (delegação — caça às aves)

- **Jogador:** "Valk, planeja a caça às aves amanhã."
- **Errado:** repetir "qual rota prefere A/B/C?" quatro vezes.
- **Certo:** Valk devolve plano (saída 05h20, rota pelo leste, Scout/Rusty no perímetro, volta 10h30); Ryan só ajusta se quiser.

---

## I) `[Avançar cena]` / `[Pressão]`

**Objetivo:** forçar **1 beat** de plot a partir da AGENDA / NOW quando a cena entrou em mood/eco sem avanço.  
**Escopo:** qualquer local (não amarrado a Pack).  
**Sinônimos:** `[Avançar cena]` · `[Pressão]` · `[Injeta pressão]`

**Guia:** [diretrizes_narrador.md](diretrizes_narrador.md) §7.1 (N1–N8)

### Passos

| # | Ação |
| - | ---- |
| 1 | Declarar: `Avançar cena — 1 gancho da AGENDA/NOW.` |
| 2 | Ler: `logs/context_pack_atual.md` → **AGENDA DA CENA** + NOW + pendências quentes. Se agenda vazia: `event_queue.md` filtrado pelo **local/região atual** (F10). |
| 3 | Escolher **1** gancho de maior prioridade **plausível no local atual**. |
| 4 | Narrar o interrupt/avanço em diegese: **sem** eco do último turno do jogador (N1); com **delta** (N2+). |
| 5 | Deixar o jogador reagir. **Não** editar arquivos neste comando (salvo o jogador pedir no mesmo turno). |

### O que não fazer

- Inventar NPC/facção/plot fora do SoT.  
- Usar gancho de **outro local** sem canal in-fiction.  
- Transformar o comando em resumo meta longo — é um **beat narrativo**.

---

## J) `[Motor de cena]` / `[Anti-eco]`

**Objetivo:** reancorar o estilo narrativo **sem** fechar sessão — corrige eco/espelho mid-chat.  
**Sinônimos:** `[Motor de cena]` · `[Anti-eco]` · `[Motor de cena — reler]`

**Guia:** [motor_cena_1pager.md](motor_cena_1pager.md) · [diretrizes_narrador.md](diretrizes_narrador.md) §7.1

### Passos

| # | Ação |
| - | ---- |
| 1 | Declarar: `Motor de cena — reancorado.` |
| 2 | Ler: `sistema/motor_cena_1pager.md` + bloco **MOTOR** + **AGENDA** em `logs/context_pack_atual.md` (RAW se preciso). |
| 3 | Responder em **formato curto** (abaixo). **Não** narrar cena ainda, salvo o jogador ter pedido “e continue” / enviado ação no mesmo turno. |
| 4 | Se houver ação no mesmo turno: narrar **já** com N1b (resultado primeiro), N8 (SOP comprimido) e N9 se for viagem limpa. |
| 5 | Mesmo se a ação for um **script longo** (ex. gerado em chat meta): **não ecoar** — só outcomes. |
| 6 | Se o thread estiver muito contaminado por eco (>~40 msgs RP): **sugerir** chat novo com `logs/handoff_atual.md`. |

### Formato de resposta obrigatório

```markdown
**Motor reancorado**
- N1 sem eco · N1b resultado-primeiro · N2+ delta ≥60% · N8 SOP · N9 fecho de viagem limpa
- AGENDA ativa: #… — …
- Próximo turno de RP: outcomes primeiro; sem espelhar o PC
- Ação OPERAÇÃO preferível: intenção curta + limites (não manual de 8 passos)
- (Opcional) Chat longo com eco pesado → preferir novo chat + handoff
```

---

## Tabela rápida

| Comando | Edita arquivos? | Precisa confirmação para gravar? |
| ------- | --------------- | -------------------------------- |
| `[Refresh contexto]` | Não | — |
| `[Vestindo]` / `[Roupa …]` | Sim (estado vestindo) se fixar look | Não para listar; sim se o fluxo da mesa gravar pack |
| `[Resumo da Sessão]` / `[Criar resumo…]` | Só se jogador pedir (b) | Sim para gravar |
| `[Finalizar sessão e gerar resumo]` | Sim (após sim) | **Sim** antes de gravar |
| `[Gerar handoff…]` / `[Preparar novo chat]` | Sim (handoff ± pack) | Sim para commit/push; gravar local pode ser imediato se o jogador pediu o handoff |
| `[Carregar cena]` | Não | — |
| `[Verificar fato]` | Não | — |
| `[Agência NPC]` / delegação / `*observo*` | Não | — |
| `[Avançar cena]` / `[Pressão]` | Não | — |
| `[Motor de cena]` / `[Anti-eco]` | Não | — |
| `[Estoque]` / `[Recursos]` / `[O que tem: …]` | Não | — |

---

## K) `[Estoque]` / `[Recursos]` / `[O que tem: <filtro>]`

**Objetivo:** consulta **sob demanda** ao ledger de micro-recursos — **sem** inventário RPG no tier-0.  
**Sinônimos:** `[Estoque]` · `[Recursos]` · `[O que tem: X]` · `[Estoque: Ryan]` · `[Estoque: destilaria]`

**SoT:** [economia.md](../economia.md) — § Atores · § Estoque · § Ryan mínimo

### Passos

| # | Ação |
| - | ---- |
| 1 | Declarar: `Estoque — consulta ledger.` |
| 2 | Abrir `economia.md` (local ou RAW). |
| 3 | **Filtrar:** (a) argumento do jogador (ator, item, local) **ou** (b) default = **região/local do NOW** + **Ryan mínimo** + atores presentes na cena. |
| 4 | Responder **só linhas relevantes** (alvo ≤ ~15 linhas): IDs, item, onde, qtd, nota curta. Incluir **capacidade** do ator se o filtro for facility/NPC. |
| 5 | Se nada bater: **“Não registrado no SoT”** — **não inventar** estoque “óbvio”. |
| 6 | **Não** narrar RP salvo o jogador pediu continue no mesmo turno. |
| 7 | **Não** dump da tabela inteira (mata legibilidade; não é o objetivo). |

### Exemplos

```text
[Estoque]                 → NOW + Ryan mínimo
[Estoque: Ryan]
[Estoque: destilaria]     → A-ELI + P* ligados
[O que tem: sabonete]
[Recursos: Pack]
```

---

## Referências

- [Context pack](../logs/context_pack_atual.md) · [Fatos duros](fatos_duros.md) · [Instruções](instrucoes_projeto.md) · [Economia / estoque](../economia.md)
- [Diretrizes IA](diretrizes_ia.md) · [Diretrizes Narrador](diretrizes_narrador.md) §7.1 · [Motor 1pager](motor_cena_1pager.md) · [Agência NPC](npc_agencia_cena.md)
- [Como atualizar](como_atualizar_arquivos.md) · [Novo chat](novo_chat_procedimento.md)
- [Template resumo](../logs/sessao_resumo_template.md) · [Template handoff](../logs/handoff_template.md)
