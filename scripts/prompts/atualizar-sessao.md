# Tarefa: Atualizar campanha Cyberpunk RED a partir de delta Grok (proposal-first)

Você está no repositório `Cyberpunk` (campanha solo Ryan "Wireghost" Voss). Siga **estritamente** os arquivos em `sistema/diretrizes_ia.md`, `sistema/instrucoes_projeto.md` e `sistema/como_atualizar_arquivos.md`.

## Regras absolutas

- **Não invente** eventos, NPCs ou consequências. Só registre o que aparece no delta abaixo ou já está nos arquivos do repo.
- Leia o estado atual antes de editar: `board/board_campanha.md`, `sistema/dashboard_contexto.md`, `consequencias/consequencias_persistentes.md`, `relacionamentos/ryan_relacionamentos.md`, `heat.md`, `event_queue.md`, `reputacao.md`, `economia.md`.
- Use `relacionamentos/mapa_relacional_geral.md` para localizar fichas NPC.
- Próximo resumo de sessão: **logs/sessao*resumo*{SESSION_NUM}.md** (template: `logs/sessao_resumo_template.md`).

## Delta a processar

Os arquivos em `.grok-sync/deltas/` contêm **apenas mensagens novas** desde o último sync. Leia todos os `*.md` nessa pasta.

## O que fazer

1. Gere uma proposta estruturada por lotes (JSON) em vez de editar diretamente os arquivos.
2. Cada lote deve ter: `id`, `label`, `risk`, `rationale`, `items`.
3. Cada item deve ter: `action`, `file_path`, `hash_before` e, quando aplicável, `new_content`.
4. Agrupe alterações relacionadas no mesmo lote e mantenha lotes pequenos/auditáveis.
5. O pipeline fará revisão, aprovação e aplicação atômica depois.

## Se o delta for vazio ou irrelevante

Retorne JSON com `batches: []` e `summary` explicando que não há mudanças relevantes.

## Ao terminar

Retorne somente JSON válido com a proposta. Não inclua texto adicional fora do JSON.
