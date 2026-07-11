# Handoff — Template (não usar com estado vivo)

> **Uso:** copiar estrutura para regenerar `logs/handoff_atual.md` via [sistema/novo_chat_procedimento.md](../sistema/novo_chat_procedimento.md).  
> **Não** preencher este arquivo com estado da campanha — o vigente é sempre `handoff_atual.md`.

---

## Metadados

| Campo | Valor |
| ----- | ----- |
| Gerado após sessão | `XXX` |
| Próxima sessão | `XXX+1` / `sessao_resumo_NNN.md` |
| Data in-game ao fechar | DD/MM/AAAA · período |
| Branch | `feature/linha-estavel` |
| Share Grok (opcional) | URL |

---

## Prompt de abertura (colar no chat novo)

```markdown
# Cyberpunk RED — Continuidade (Sessão NNN)

## Boot obrigatório
- Repo: https://github.com/Klaillton/Cyberpunk
- Branch: `feature/linha-estavel`
- Canon = arquivos do repo após sync
- RAW board: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/board/board_campanha.md
- RAW última sessão: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/sessao_resumo_XXX.md
- Handoff: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/handoff_atual.md
- Procedimento: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/sistema/novo_chat_procedimento.md
- Share (auxiliar): [URL se houver]

Leia: instrucoes_projeto → diretrizes_ia → handoff_atual → dashboard → board → último sessao_resumo → event_queue / consequencias recentes → relacionamentos em cena.

## Estado atual
- Data / local / prioridade
- Cena de abertura

## O que acabou de acontecer
- …

## Pendências
- …

## Projetos / NPCs quentes
- …

## Regras duras
- Sem meta-game; Warden = drone terrestre scorpion-like; datas do board; próximo resumo NNN

## Comece
Confirme boot em 1 frase e continue a partir de: [gancho]
```

---

## Notas da IA ao gerar

- Máx. ~1–2 telas; não recontar sessões antigas.
- IDs de `event_queue` quando existirem.
- Segredos: marcar o que ainda é secreto in-fiction.
