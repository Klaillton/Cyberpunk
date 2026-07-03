# Registro de Arquivos do Projeto - Cyberpunk RED

**Última atualização:** 02 de Julho de 2026

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
| Exposição / perseguição | `heat.md` | `event_queue.md`, `consequencias/consequencias_persistentes.md` |
| Eventos pendentes no mundo | `event_queue.md` | `board/board_campanha.md`, `consequencias/consequencias_persistentes.md` |
| Situação financeira | `economia.md` | `board/board_campanha.md`, `logs/downtime_ryan.md` |
| Relações do protagonista | `relacionamentos/ryan_relacionamentos.md` | `relacionamentos/mapa_relacional_geral.md`, `relacionamentos/crew_relacionamentos.md` |
| Dinâmica entre membros da crew | `relacionamentos/crew_relacionamentos.md` | `relacionamentos/mapa_relacional_geral.md` |
| Arco romântico futuro (polycule) | `relacionamentos/crew_polycule_ryan_valk_alex_reina.md` | `relacionamentos/crew_relacionamentos.md`, arquivos individuais |
| Relações com facções | `relacionamentos/faccao_relacionamentos.md` | `facoes/pack_badlands.md`, `facoes/faccoes_geral.md`, `reputacao.md` |
| Hub de personagens (onde achar cada NPC) | `relacionamentos/mapa_relacional_geral.md` | `fichas/`, `relacionamentos/*_relacionamentos.md` |
| Ficha mecânica de personagem | `fichas/<personagem>.md` | Relacionamento correspondente em `relacionamentos/` |
| Detalhes de facção ativa | `facoes/pack_badlands.md` | `relacionamentos/faccao_relacionamentos.md`, `reputacao.md` |
| Facções menores / superficiais | `facoes/faccoes_geral.md` | `relacionamentos/faccao_relacionamentos.md` |
| Atividades de downtime do Ryan | `logs/downtime_ryan.md` | `board/board_campanha.md`, `fichas/techie - ryan_wireghost_voss.md` |
| Histórico de sessão | `logs/sessao_resumo_XXX.md` | Arquivos listados na seção "Arquivos Atualizados" de cada resumo |
| Instruções do projeto (boot) | `sistema/instrucoes_projeto.md` | `diretrizes_ia.md`, este arquivo |
| Regras da IA (boot sequence) | `sistema/diretrizes_ia.md` | `instrucoes_projeto.md`, este arquivo |
| Regras do narrador | `sistema/diretrizes_narrador.md` | `sistema/diretrizes_ia.md` |
| Como atualizar após sessão | `sistema/como_atualizar_arquivos.md` | Este arquivo |

**Padrão de resumos de sessão:** `logs/sessao_resumo_XXX.md` (ex.: `001`, `002`, `003`, `004`). Próximo número disponível: **005**.

---

## Estrutura Geral do Projeto

```text
cyberpunk/
├── LEIA-ME.md                     ← Visão geral e fluxo de consulta
├── README.md                      ← Entrada rápida
├── reputacao.md                   ← Reputação por facção/NPC
├── heat.md                        ← Exposição / perseguição
├── event_queue.md                 ← Eventos pendentes
├── economia.md                    ← Estado financeiro
├── base/                          ← PDFs de referência
│   ├── Cyberpunk Red.pdf
│   └── Night City 2045 Atlas Full.pdf
├── board/
│   ├── board_campanha.md          ← Board oficial (estado narrativo)
│   └── campanha_referencia.md     ← Snapshot histórico (23/06)
├── consequencias/
│   └── consequencias_persistentes.md
├── facoes/
│   ├── faccao_template.md
│   ├── pack_badlands.md
│   └── faccoes_geral.md
├── fichas/
│   ├── fixer - kaz_the_broker_takahashi.md
│   ├── medtech - stephania_doc_voss.md
│   ├── netrunner - alex_specter_kane.md
│   ├── nomad - lena_valk_kane.md
│   ├── solo - jax_razor_kane.md
│   ├── solo - reina_bearclaw_morales.md
│   ├── techie - ryan_wireghost_voss.md
│   └── vehicle - the_mule.md
├── imagens/
│   ├── fixer - kaz_the_broker_takahashi.jpg
│   ├── medtech - stephania_doc_voss.jpg
│   ├── netrunner - alex_specter_kane.jpg
│   ├── nomad - lena_valk_kane.jpg
│   ├── solo - jax_razor_kane.png
│   ├── solo - reina_bearclaw_morales.png
│   ├── techie - ryan_wireghost_voss.jpg
│   └── vehicle - the_mule.jpg
├── logs/
│   ├── downtime_ryan.md
│   ├── sessao_resumo_template.md
│   ├── sessao_resumo_001.md
│   ├── sessao_resumo_002.md
│   ├── sessao_resumo_003.md
│   └── sessao_resumo_004.md
├── relacionamentos/
│   ├── mapa_relacional_geral.md   ← Hub de personagens
│   ├── ryan_relacionamentos.md
│   ├── crew_relacionamentos.md
│   ├── crew_polycule_ryan_valk_alex_reina.md
│   ├── faccao_relacionamentos.md
│   ├── alex_specter_kane_relacionamentos.md
│   ├── lena_valk_kane_relacionamentos.md
│   └── reina_bearclaw_morales_relacionamentos.md
└── sistema/
    ├── instrucoes_projeto.md      ← Instruções do projeto (espelho versionado)
    ├── como_atualizar_arquivos.md
    ├── dashboard_contexto.md
    ├── diretrizes_ia.md
    ├── diretrizes_narrador.md
    └── registro_arquivos.md       ← Este arquivo
```

