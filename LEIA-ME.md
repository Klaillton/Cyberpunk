# LEIA-ME — Cyberpunk RED (Campanha Solo)

> As instruções de boot da IA também estão na **descrição do projeto** (configuração do repositório).
> A versão versionada e completa está em [sistema/instrucoes_projeto.md](sistema/instrucoes_projeto.md); o detalhamento operacional está nos arquivos abaixo.

Visão geral da estrutura do projeto e de como os arquivos se conectam entre si.

**Source of Truth:** Os arquivos no computador local do jogador (após sync com o repositório).

---

## Por Onde Começar

| Papel | Arquivo inicial |
| ----- | --------------- |
| Jogador / Narrador humano | [README.md](README.md) |
| IA (instruções do projeto) | [sistema/instrucoes_projeto.md](sistema/instrucoes_projeto.md) |
| IA (boot sequence) | [sistema/diretrizes_ia.md](sistema/diretrizes_ia.md) |
| Índice completo do projeto | [sistema/registro_arquivos.md](sistema/registro_arquivos.md) |
| Estado rápido da campanha | [sistema/dashboard_contexto.md](sistema/dashboard_contexto.md) |
| Situação narrativa atual | [board/board_campanha.md](board/board_campanha.md) |

---

## Fluxo de Consulta da IA

```
registro_arquivos.md  →  identificar qual arquivo usar
        ↓
dashboard_contexto.md  →  resumo rápido (início de sessão)
        ↓
board_campanha.md  →  missão, NPCs, facções ativas
        ↓
consequencias + reputacao + heat + event_queue + economia  →  estado mecânico
        ↓
mapa_relacional_geral.md  →  localizar personagem
        ↓
ficha + relacionamentos  →  contexto do NPC em cena
```

---

## Pastas e Finalidade

| Pasta | Conteúdo | Quando consultar |
| ----- | -------- | ---------------- |
| `board/` | Estado narrativo atual da campanha | Toda sessão |
| `consequencias/` | Impactos permanentes de eventos passados | Antes de narrar consequências |
| `relacionamentos/` | Dinâmicas entre personagens e facções | Interações com NPCs |
| `fichas/` | Fichas mecânicas dos personagens | Combate, testes, atributos |
| `facoes/` | Detalhes de facções | Cenas com grupos/corporações |
| `logs/` | Resumos de sessão e downtime | Retomar contexto, registrar mudanças |
| `sistema/` | Regras, índice e guias de manutenção | Boot da IA, atualizações |
| Raiz (`*.md`) | Estado mecânico global | Reputação, heat, eventos, economia |

---

## Como Manter Atualizado

Consulte [sistema/como_atualizar_arquivos.md](sistema/como_atualizar_arquivos.md) para comandos e fluxo de atualização pós-sessão.

Após cada sessão, os arquivos mais críticos a revisar são:

- [board/board_campanha.md](board/board_campanha.md)
- [consequencias/consequencias_persistentes.md](consequencias/consequencias_persistentes.md)
- [relacionamentos/ryan_relacionamentos.md](relacionamentos/ryan_relacionamentos.md)
- [sistema/dashboard_contexto.md](sistema/dashboard_contexto.md)
- Novo resumo em `logs/sessao_resumo_XXX.md` (próximo: `005`)

---

## Referências

- [Instruções do Projeto](sistema/instrucoes_projeto.md) · [Registro de Arquivos](sistema/registro_arquivos.md)
- [Diretrizes IA](sistema/diretrizes_ia.md) · [Diretrizes Narrador](sistema/diretrizes_narrador.md)
- [Mapa Relacional Geral](relacionamentos/mapa_relacional_geral.md)
- [Board de Campanha](board/board_campanha.md)