# Registro de Arquivos do Projeto - Cyberpunk RED

**Última atualização:** 13 de Julho de 2026 (context pack + comandos)

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
| Ficha mecânica de personagem (crew) | `fichas/<personagem>.md` | Relacionamento correspondente em `relacionamentos/` |
| NPC secundário (personalidade + eventos) | `fichas/npc/<slug>.md` | [mapa_relacional_geral.md](../relacionamentos/mapa_relacional_geral.md), facção/job/sessão |
| Detalhes de facção ativa | `facoes/pack_badlands.md` | `relacionamentos/faccao_relacionamentos.md`, `reputacao.md` |
| Facções menores / superficiais | `facoes/faccoes_geral.md` | `relacionamentos/faccao_relacionamentos.md` |
| Atividades de downtime do Ryan | `logs/downtime_ryan.md` | `board/board_campanha.md`, `fichas/techie - ryan_wireghost_voss.md` |
| **Guarda-roupa / visual por ocasião (Ryan)** | `fichas/ryan_guarda_roupas.md` | `imagens/ryan/guarda_roupas/`, ficha techie |
| **Guarda-roupa / peças por ocasião (feminino)** | `fichas/crew_guarda_roupas.md` | `imagens/crew/guarda_roupas/` — foco em **roupa**, não personagem da foto |
| Background e gatilhos do Ryan (narrador) | `fichas/notas_narrador/ryan_background_completo.md` | `fichas/notas_narrador/ryan_gatilhos_memorias.md`, `fichas/techie - ryan_wireghost_voss.md` (Elisa "Doc" Moreau) |
| Histórico de sessão | `logs/sessao_resumo_XXX.md` | Arquivos listados na seção "Arquivos Atualizados" de cada resumo |
| Detalhes de job / gig concluído | `logs/job_XXX_*.md` | `logs/sessao_resumo_*.md`, `consequencias/consequencias_persistentes.md`, `heat.md` |
| Incidente narrativo marcante (combate, confronto) | `logs/incidente_XXX_*.md` | `consequencias/consequencias_persistentes.md`, `event_queue.md`, sessões |
| Instruções do projeto (boot) | `sistema/instrucoes_projeto.md` | `diretrizes_ia.md`, este arquivo |
| Regras da IA (boot sequence) | `sistema/diretrizes_ia.md` | `instrucoes_projeto.md`, este arquivo |
| Regras do narrador | `sistema/diretrizes_narrador.md` | `sistema/diretrizes_ia.md` |
| NPCs agem / falam entre si na cena (delegação, anti-loop) | `sistema/npc_agencia_cena.md` | `diretrizes_narrador.md` §3.1, `comandos_jogador.md` § H, pulsos |
| Como atualizar após sessão | `sistema/como_atualizar_arquivos.md` | Este arquivo |
| **Tier-0 / anti-esquecimento sandbox** | `logs/context_pack_atual.md` | `sistema/fatos_duros.md`, `sistema/comandos_jogador.md` |
| Fatos que não se inventam | `sistema/fatos_duros.md` | context pack, board |
| Playbooks de comandos do jogador | `sistema/comandos_jogador.md` | instrucoes_projeto, diretrizes_ia |
| **Abrir chat novo / handoff** | `sistema/novo_chat_procedimento.md` | `logs/handoff_atual.md`, `logs/context_pack_atual.md`, último `sessao_resumo_*.md` |
| Continuidade colável (estado vigente) | `logs/handoff_atual.md` | context pack, board |
| Simular mundo off-screen (pulso diário) | `sistema/pulso_procedimento.md` | `pulso_do_mundo/pack_badlands/pulso_geral.md`, pulsos NPC |
| Log de pulso (auditoria opcional) | `logs/pulso_YYYYMMDD.md` | [pulso_log_template.md](../logs/pulso_log_template.md) |

**Padrão de resumos de sessão:** `logs/sessao_resumo_XXX.md` (ex.: `001` … `010`). Próximo número disponível: **011**.

---

## Estrutura Geral do Projeto

