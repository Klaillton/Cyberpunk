# Como Atualizar os Arquivos da Campanha

Este arquivo serve como referência rápida para manter os arquivos da campanha atualizados de forma organizada, especialmente quando a campanha está espalhada em vários chats.

---

## Fluxo Recomendado

### Regra Principal

Sempre seja o mais específico possível sobre **qual arquivo** você quer atualizar.

Quanto mais específico você for, menor o risco de inconsistências.

### Ordem de Prioridade

1. **Chats atuais / recentes** → Use comandos específicos (nome do arquivo).
2. **Chats antigos ou longos** → Peça primeiro um **resumo das atualizações** antes de aplicar.
3. **Sempre que possível** → Peça para eu mostrar as mudanças propostas antes de confirmar.

---

## Comandos Recomendados

### Comando Genérico (bom para chats antigos)

"Analise este chat e atualize os arquivos da campanha conforme o que aconteceu.
Atualize Board, Consequências Persistentes, Relacionamentos relevantes e Downtime se aplicável.
Se tiver dúvidas ou precisar de mais contexto antes de aplicar as mudanças, me pergunte primeiro."

### Templates Prontos (mais seguros)

| Finalidade                               | Comando                                                                                                                                                                                  |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Atualização geral de sessão**          | `Com base neste chat, atualize o Board e as Consequências Persistentes com o que aconteceu. Depois me mostre um resumo das mudanças propostas.`                                          |
| **Foco em Relacionamentos**              | `Analise este chat e atualize os arquivos de relacionamentos (ryan_relacionamentos.md, crew_relacionamentos.md, faccao_relacionamentos.md) com as interações e mudanças que ocorreram.`  |
| **Foco em Arco Polycule**                | `Analise este chat e atualize crew_polycule_ryan_valk_alex_reina.md (fase atual, eventos, conflitos) e os arquivos individuais de Ryan, Valk, Alex e Reina conforme necessário.`        |
| **Foco em Downtime**                     | `Atualize o downtime_ryan.md com as atividades que Ryan realizou nesse período.`                                                                                                         |
| **Atualização completa (com segurança)** | `Faça uma análise completa deste chat e proponha atualizações para Board, Consequências, Relacionamentos, Downtime, sugira outros arquivos a serem atualizados/criados. Só aplique depois que eu confirmar.`                                |
| **Chats muito antigos / confusos**       | `Leia este chat antigo e extraia os eventos importantes que ainda não estão registrados nos arquivos da campanha. Me mostre um resumo primeiro.`                                         |
| **Resumo rápido**                        | `[Faça um resumo do que precisa ser atualizado nos arquivos após essa sessão, liste tbm em quais arquivos ocorrerão essas atualizações; Me mostre o resumo antes de qualquer alteração]` |

---

## Boas Práticas

### 1. Sempre mencione o nome do arquivo quando possível

Exemplos bons:

- `Atualize o board_campanha.md com...`
- `Adicione no ryan_relacionamentos.md o seguinte...`
- `Atualize o consequencias_persistentes.md com o evento...`

### 2. Peça resumo antes de aplicar (especialmente em chats antigos)

Comando recomendado:

> “Faça um resumo do que precisa ser atualizado nos arquivos e depois aplique as mudanças.”

### 3. Para chats muito longos ou antigos

Use este fluxo:

1. Peça um resumo primeiro.
2. Revise o resumo.
3. Confirme para eu aplicar as mudanças.

### 4. Atualização em lote

Você pode pedir para atualizar vários arquivos de uma vez:

> “Atualize o Board, as Consequências e os Relacionamentos com base no que rolou nessa sessão.”

### 5. Quando estiver em dúvida

Peça:

> “Me ajude a identificar o que precisa ser atualizado nos arquivos depois dessa sessão.”

---

## Arquivos a Atualizar por Tipo de Evento

| O que aconteceu na sessão | Arquivos a atualizar |
| ------------------------- | -------------------- |
| Mudança de missão, local ou NPCs ativos | `board/board_campanha.md`, `sistema/dashboard_contexto.md` |
| Novo impacto permanente | `consequencias/consequencias_persistentes.md` |
| Interação com NPC | `relacionamentos/ryan_relacionamentos.md` e/ou arquivo individual + `crew_relacionamentos.md` |
| Progresso no arco polycule | `relacionamentos/crew_polycule_ryan_valk_alex_reina.md` + arquivos individuais dos envolvidos + `crew_relacionamentos.md` |
| Mudança com facção | `relacionamentos/faccao_relacionamentos.md`, `facoes/`, `reputacao.md` |
| Ação chamativa / discrição | `heat.md`, possivelmente `event_queue.md` |
| Dinheiro, recursos, projetos | `economia.md`, `logs/downtime_ryan.md` |
| Evento futuro agendado | `event_queue.md` |
| Fim de sessão | `logs/sessao_resumo_XXX.md` (próximo: `011`) + todos os arquivos acima afetados |
| Abrir chat novo / continuidade | [novo_chat_procedimento.md](novo_chat_procedimento.md) → atualizar `logs/handoff_atual.md` |
| Pedido de handoff | `[Gerar handoff para novo chat]` — sobrescrever `logs/handoff_atual.md` |
| Passou 1+ dia in-game / Ryan dormiu a noite | [pulso_procedimento.md](pulso_procedimento.md) → `pulso_do_mundo/` + `event_queue` / `consequencias` se impacto |
| Job / gig concluído | `logs/job_XXX_<slug>.md` (usar [job_template.md](../logs/job_template.md)) + consequências, heat, event_queue |
| NPC com personalidade ou arco próprio | `fichas/npc/<slug>.md` (usar [npc_template.md](../fichas/npc/npc_template.md)) + entrada em [mapa_relacional_geral.md](../relacionamentos/mapa_relacional_geral.md) |
| Tempo off-screen (mundo vivo) | [pulso_procedimento.md](pulso_procedimento.md) + pulso em `pulso_do_mundo/` + opcional `logs/pulso_YYYYMMDD.md` |

Consulte a tabela completa em [registro_arquivos.md](registro_arquivos.md) (seção "Guia de Consulta Cruzada").

## Estrutura de Pastas (Referência Rápida)

Ver estrutura completa e atualizada em [registro_arquivos.md](registro_arquivos.md).

---

## Dica Final

- **Chats atuais**: Seja específico.
- **Chats antigos**: Peça resumo primeiro.
- **Sempre**: Eu mostro as mudanças propostas antes de você confirmar a aplicação final nos seus arquivos locais.

Manter esse hábito evita bagunça e inconsistências conforme a campanha cresce.

---

## Referências

- [Registro de Arquivos](registro_arquivos.md) · [Dashboard de Contexto](dashboard_contexto.md) · [Diretrizes IA](diretrizes_ia.md) · [Novo Chat](novo_chat_procedimento.md) · [Pulso do Mundo](pulso_procedimento.md)
- [Board](../board/board_campanha.md) · [Mapa Relacional](../relacionamentos/mapa_relacional_geral.md)
- [Template de Resumo](../logs/sessao_resumo_template.md)
