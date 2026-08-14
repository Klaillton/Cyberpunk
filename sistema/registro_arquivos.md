# Registro de Arquivos do Projeto - Cyberpunk RED

**Última atualização:** 2026-08-14 (Finalizar sessão 019; Ruleset v1.3.0; próximo resumo **020**)

Este arquivo é o **índice central** do projeto. A IA deve consultá-lo primeiro para identificar onde buscar cada tipo de informação.

---

## Guia de Consulta Cruzada

Use esta tabela para saber **qual arquivo abrir** conforme o tipo de informação necessária.

| Preciso de… | Arquivo principal | Arquivos relacionados |
| ----------- | ----------------- | --------------------- |
| Estado narrativo atual (missão, local, NPCs ativos) | `board/board_campanha.md` | `sistema/dashboard_contexto.md`, `consequencias/consequencias_persistentes.md` |
| Resumo rápido para início de sessão | `sistema/dashboard_contexto.md` | `board/board_campanha.md`, `reputacao.md`, `heat.md`, `event_queue.md` |
| Impactos permanentes de eventos passados | `consequencias/consequencias_persistentes.md` | `board/board_campanha.md`, `logs/sessao_resumo_*.md` |
| Reputação com facções/NPCs | `reputacao.md` | `relacionamentos/faccao_relacionamentos.md`, `facoes/` |
| Exposição / perseguição | `heat.md` | `event_queue.md`, `consequencias/consequencias_persistentes.md`, `sistema/echo_exposicao.md` |
| Eventos pendentes no mundo | `event_queue.md` | `board/board_campanha.md`, `board/arco_ativo.md`, `consequencias/consequencias_persistentes.md` |
| Arco em foco (L1) + NPCs off-screen | `board/arco_ativo.md` | `logs/context_pack_atual.md` (AGENDA), `event_queue.md` |
| Ambientação / ganchos / imagem opcional | `sistema/cena_ambientacao_ganchos.md` | `motor_cena_1pager.md`, `arco_ativo.md` §7 |
| Relações do protagonista | `relacionamentos/ryan_relacionamentos.md` | `relacionamentos/mapa_relacional_geral.md`, `relacionamentos/crew_relacionamentos.md` |
| **Tier-0 / anti-esquecimento sandbox** | `logs/context_pack_atual.md` | `fatos_duros.md`, `comandos_jogador.md`, bloco **MOTOR** + **AGENDA** |
| Fatos que não se inventam | `sistema/fatos_duros.md` | context pack, board |
| Playbooks de comandos do jogador | `sistema/comandos_jogador.md` | instrucoes_projeto, diretrizes_ia |
| **Abrir chat novo / handoff** | `sistema/novo_chat_procedimento.md` | `logs/handoff_atual.md`, `logs/context_pack_atual.md`, último `sessao_resumo_*.md` |
| Continuidade colável (estado vigente) | `logs/handoff_atual.md` | context pack, board |
| **Regras RED (mecânica / testes)** | `sistema/regras_red/11_referencia.md` (atalho) | `00`–`10` full · Ruleset **1.3.0** · **não** tier-0 |

**Padrão de resumos de sessão:** `logs/sessao_resumo_XXX.md` (ex.: `001` … `019`). Próximo número disponível: **020**.

---

## Observações Gerais

- O `registro_arquivos.md` é o **arquivo de referência central**.
- **Resumos de Sessão:** Padrão `logs/sessao_resumo_XXX.md`. Próximo número: **020**.
- **Ruleset:** v1.3.0 em `sistema/regras_red/` (sessão 017+; F18).
- **Handoff / chat novo:** Após sessão, atualizar `logs/handoff_atual.md` via [novo_chat_procedimento.md](novo_chat_procedimento.md).
- **NPCs secundários:** Um arquivo em `fichas/npc/<slug>.md`. Handles de rádio (**Sparrow**, **Steel**, Scout) = **pessoas** — ver `lina_park.md`, `marcus_steel_rivera.md`, `scout.md`.
- O **Source of Truth** permanece nos arquivos do repo (`feature/linha-estavel`).

---

## Referências

- [README.md](../README.md)
- [Instruções do Projeto](instrucoes_projeto.md) · [Diretrizes IA](diretrizes_ia.md) · [Diretrizes Narrador](diretrizes_narrador.md) · [Como Atualizar](como_atualizar_arquivos.md) · [Novo Chat](novo_chat_procedimento.md)
- [Dashboard de Contexto](dashboard_contexto.md) · [Board](../board/board_campanha.md)
- [Mapa Relacional Geral](../relacionamentos/mapa_relacional_geral.md)
- [Sessão 019](../logs/sessao_resumo_019.md) · [Context pack](../logs/context_pack_atual.md) · [Handoff](../logs/handoff_atual.md)
