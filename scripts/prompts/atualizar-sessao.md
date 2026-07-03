# Tarefa: Atualizar campanha Cyberpunk RED a partir de delta Grok

Você está no repositório `Cyberpunk` (campanha solo Ryan "Wireghost" Voss). Siga **estritamente** os arquivos em `sistema/diretrizes_ia.md`, `sistema/instrucoes_projeto.md` e `sistema/como_atualizar_arquivos.md`.

## Regras absolutas

- **Não invente** eventos, NPCs ou consequências. Só registre o que aparece no delta abaixo ou já está nos arquivos do repo.
- Leia o estado atual antes de editar: `board/board_campanha.md`, `sistema/dashboard_contexto.md`, `consequencias/consequencias_persistentes.md`, `relacionamentos/ryan_relacionamentos.md`, `heat.md`, `event_queue.md`, `reputacao.md`, `economia.md`.
- Use `relacionamentos/mapa_relacional_geral.md` para localizar fichas NPC.
- Próximo resumo de sessão: **logs/sessao_resumo_{SESSION_NUM}.md** (template: `logs/sessao_resumo_template.md`).

## Delta a processar

Os arquivos em `.grok-sync/deltas/` contêm **apenas mensagens novas** desde o último sync. Leia todos os `*.md` nessa pasta.

## O que fazer

1. **Criar** `logs/sessao_resumo_{SESSION_NUM}.md` com o que aconteceu no delta (eventos, mudanças, decisões, pendências). Cabeçalho: `# Resumo de Sessão — {SESSION_NUM}`.
2. **Atualizar** todos os arquivos afetados conforme `sistema/como_atualizar_arquivos.md` (board, dashboard, consequências, relacionamentos, heat/event_queue/reputacao/economia se aplicável, fichas NPC se houver NPC novo ou mudança relevante).
3. No resumo, preencher a seção **Arquivos Atualizados Nesta Sessão** com links relativos aos arquivos que você modificou.
4. Atualizar `sistema/registro_arquivos.md` se criou job, incidente, NPC ou novo resumo (ajustar "Próximo número disponível" para {NEXT_SESSION_NUM}).
5. Marcar no resumo: `**Enviado para GitHub:** Sim` (o script fará o commit).

## Se o delta for vazio ou irrelevante

Não crie resumo de sessão nem altere arquivos. Escreva em `.grok-sync/last_run_result.txt`: `SKIP: delta vazio ou sem eventos de campanha`.

## Ao terminar

Escreva em `.grok-sync/last_run_result.txt` uma linha `DONE: <lista breve de arquivos alterados>`.