---

## Arquivos de Estado do Mundo

| Arquivo | Status | Finalidade | Consultar junto com |
| ------- | ------ | ---------- | ------------------- |
| `board/board_campanha.md` | Ativo | Estado narrativo atual | `dashboard_contexto.md`, `consequencias/consequencias_persistentes.md` |
| `reputacao.md` | Ativo | Reputação por facção e NPC | `relacionamentos/faccao_relacionamentos.md`, `facoes/` |
| `heat.md` | Ativo | Nível de exposição/perseguição | `event_queue.md`, `consequencias/consequencias_persistentes.md` |
| `event_queue.md` | Ativo | Fila de eventos globais pendentes | `board/board_campanha.md`, `heat.md` |
| `economia.md` | Ativo | Estado financeiro e econômico | `board/board_campanha.md`, `logs/downtime_ryan.md` |
| `consequencias/consequencias_persistentes.md` | Ativo | Impactos permanentes | `board/board_campanha.md`, `logs/sessao_resumo_*.md` |

---

## Arquivos Auxiliares e de Sistema

| Arquivo | Status | Finalidade | Consultar junto com |
| ------- | ------ | ---------- | ------------------- |
| `sistema/dashboard_contexto.md` | Ativo | Resumo rápido para a IA | Todos os arquivos de estado |
| `relacionamentos/mapa_relacional_geral.md` | Ativo | Hub de personagens e relações | `fichas/`, `relacionamentos/` |
| `sistema/instrucoes_projeto.md` | Ativo | Instruções do projeto (espelho versionado) | `diretrizes_ia.md`, descrição do projeto |
| `sistema/diretrizes_ia.md` | Ativo | Boot sequence e regras da IA | `instrucoes_projeto.md`, este arquivo |
| `sistema/diretrizes_narrador.md` | Ativo | Regras de narração | `diretrizes_ia.md` |
| `sistema/como_atualizar_arquivos.md` | Ativo | Guia de manutenção pós-sessão | Este arquivo |
| `LEIA-ME.md` | Ativo | Visão geral do projeto | `README.md` |

---

## Observações Gerais

- O `registro_arquivos.md` é o **arquivo de referência central**.
- Os arquivos mais críticos para manter atualizados são:
  - `board/board_campanha.md`
  - `consequencias/consequencias_persistentes.md`
  - `relacionamentos/ryan_relacionamentos.md`
  - `sistema/dashboard_contexto.md`
  - `relacionamentos/mapa_relacional_geral.md`
- **Resumos de Sessão:** Padrão `logs/sessao_resumo_XXX.md`. Próximo número: **005**.
- **Facções:** Detalhes em `facoes/`. Facções menores em `facoes/faccoes_geral.md`.
- **Referências cruzadas:** Cada arquivo relevante possui seção `## Referências` apontando para arquivos relacionados.
- O **Source of Truth** permanece nos arquivos locais do jogador.

---

## Referências

- [LEIA-ME.md](../LEIA-ME.md) · [README.md](../README.md)
- [Instruções do Projeto](instrucoes_projeto.md) · [Diretrizes IA](diretrizes_ia.md) · [Diretrizes Narrador](diretrizes_narrador.md) · [Como Atualizar](como_atualizar_arquivos.md)
- [Dashboard de Contexto](dashboard_contexto.md) · [Board](../board/board_campanha.md)
- [Mapa Relacional Geral](../relacionamentos/mapa_relacional_geral.md)
