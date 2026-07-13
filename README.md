# Cyberpunk RED — Campanha Solo

Bem-vindo à campanha de Cyberpunk RED.

> As instruções de boot da IA também estão na **descrição do projeto** (configuração do repositório).
> A versão versionada e completa está em [sistema/instrucoes_projeto.md](sistema/instrucoes_projeto.md); o detalhamento operacional está nos arquivos abaixo.

Visão geral da estrutura do projeto e de como os arquivos se conectam entre si.

**Source of Truth:** Os arquivos no computador local do jogador (após sync com o repositório).

---

## Por Onde Começar

| Papel | Arquivo inicial |
| ----- | --------------- |
| Jogador / Narrador humano | Este arquivo (`README.md`) |
| IA (instruções do projeto) | [sistema/instrucoes_projeto.md](sistema/instrucoes_projeto.md) |
| IA (boot sequence) | [sistema/diretrizes_ia.md](sistema/diretrizes_ia.md) |
| Índice completo do projeto | [sistema/registro_arquivos.md](sistema/registro_arquivos.md) |
| Estado rápido da campanha | [sistema/dashboard_contexto.md](sistema/dashboard_contexto.md) |
| Situação narrativa atual | [board/board_campanha.md](board/board_campanha.md) |

### Arquivos principais

- [registro_arquivos.md](sistema/registro_arquivos.md) — Índice central e guia de referências cruzadas
- [instrucoes_projeto.md](sistema/instrucoes_projeto.md) — Instruções do projeto (boot da IA)
- [diretrizes_ia.md](sistema/diretrizes_ia.md) — Boot sequence e regras da IA
- [diretrizes_narrador.md](sistema/diretrizes_narrador.md) — Regras de narração
- [como_atualizar_arquivos.md](sistema/como_atualizar_arquivos.md) — Como manter os arquivos atualizados
- [context_pack_atual.md](logs/context_pack_atual.md) — **Tier-0** (NOW + fatos; anti-esquecimento sandbox)
- [comandos_jogador.md](sistema/comandos_jogador.md) — Playbooks `[Refresh]`, `[Finalizar]`, handoff, etc.
- [fatos_duros.md](sistema/fatos_duros.md) — Fatos que a IA não pode inventar
- [novo_chat_procedimento.md](sistema/novo_chat_procedimento.md) — Procedimento para abrir chat novo + handoff
- [handoff_atual.md](logs/handoff_atual.md) — Continuidade colável (estado vigente)
- [dashboard_contexto.md](sistema/dashboard_contexto.md) — Resumo rápido (não substitui context pack)
- [board_campanha.md](board/board_campanha.md) — Board oficial da campanha
- [mapa_relacional_geral.md](relacionamentos/mapa_relacional_geral.md) — Hub de personagens e relações

---

## Fluxo de Consulta da IA

```text
context_pack_atual.md + fatos_duros.md  →  tier-0 (sempre)
        ↓
board (se pack divergir) + tier-1 da cena (região atual)
        ↓
registro_arquivos.md  →  achar arquivo sob demanda
        ↓
mapa_relacional / ficha / relacionamentos  →  NPC em cena
```

---

## Pastas e Finalidade

| Pasta | Conteúdo | Quando consultar |
| ----- | -------- | ---------------- |
| `board/` | Estado narrativo atual da campanha | Toda sessão |
| `consequencias/` | Impactos permanentes de eventos passados | Antes de narrar consequências |
| `relacionamentos/` | Dinâmicas entre personagens e facções | Interações com NPCs |
| `fichas/` | Fichas mecânicas dos personagens | Combate, testes, atributos |
| `fichas/notas_narrador/` | Material restrito do narrador (ex.: passado de Ryan) | Revelação gradual, gatilhos |
| `facoes/` | Detalhes de facções | Cenas com grupos/corporações |
| `logs/` | Resumos de sessão e downtime | Retomar contexto, registrar mudanças |
| `sistema/` | Regras, índice e guias de manutenção | Boot da IA, atualizações |
| Raiz (`*.md`) | Estado mecânico global | Reputação, heat, eventos, economia |

---

## Como Manter Atualizado

Consulte [sistema/como_atualizar_arquivos.md](sistema/como_atualizar_arquivos.md) para comandos e fluxo de atualização pós-sessão.

Para **abrir um chat novo** sem perder continuidade: [sistema/novo_chat_procedimento.md](sistema/novo_chat_procedimento.md) e cole o prompt de [logs/handoff_atual.md](logs/handoff_atual.md) (tier-0 = [context pack](logs/context_pack_atual.md)).

**Sandbox Grok esqueceu arquivos/fatos?** Peça `[Refresh contexto]` (playbook em [comandos_jogador.md](sistema/comandos_jogador.md)) ou reabra o chat com o context pack RAW.

Após cada sessão, os arquivos mais críticos a revisar são:

- [board/board_campanha.md](board/board_campanha.md)
- [consequencias/consequencias_persistentes.md](consequencias/consequencias_persistentes.md)
- [relacionamentos/ryan_relacionamentos.md](relacionamentos/ryan_relacionamentos.md)
- [sistema/dashboard_contexto.md](sistema/dashboard_contexto.md)
- Novo resumo em `logs/sessao_resumo_XXX.md` (próximo: `009`)

---

## Referências

- [Instruções do Projeto](sistema/instrucoes_projeto.md) · [Registro de Arquivos](sistema/registro_arquivos.md)
- [Diretrizes IA](sistema/diretrizes_ia.md) · [Diretrizes Narrador](sistema/diretrizes_narrador.md)
- [Mapa Relacional Geral](relacionamentos/mapa_relacional_geral.md)
- [Arco Polycule (futuro)](relacionamentos/crew_polycule_ryan_valk_alex_reina.md)
- [Board de Campanha](board/board_campanha.md)
