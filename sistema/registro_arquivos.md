# Registro de Arquivos do Projeto - Cyberpunk RED

**Última atualização:** 2026-08-09 (curadoria sessão 017; Ruleset v1.3.0; próximo resumo **018**)

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
| Vazamento Media (Echo) / Void List | `sistema/echo_exposicao.md` | `heat.md`, `reputacao.md`, ficha Echo |
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
| **Projeto futuro armadura Reina (não canônico)** | `fichas/reina_armour_project.md` | Ficha Reina; `imagens/reina/reina_armour_1.jpg` · `_2.jpg` · `reina_bursts.jpg` — **só após ATIVO** |
| Background e gatilhos do Ryan (narrador) | `fichas/notas_narrador/ryan_background_completo.md` | `fichas/notas_narrador/ryan_gatilhos_memorias.md`, `fichas/techie - ryan_wireghost_voss.md` (Elisa "Doc" Moreau) |
| Histórico de sessão | `logs/sessao_resumo_XXX.md` | Arquivos listados na seção "Arquivos Atualizados" de cada resumo |
| Detalhes de job / gig concluído | `logs/job_XXX_*.md` | `logs/sessao_resumo_*.md`, `consequencias/consequencias_persistentes.md`, `heat.md` |
| Incidente narrativo marcante (combate, confronto) | `logs/incidente_XXX_*.md` | `consequencias/consequencias_persistentes.md`, `event_queue.md`, sessões |
| Instruções do projeto (boot) | `sistema/instrucoes_projeto.md` | `diretrizes_ia.md`, este arquivo |
| Regras da IA (boot sequence) | `sistema/diretrizes_ia.md` | `instrucoes_projeto.md`, este arquivo |
| Regras do narrador | `sistema/diretrizes_narrador.md` | `sistema/diretrizes_ia.md`, **§7.1 Motor de cena** |
| Motor de cena (1 página anti-eco) | `sistema/motor_cena_1pager.md` | context pack bloco MOTOR, `comandos_jogador.md` § J |
| NPCs agem / falam entre si na cena (delegação, anti-loop) | `sistema/npc_agencia_cena.md` | `diretrizes_narrador.md` §3.1/§7.1, `comandos_jogador.md` § H |
| Como atualizar após sessão | `sistema/como_atualizar_arquivos.md` | Este arquivo |
| **Tier-0 / anti-esquecimento sandbox** | `logs/context_pack_atual.md` | `fatos_duros.md`, `comandos_jogador.md`, bloco **MOTOR** + **AGENDA** |
| Fatos que não se inventam | `sistema/fatos_duros.md` | context pack, board |
| Playbooks de comandos do jogador | `sistema/comandos_jogador.md` | instrucoes_projeto, diretrizes_ia |
| Micro-recursos / estoque / produtores | `economia.md` § Atores · Estoque · Ryan mínimo | `[Estoque]` playbook K; pack_badlands (só link) |
| **Abrir chat novo / handoff** | `sistema/novo_chat_procedimento.md` | `logs/handoff_atual.md`, `logs/context_pack_atual.md`, último `sessao_resumo_*.md` |
| Continuidade colável (estado vigente) | `logs/handoff_atual.md` | context pack, board |
| Simular mundo off-screen (pulso diário) | `sistema/pulso_procedimento.md` | `pulso_do_mundo/pack_badlands/pulso_geral.md`, pulsos NPC |
| Log de pulso (auditoria opcional) | `logs/pulso_YYYYMMDD.md` | [pulso_log_template.md](../logs/pulso_log_template.md) |
| **Regras RED (mecânica / testes)** | `sistema/regras_red/11_referencia.md` (atalho) | `00`–`10` full · Ruleset **1.3.0** · **não** tier-0 |
| Netrunning / Interface | `sistema/regras_red/10_netrunning.md` | ficha Alex, `07_roles` |
| Combate / ROF / stealth attack | `sistema/regras_red/02_combate.md` | `04_armas`, `03_ferimentos`, house |
| Armas (categorias) | `sistema/regras_red/04_armas.md` | **dano/ROF no loadout** |
| Cyberware / HL | `sistema/regras_red/05_cyberware.md` | ficha personagem |
| Skills (mapa STAT) | `sistema/regras_red/06_skills.md` | ficha |
| Role Abilities (crew) | `sistema/regras_red/07_roles.md` | fichas crew |
| Maker / craft / drones (regras) | `sistema/regras_red/08_techie.md` | ficha Ryan, `ryan_loadout`, economia |
| Veículos / perseguição / Mule (regras) | `sistema/regras_red/09_veiculos.md` | ficha Mule, Valk |
| **Loadout tático Ryan (dano/ROF/WA)** | `fichas/ryan_loadout.md` | SoT stats armas/drones |
| HP / SP / Death Save | `sistema/regras_red/03_ferimentos.md` | ficha do personagem, Finalizar |
| House rules (stealth, drones, oficina) | `sistema/house_rules/regras_campanha.md` | `regras_red/00`, F03/F12/F16/F18 |
| Versão do ruleset | `sistema/versionamento_regras.md` | `Ruleset: 1.1.0` no resumo |
| Planos de trabalho (sistema) | `plans/README.md` | `plans/add-cyberpunk-red-mechanics.md` |
| Auditoria combates pré-017 (só leitura) | `plans/auditoria_combates_canonicos.md` | F18 — **não** retcon |
| Agents OPSEC Ryan (Vault/Honeypot/…) | `plans/agent_security.md` | F19 · `ryan_loadout` · ≠ Warden drone |

