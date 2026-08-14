# Registro de Arquivos do Projeto - Cyberpunk RED

**Última atualização:** 2026-08-14 (Finalizar sessão 019; Ruleset v1.3.0; próximo resumo **020**)

Este arquivo é o **índice central** do projeto. A IA deve consultá-lo primeiro para identificar onde buscar cada tipo de informação.

---

## Guia de Consulta Cruzada

| Preciso de… | Arquivo principal | Arquivos relacionados |
| ----------- | ----------------- | --------------------- |
| Estado narrativo atual | `board/board_campanha.md` | `sistema/dashboard_contexto.md`, `consequencias/consequencias_persistentes.md` |
| Resumo rápido | `sistema/dashboard_contexto.md` | board, reputacao, heat, event_queue |
| Impactos permanentes | `consequencias/consequencias_persistentes.md` | board, `logs/sessao_resumo_*.md` |
| Reputação | `reputacao.md` | `relacionamentos/faccao_relacionamentos.md`, `facoes/` |
| Heat / exposição | `heat.md` | event_queue, consequencias, `sistema/echo_exposicao.md` |
| Eventos pendentes | `event_queue.md` | board, `board/arco_ativo.md` |
| Arco L1 + off-screen | `board/arco_ativo.md` | `logs/context_pack_atual.md`, event_queue |
| Ambientação / ganchos | `sistema/cena_ambientacao_ganchos.md` | motor_cena_1pager, arco_ativo §7 |
| Relações do protagonista | `relacionamentos/ryan_relacionamentos.md` | mapa_relacional_geral, crew_relacionamentos |
| Relação Valk | `relacionamentos/lena_valk_kane_relacionamentos.md` | ryan_relacionamentos |
| NPC secundário | `fichas/npc/<slug>.md` | mapa_relacional_geral |
| **Tier-0** | `logs/context_pack_atual.md` | fatos_duros, comandos_jogador |
| Fatos duros | `sistema/fatos_duros.md` | context pack, board |
| Comandos do jogador | `sistema/comandos_jogador.md` | instrucoes_projeto, diretrizes_ia |
| Handoff / chat novo | `sistema/novo_chat_procedimento.md` | `logs/handoff_atual.md`, context_pack, último resumo |
| Continuidade colável | `logs/handoff_atual.md` | context pack, board |
| Regras RED | `sistema/regras_red/11_referencia.md` | `00`–`10` · Ruleset **1.3.0** · **não** tier-0 |
| Loadout Ryan | `fichas/ryan_loadout.md` | SoT armas/drones |
| House rules | `sistema/house_rules/regras_campanha.md` | regras_red/00, F03/F12/F16/F18 |

**Padrão de resumos de sessão:** `logs/sessao_resumo_XXX.md` (ex.: `001` … `019`). Próximo número disponível: **020**.

---

## Observações Gerais

- O `registro_arquivos.md` é o **arquivo de referência central**.
- **Resumos de Sessão:** Padrão `logs/sessao_resumo_XXX.md`. Próximo número: **020**.
- **Ruleset:** v1.3.0 (sessão 017+; F18).
- **Handoff / chat novo:** Atualizar `logs/handoff_atual.md` após sessão.
- **NPCs secundários:** `fichas/npc/<slug>.md`. Handles **Sparrow** / **Steel** / Scout = **pessoas** (F20).
- **Source of Truth:** arquivos do repo `feature/linha-estavel`.

### Arquivos críticos pós-019

| Arquivo | Nota |
| ------- | ---- |
| `logs/sessao_resumo_019.md` | Resumo completo 019 |
| `logs/context_pack_atual.md` | Tier-0 · Pack ~27/07 noite |
| `logs/handoff_atual.md` | Prompt sessão 020 |
| `board/board_campanha.md` | Pack pós-retorno |
| `board/arco_ativo.md` | Fase ad no ar + retorno Pack |
| `event_queue.md` | E015 ad ativo; E016 residual Sasha/Lira |
| `fichas/npc/sasha.md` / `lira.md` | Residual positivo 019 |
| `relacionamentos/ryan_relacionamentos.md` | Acordo Valk + residual Sasha/Lira |
| `relacionamentos/lena_valk_kane_relacionamentos.md` | Acordo comunicação ops 019 |

---

## Referências

- [README.md](../README.md) · [Instruções](instrucoes_projeto.md) · [Diretrizes IA](diretrizes_ia.md) · [Novo Chat](novo_chat_procedimento.md)
- [Dashboard](dashboard_contexto.md) · [Board](../board/board_campanha.md) · [Arco](../board/arco_ativo.md)
- [Sessão 019](../logs/sessao_resumo_019.md) · [Context pack](../logs/context_pack_atual.md) · [Handoff](../logs/handoff_atual.md)
