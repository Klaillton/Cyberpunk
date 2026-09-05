# Registro de Arquivos do Projeto - Cyberpunk RED

**Última atualização:** 2026-08-31 (sessão 024 gravada; próximo resumo **025**)

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
| Vazamento Media (Echo) / Void List | `sistema/echo_exposicao.md` | `heat.md`, `reputacao.md`, ficha Echo · kit caveira/espartana **§7.1** |
| Eventos pendentes no mundo | `event_queue.md` | `board/board_campanha.md`, `board/arco_ativo.md`, `consequencias/consequencias_persistentes.md` |
| Arco em foco (L1) + NPCs off-screen | `board/arco_ativo.md` | `logs/context_pack_atual.md` (AGENDA), `event_queue.md` |
| Ambientação / ganchos / imagem opcional | `sistema/cena_ambientacao_ganchos.md` | `motor_cena_1pager.md`, `arco_ativo.md` §7 |
| Soft-canon / refinamentos futuros (não tier-0) | `ideas_concepts/README.md` | polycule, gatilhos, Moreau — **não** boot |
| Situação financeira | `economia.md` | `board/board_campanha.md`, `logs/downtime_ryan.md` |
| Relações do protagonista | `relacionamentos/ryan_relacionamentos.md` | `relacionamentos/mapa_relacional_geral.md`, `relacionamentos/crew_relacionamentos.md` |
| Relação Valk | `relacionamentos/lena_valk_kane_relacionamentos.md` | `ryan_relacionamentos.md` |
| Dinâmica entre membros da crew | `relacionamentos/crew_relacionamentos.md` | `relacionamentos/mapa_relacional_geral.md` |
| Arco romântico futuro (polycule) | `relacionamentos/crew_polycule_ryan_valk_alex_reina.md` | `relacionamentos/crew_relacionamentos.md`, arquivos individuais |
| Relações com facções | `relacionamentos/faccao_relacionamentos.md` | `facoes/pack_badlands.md`, `facoes/faccoes_geral.md`, `reputacao.md` |
| Hub de personagens (onde achar cada NPC) | `relacionamentos/mapa_relacional_geral.md` | `fichas/`, `relacionamentos/*_relacionamentos.md` |
| Ficha mecânica de personagem (crew) | `fichas/<personagem>.md` | Relacionamento correspondente em `relacionamentos/` |
| NPC secundário (personalidade + eventos) | `fichas/npc/<slug>.md` | [mapa_relacional_geral.md](../relacionamentos/mapa_relacional_geral.md), facção/job/sessão |
| **Sparrow** (Lina Park) | `fichas/npc/lina_park.md` | E015 · residual sem ACK (019) |
| **Steel** (Marcus Rivera) | `fichas/npc/marcus_steel_rivera.md` | E015 · mudo (019) · ≠ Echo Rivera |
| Detalhes de facção ativa | `facoes/pack_badlands.md` | `relacionamentos/faccao_relacionamentos.md`, `reputacao.md` |
| Facções menores / superficiais | `facoes/faccoes_geral.md` | `relacionamentos/faccao_relacionamentos.md` |
| Atividades de downtime do Ryan | `logs/downtime_ryan.md` | `board/board_campanha.md`, `fichas/techie - ryan_wireghost_voss.md` |
| **Guarda-roupa / visual por ocasião (Ryan)** | `fichas/ryan_guarda_roupas.md` | `imagens/ryan/guarda_roupas/`, ficha techie |
| **Guarda-roupa / peças por ocasião (feminino)** | `fichas/crew_guarda_roupas.md` | `imagens/crew/guarda_roupas/` — foco em **roupa**, não personagem da foto |
| **Quem está vestindo o quê agora** | `fichas/notas_narrador/crew_vestindo_agora.md` | `roupa_por_ocasiao.md`, context pack NOW |
| **Projeto futuro armadura Reina (não canônico)** | `fichas/reina_armour_project.md` | Ficha Reina; `imagens/reina/reina_armour_1.jpg` · `_2.jpg` · `reina_bursts.jpg` — **só após ATIVO** |
| **Projeto futuro moto Reina (não canônico)** | `fichas/reina_byke_project.md` | Ficha Reina; `imagens/reina/bike9.jpg` — **só após ATIVO** |
| Background e gatilhos do Ryan (narrador) | `fichas/notas_narrador/ryan_background_completo.md` | `fichas/notas_narrador/ryan_gatilhos_memorias.md`, `fichas/techie - ryan_wireghost_voss.md` (Elisa "Doc" Moreau) |
| Curiosidade: valor agregado ao Pack (estimativa) | `fichas/notas_narrador/ryan_valor_pack.md` | **Não** é ledger; Ryan não sabe; [economia.md](../economia.md) |
| Background Valkirya (narrador) | `fichas/notas_narrador/lena_valkyria_kane_background.md` | Backstory ≠ mesa; upgrades Mule = campanha |
| Background Alex (narrador) | `fichas/notas_narrador/alex_specter_kane_background_consolidado.md` | Janus **F22**; backstory ≠ mesa; `backstory.md` = ponte |
| Background Reina (narrador) | `fichas/notas_narrador/reina_bearclaw_morales_background.md` | Braços / Doc / Stitch; backstory ≠ mesa; reencontro parked |
| Background Echo (narrador) | `fichas/notas_narrador/emilia_echo_rivera_background.md` | Backstory ≠ mesa; Void List; ≠ Steel Rivera (F20) |
| Background Jax (narrador) | `fichas/notas_narrador/jax_razor_kane_background.md` | Combate ≠ guerra; placar; Militech = carreira ≠ vendetta; ≠ mesa; off-screen NC |
| Background Leopold (narrador) | `fichas/notas_narrador/leopold_habsbruck_background.md` | Prometheus; chama de três linhas; teia Habsbrück / avó / Kaz / Zoners = nota; ≠ Echo; **F23**; off-screen NC |
| Ficha Leopold (Rockerboy) | `fichas/rockerboy - leopold_habsbruck.md` | CI **6** · 62 stats · 100 skills · fashionware; rel [leopold_habsbruck_relacionamentos.md](../relacionamentos/leopold_habsbruck_relacionamentos.md); pulso `pulso_do_mundo/crew/leopold.md`; chama `imagens/leopold/prometheus_flame.jpg` |
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
| Versão do ruleset | `sistema/versionamento_regras.md` | `Ruleset: 1.3.0` no resumo |
| Planos de trabalho (sistema) | `plans/README.md` | `plans/add-cyberpunk-red-mechanics.md` |
| Auditoria combates pré-017 (só leitura) | `plans/auditoria_combates_canonicos.md` | F18 — **não** retcon |
| Agents OPSEC Ryan (Vault/Honeypot/…) | `plans/agent_security.md` | F19 · `ryan_loadout` · ≠ Warden drone |

**Padrão de resumos de sessão:** `logs/sessao_resumo_XXX.md` (ex.: `001` … `024`). Próximo número disponível: **025**.

---

## Estrutura Geral do Projeto

O índice de árvore e o restante deste arquivo permanecem como na SoT 30/08 (Jax + Echo indexados). **2026-09-05:** Leopold / **Prometheus** — ficha RED (CI 6, 62/100, fashionware); chama em `imagens/leopold/`. Próximo resumo: **025**.

---

## Observações Gerais

- O `registro_arquivos.md` é o **arquivo de referência central**.
- **Resumos de Sessão:** Padrão `logs/sessao_resumo_XXX.md`. Próximo número: **025**.
- **Ruleset:** v1.3.0 em `sistema/regras_red/` (sessão 017+; F18).
- O **Source of Truth** permanece nos arquivos do repo (`feature/linha-estavel`).
