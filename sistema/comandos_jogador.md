# Comandos do Jogador — Playbooks para a IA

**Finalidade:** instruções **passo a passo** que a IA deve seguir ao receber cada comando.  
**Branch canônica:** `feature/linha-estavel`  
**Última atualização:** 13 de Julho de 2026

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
| 2 | Abrir **nesta ordem**: `logs/context_pack_atual.md` → `sistema/fatos_duros.md` → (só se pack vazio/contraditório) `board/board_campanha.md`. |
| 3 | Se local falhar: mesmos paths via **RAW**. |
| 4 | **Proibido** neste comando: reler ficha completa, todos os relacionamentos, todos os `sessao_resumo_*`, pasta `pulso_do_mundo` inteira. |
| 5 | Responder **no formato fixo abaixo** (obrigatório). |
| 6 | Se o jogador não disse “continue”: perguntar se retoma a cena. Se disse “refresh e continue”: após o formato fixo, retomar a cena com o estado reancorado. |

### Formato de resposta obrigatório

```markdown
**Boot refresh OK**
- Data in-game: …
- Região / local / período: …
- Prioridade (E0XX ou livre): …
- Fato duro 1 (ex. F03 Warden terrestre): …
- Fato duro 2 (ex. F04 Stitch ≠ Doc): …
- Conflito detectado? Não | Sim — fonte vencedora: RAW/board/pack
```

### Quando sugerir (proativo)

- ~40–50 mensagens relevantes no chat
- Mudança de local ou região
- Fim de combate / job
- Jogador confuso sobre “onde estamos” ou “o que está pendente”

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

**Objetivo:** fechar a sessão de forma canônica: resumo + estado + context pack + handoff.

### Passos

| # | Ação |
| - | ---- |
| 1 | Declarar: `Finalizar sessão — playbook completo.` |
| 2 | Ler: `sessao_resumo_template.md`, `registro_arquivos.md` (NNN), `board`, `dashboard_contexto`, `event_queue`, `como_atualizar_arquivos.md`, `context_pack_atual`, `fatos_duros`. |
| 3 | Gerar **rascunho** de `logs/sessao_resumo_NNN.md` (conteúdo como em B). |
| 4 | Montar **tabela de mudanças propostas** (Arquivo → o que muda), usando `como_atualizar_arquivos.md`: |
| | - Missão/local/NPCs → `board`, `dashboard` |
| | - Impacto permanente → `consequencias` |
| | - NPCs → relacionamentos relevantes |
| | - Facção / heat / economia → arquivos correspondentes |
| | - **Sempre no finalize:** `logs/context_pack_atual.md` + `logs/handoff_atual.md` |
| | - `registro_arquivos` se novo resumo ou arquivo |
| 5 | **Mostrar ao jogador:** (1) resumo completo; (2) tabela Arquivo → mudança. |
| 6 | **Parar.** Pedir confirmação explícita: aplicar arquivos? commit/push? |
| 7 | **Só após confirmação:** escrever arquivos no workspace. |
| 8 | Ordem de escrita: `sessao_resumo_NNN` → board → dashboard → event_queue → consequencias/rels (se houver) → **context_pack** → **handoff** → registro. |
| 9 | Responder com: lista de paths alterados + próximo NNN+1 + lembrete de colar prompt do handoff se abrir chat novo. |
| 10 | Commit/push **somente** se o jogador confirmou. |

### Caso especial: só RP, estado canônico igual

Ainda gerar resumo mínimo; atualizar handoff + context pack com “sem mudança mecânica / só roleplay”; board só se data/local in-game avançou.

### Se passou 1+ dia in-game na sessão

Após confirmação, seguir também [pulso_procedimento.md](pulso_procedimento.md) se aplicável à **região atual** (não forçar pulso Pack em NC).

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
| | - Regras duras (F03, F04, F11, …) |
| | - **Prompt de abertura colável** (tier-0 primeiro: context pack) |
| 6 | Se o NOW mudou: atualizar também `logs/context_pack_atual.md`. |
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

---

## Tabela rápida

| Comando | Edita arquivos? | Precisa confirmação para gravar? |
| ------- | --------------- | -------------------------------- |
| `[Refresh contexto]` | Não | — |
| `[Resumo da Sessão]` / `[Criar resumo…]` | Só se jogador pedir (b) | Sim para gravar |
| `[Finalizar sessão e gerar resumo]` | Sim (após sim) | **Sim** antes de gravar |
| `[Gerar handoff…]` / `[Preparar novo chat]` | Sim (handoff ± pack) | Sim para commit/push; gravar local pode ser imediato se o jogador pediu o handoff |
| `[Carregar cena]` | Não | — |
| `[Verificar fato]` | Não | — |

---

## Referências

- [Context pack](../logs/context_pack_atual.md) · [Fatos duros](fatos_duros.md) · [Instruções](instrucoes_projeto.md)
- [Diretrizes IA](diretrizes_ia.md) · [Como atualizar](como_atualizar_arquivos.md) · [Novo chat](novo_chat_procedimento.md)
- [Template resumo](../logs/sessao_resumo_template.md) · [Template handoff](../logs/handoff_template.md)