**Padrão de resumos de sessão:** `logs/sessao_resumo_XXX.md` (ex.: `001` … `017`). Próximo número disponível: **018**.

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
│   ├── ryan_loadout.md            ← Armas / drones / SP (SoT tático)
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
│   │   ├── lira.md
│   │   ├── scout.md
│   │   ├── rusty.md
│   │   └── elisa_doc_moreau.md  ← Doc Moreau (≠ Stitch); E011
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
│   ├── lina_park.jpg              ← ficha npc/lina_park.md
│   ├── elisa_doc_moreau.jpg       ← ficha npc/elisa_doc_moreau.md (Doc ≠ Stitch)
│   ├── Reyes.jpg · Reyes_token.jpg  ← ficha npc/reyes.md
│   └── Tio_Gringo.jpg · Tio_Gringo_arm.jpg  ← ficha npc/tio_gringo.md
├── pulso_do_mundo/                ← Off-screen NPCs (ver pulso_procedimento.md)
│   ├── README.md
│   ├── template_pulso_npc.md
│   ├── pack_badlands/
│   │   ├── pulso_geral.md
│   │   ├── reyes.md, tio_gringo.md, sasha_e_lira.md, scout.md
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
│   ├── sessao_resumo_011.md
│   ├── sessao_resumo_012.md
│   ├── sessao_resumo_013.md
│   ├── sessao_resumo_014.md
│   ├── sessao_resumo_015.md
│   ├── sessao_resumo_016.md
│   ├── sessao_resumo_017.md
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
├── plans/                         ← Planos de trabalho (não estado de campanha)
│   ├── README.md
│   └── add-cyberpunk-red-mechanics.md
└── sistema/
    ├── instrucoes_projeto.md      ← Instruções do projeto (espelho versionado)
    ├── npc_agencia_cena.md        ← NPCs in-scene: delegação, troca NPC↔NPC, anti-loop
    ├── motor_cena_1pager.md       ← Anti-eco / resultado-primeiro (mid-chat)
    ├── pulso_procedimento.md      ← Motor off-screen (1×/dia in-game)
    ├── novo_chat_procedimento.md  ← Abrir chat novo + handoff
    ├── comandos_jogador.md        ← Playbooks passo a passo
    ├── fatos_duros.md             ← F-IDs anti-alucinação
    ├── como_atualizar_arquivos.md
    ├── dashboard_contexto.md
    ├── diretrizes_ia.md
    ├── diretrizes_narrador.md
    ├── versionamento_regras.md    ← Ruleset semver
    ├── regras_red/                ← Mecânica RED (resumo operacional)
    │   ├── 00_integridade_regras.md
    │   ├── 01_core.md
    │   ├── 02_combate.md
    │   ├── 03_ferimentos.md
    │   ├── 04_armas.md
    │   ├── 05_cyberware.md
    │   ├── 06_skills.md
    │   ├── 07_roles.md
    │   ├── 08_techie.md
    │   ├── 09_veiculos.md
    │   ├── 10_netrunning.md
    │   └── 11_referencia.md
    ├── house_rules/
    │   ├── README.md
    │   └── regras_campanha.md     ← Stealth, drones
    └── registro_arquivos.md       ← Este arquivo
```

---

## Arquivos de Estado do Mundo

| Arquivo | Status | Finalidade | Consultar junto com |
| ------- | ------ | ---------- | ------------------- |
| `board/board_campanha.md` | Ativo | Estado narrativo atual | `dashboard_contexto.md`, `consequencias/consequencias_persistentes.md` |
| `reputacao.md` | Ativo | Reputação por facção e NPC | `relacionamentos/faccao_relacionamentos.md`, `facoes/` |
| `heat.md` | Ativo | Nível de exposição/perseguição | `event_queue.md`, `consequencias/consequencias_persistentes.md`, `sistema/echo_exposicao.md` |
| `sistema/echo_exposicao.md` | Ativo | Void List / Null / níveis de vazamento Echo | `heat.md`, `reputacao.md`, ficha Echo |
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
- **Resumos de Sessão:** Padrão `logs/sessao_resumo_XXX.md`. Próximo número: **018**.
- **Ruleset:** v1.3.0 em `sistema/regras_red/` (sessão 017+; F18).
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
