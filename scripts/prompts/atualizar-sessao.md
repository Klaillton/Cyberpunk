# Tarefa: Atualizar campanha Cyberpunk RED a partir de delta Grok

Você está no repositório `Cyberpunk` (campanha solo Ryan "Wireghost" Voss). Siga **estritamente** os arquivos em `sistema/diretrizes_ia.md`, `sistema/instrucoes_projeto.md`, `sistema/como_atualizar_arquivos.md` e o playbook **C** de `sistema/comandos_jogador.md` (matriz de ledgers).

## Regras absolutas

- **Não invente** eventos, NPCs ou consequências. Só registre o que aparece no delta abaixo ou já está nos arquivos do repo.
- Leia o estado atual antes de editar — **matriz completa**:
  - Núcleo: `board/board_campanha.md`, `sistema/dashboard_contexto.md`, `event_queue.md`, `logs/context_pack_atual.md`
  - Ledgers: `consequencias/consequencias_persistentes.md`, `heat.md`, `reputacao.md`, `economia.md`, `logs/downtime_ryan.md`
  - Facções: `facoes/pack_badlands.md` e/ou `facoes/faccoes_geral.md`, `relacionamentos/faccao_relacionamentos.md`
  - Rels: `relacionamentos/ryan_relacionamentos.md` (+ individuais tocados)
  - Se o delta **avança data** ou menciona sono/noite/elipse: `sistema/pulso_procedimento.md` + `pulso_do_mundo/` da região
- Use `relacionamentos/mapa_relacional_geral.md` para localizar fichas NPC.
- Próximo resumo de sessão: **logs/sessao_resumo_{SESSION_NUM}.md** (template: `logs/sessao_resumo_template.md`).

## Delta a processar

Os arquivos em `.grok-sync/deltas/` contêm **apenas mensagens novas** desde o último sync. Leia todos os `*.md` nessa pasta.

## O que fazer

1. **Criar** `logs/sessao_resumo_{SESSION_NUM}.md` com o que aconteceu no delta (eventos, mudanças, decisões, pendências). Cabeçalho: `# Resumo de Sessão — {SESSION_NUM}`. Preencher seções Rep/Heat/Econ, Downtime, Facções/Consequências, Pulsos — usar **“sem delta”** quando avaliou e nada mudou.
2. **Calcular** data in-game início→fim e dias cobertos.
3. **Atualizar** a matriz de arquivos conforme `sistema/como_atualizar_arquivos.md` e playbook C:
   - Sempre avaliar board, dashboard, event_queue, consequências, facções, heat, reputação, economia
   - Downtime se Ryan produziu
   - Pulso se 1+ dia (ciclos ou gap B1 documentado — **não inventar d100 retroativos**)
   - Relacionamentos tocados
   - Sempre: context_pack + handoff se for fechamento de sessão
4. No resumo, preencher **Arquivos Avaliados / Atualizados** com links relativos.
5. Atualizar `sistema/registro_arquivos.md` se criou job, incidente, NPC ou novo resumo (ajustar "Próximo número disponível" para {NEXT_SESSION_NUM}).
6. Marcar no resumo: `**Enviado para GitHub:** Sim` (o script fará o commit).

## Se o delta for vazio ou irrelevante

Não crie resumo de sessão nem altere arquivos. Escreva em `.grok-sync/last_run_result.txt`: `SKIP: delta vazio ou sem eventos de campanha`.

## Ao terminar

Escreva em `.grok-sync/last_run_result.txt` uma linha `DONE: <lista breve de arquivos alterados>`.