```text
cyberpunk/
├── README.md                      ← Visão geral e entrada do projeto
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
│   ├── medtech - stephania_stitch_voss.md
│   ├── media - emilia_echo_rivera.md
│   ├── netrunner - alex_specter_kane.md
│   ├── nomad - lena_valk_kane.md
│   ├── solo - jax_razor_kane.md
│   ├── solo - reina_bearclaw_morales.md
│   ├── techie - ryan_wireghost_voss.md
│   ├── ryan_guarda_roupas.md      ← Visual por ocasião (Badlands / NC / Wireghost)
│   ├── crew_guarda_roupas.md      ← Catálogo de roupa (ocasião; não personagem)
│   ├── vehicle - the_mule.md
│   ├── npc/                       ← Fichas mínimas (um NPC por arquivo)
│   │   ├── npc_template.md
│   │   ├── dr_elias_vossler.md
│   │   ├── lina_park.md
│   │   ├── reyes.md
│   │   ├── tio_gringo.md
│   │   ├── mara_recruit.md
│   │   ├── elias_recruit.md
│   │   ├── tomas_recruit.md
│   │   ├── sasha.md
│   │   └── lira.md
│   └── notas_narrador/
│       ├── ryan_background_completo.md
│       └── ryan_gatilhos_memorias.md
├── imagens/
│   ├── fixer - kaz_the_broker_takahashi.jpg
│   ├── medtech - stephania_stitch_voss.jpg
│   ├── netrunner - alex_specter_kane.jpg
│   ├── nomad - lena_valk_kane.jpg
│   ├── solo - jax_razor_kane.png
│   ├── solo - reina_bearclaw_morales.png
│   ├── techie - ryan_wireghost_voss.jpg              ← ficha Ryan (tático)
│   ├── techie - ryan_wireghost_voss_daily_clothes.png ← Ryan casual/oficina
│   ├── media - emilia_echo_rivera.jpg                 ← ficha Echo
│   ├── ryan/guarda_roupas/          ← catálogo Ryan (ver ryan_guarda_roupas.md)
│   ├── crew/guarda_roupas/          ← catálogo roupa por ocasião (ver crew_guarda_roupas.md)
│   ├── vehicle - the_mule.jpg
│   ├── Sasha.jpg
│   ├── Lira.jpg
│   ├── Reyes.jpg · Reyes_token.jpg  ← ficha npc/reyes.md
│   └── Tio_Gringo.jpg · Tio_Gringo_arm.jpg  ← ficha npc/tio_gringo.md
├── pulso_do_mundo/                ← Off-screen NPCs (ver pulso_procedimento.md)
│   ├── README.md
│   ├── template_pulso_npc.md
│   ├── pack_badlands/
│   │   ├── pulso_geral.md
│   │   ├── reyes.md, tio_gringo.md, sasha_e_lira.md
│   │   ├── criancas.md, recrutas.md
│   └── crew/
│       ├── valk.md, kaz.md, alex.md, reina.md
│       ├── stephania_stitch.md, jax.md
├── logs/
│   ├── pulso_log_template.md
│   ├── pulso_20260703.md
│   ├── downtime_ryan.md
│   ├── job_template.md
│   ├── job_001_extracao_vossler.md
│   ├── incidente_001_incursao_recursos_raffen.md
│   ├── incidente_002_incursao_noturna_raffen.md
│   ├── sessao_resumo_template.md
│   ├── sessao_resumo_001.md
│   ├── sessao_resumo_002.md
│   ├── sessao_resumo_003.md
│   ├── sessao_resumo_004.md
│   ├── sessao_resumo_005.md
│   ├── sessao_resumo_006.md
│   ├── sessao_resumo_007.md
│   ├── sessao_resumo_008.md
│   ├── sessao_resumo_009.md
│   ├── sessao_resumo_010.md
│   ├── context_pack_atual.md      ← Tier-0 anti-esquecimento (NOW)
│   ├── context_pack_template.md
│   ├── handoff_atual.md           ← Continuidade para chat novo
│   └── handoff_template.md
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
    ├── npc_agencia_cena.md        ← NPCs in-scene: delegação, troca NPC↔NPC, anti-loop
    ├── pulso_procedimento.md      ← Motor off-screen (1×/dia in-game)
    ├── novo_chat_procedimento.md  ← Abrir chat novo + handoff
    ├── comandos_jogador.md        ← Playbooks passo a passo
    ├── fatos_duros.md             ← F-IDs anti-alucinação
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
| `sistema/novo_chat_procedimento.md` | Ativo | Abrir chat novo + gerar handoff | `logs/handoff_atual.md`, `logs/handoff_template.md` |
| `logs/handoff_atual.md` | Ativo | Continuidade colável (vigente) | Board, último `sessao_resumo_*`, event_queue |
| `README.md` | Ativo | Visão geral e entrada do projeto | `sistema/registro_arquivos.md` |

---

## Observações Gerais

- O `registro_arquivos.md` é o **arquivo de referência central**.
- Os arquivos mais críticos para manter atualizados são:
  - `board/board_campanha.md`
  - `consequencias/consequencias_persistentes.md`
  - `relacionamentos/ryan_relacionamentos.md`
  - `sistema/dashboard_contexto.md`
  - `relacionamentos/mapa_relacional_geral.md`
- **Resumos de Sessão:** Padrão `logs/sessao_resumo_XXX.md`. Próximo número: **011**.
- **Handoff / chat novo:** Após sessão, atualizar `logs/handoff_atual.md` via [novo_chat_procedimento.md](novo_chat_procedimento.md).
- **Jobs / Gigs:** Padrão `logs/job_XXX_<slug>.md` para briefing, execução e fallout permanente. Sessões referenciam o job; não duplicar táticas completas no resumo.
- **NPCs secundários:** Um arquivo em `fichas/npc/<slug>.md` quando o personagem tem personalidade ou eventos que não cabem só no board/facção. Índice em [mapa_relacional_geral.md](../relacionamentos/mapa_relacional_geral.md). **Não** misturar vários NPCs num único arquivo (dificulta busca da IA).
- **Facções:** Detalhes em `facoes/`. Facções menores em `facoes/faccoes_geral.md`.
- **Referências cruzadas:** Cada arquivo relevante possui seção `## Referências` apontando para arquivos relacionados.
- O **Source of Truth** permanece nos arquivos locais do jogador.

---

## Referências

- [README.md](../README.md)
- [Instruções do Projeto](instrucoes_projeto.md) · [Diretrizes IA](diretrizes_ia.md) · [Diretrizes Narrador](diretrizes_narrador.md) · [Como Atualizar](como_atualizar_arquivos.md) · [Novo Chat](novo_chat_procedimento.md)
- [Dashboard de Contexto](dashboard_contexto.md) · [Board](../board/board_campanha.md)
- [Mapa Relacional Geral](../relacionamentos/mapa_relacional_geral.md)
