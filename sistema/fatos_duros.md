# Fatos Duros (anti-alucinação)

**Finalidade:** lista **estável** de fatos que a IA **não pode inventar nem inverter**.  
**Uso:** tier-0 com `logs/context_pack_atual.md`; comando `[Verificar fato]`; boot/refresh.  
**Última revisão estrutural:** 22 de Agosto de 2026 (F22 — Janus / Alex; natureza só na nota)

> Snapshot de **data/local/prioridade** vive no **context pack** (muda a cada sessão).  
> Este arquivo muda **raramente** — só quando a campanha redefinir um fato canônico.

---

## Hierarquia de verdade

1. Arquivos no repo branch **`feature/linha-estavel`** (local após sync ou **RAW**)
2. Snapshot em `logs/context_pack_atual.md` / `board/board_campanha.md`
3. Memória de chat / share Grok → **nunca** vence conflito

**RAW base:**  
`https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/`

---

## Fatos estáveis (campanha inteira)

| ID | Fato | Onde confirmar |
| -- | ---- | -------------- |
| **F01** | Branch canônica da rota normal: `feature/linha-estavel` | `instrucoes_projeto.md` |
| **F02** | Source of truth = arquivos do repo. Memória de chat **não** é canon | `diretrizes_ia.md` |
| **F03** | **Warden** = drone **terrestre** scorpion-like (modo mochila/transporte). **Não voa** | Ficha Ryan |
| **F04** | **Stitch** = Dr. Stephania Voss (MedTech da **crew**). **Doc** = Elisa “Doc” Moreau (passado de Ryan). Nunca trocar os nomes | [Stitch](../fichas/medtech%20-%20stephania_stitch_voss.md) · [Doc](../fichas/npc/elisa_doc_moreau.md) |
| **F05** | Ryan e Stephania compartilham sobrenome **Voss** por coincidência — **sem parentesco** | Ficha Stitch / ryan_relacionamentos |
| **F06** | Protagonista jogável: **Ryan “Wireghost” Voss** (Techie). Valkirya, Alex, Reina, Kaz, Stitch, **Jax “Razor” Kane**, **Emilia “Echo” Rivera** (Media) = **crew** (NC) | mapa_relacional |
| **F14** | **Scout** = sentinela/recon do Pack Badlands (apelido; scavs). **≠** Jax **“Razor” Kane** (Solo crew). Razor **não** está nas Badlands | [scout.md](../fichas/npc/scout.md) |
| **F20** | **Sparrow** = **Lina “Sparrow” Park** (contato/fixer, **pessoa**). **Steel** = **Marcus “Steel” Rivera** (contato, **pessoa**). Handles de rádio **≠** sistema/drone/protocolo. Steel **≠** Emilia “Echo” **Rivera** | [lina_park](../fichas/npc/lina_park.md) · [marcus_steel_rivera](../fichas/npc/marcus_steel_rivera.md) |
| **F07** | Ryan × Valkirya = relação **consolidada** (amor declarado); ela costuma escolher roupa em saídas | ryan / lena relacionamentos; guarda-roupa |
| **F08** | **The Mule** = veículo dela; equipe operacional **Valk + Mule** (atalho de mesa) | vehicle - the_mule; ficha |
| **F21** | Handle de rua = **Valkirya**. **Valk** = apelido **carinhoso do Ryan**. Nome civil: Lena Kane. Outros (Pack, crew, jobs, Echo) usam **Valkirya** ou Lena, não “Valk”, salvo se tiverem pego o apelido dele. **Sem retcon** de logs/diálogos já gravados | ficha nomad · este arquivo |
| **F22** | Mentor/companheiro NET de **Alex “Specter” Kane** = **Janus** (nunca “Handler”). Natureza e fragmentos = só a [nota do narrador](../fichas/notas_narrador/alex_specter_kane_background_consolidado.md). Ryan, Pack e Valkirya **não** sabem que Janus é IA. Não narrar Janus em cena do Pack. Não usar Janus como segundo PC / Interface extra. Interface dela = **6** (3 NET Actions) | ficha Alex · nota |
| **F09** | Job 001 (extração Vossler / Biotechnica) e incursões Raffen são **passados registrados** em `logs/` — não reinventar o outcome | job_001, incidentes, sessões |
| **F10** | NPCs só sabem o que viram/ouviram in-fiction (**anti meta-game**) | diretrizes_narrador |
| **F11** | Casas modulares dobráveis = projeto de Ryan; time produção + Tio Gringo sabem; **pack geral** sem anúncio oficial completo (E014: produção ok; revelação pública adiada / E012) | board / event_queue E012·E014 |
| **F17** | **Doc** = Dra. Elisa Moreau ([npc/elisa_doc_moreau.md](../fichas/npc/elisa_doc_moreau.md)); visita **E011** pendente em NC | ficha Doc · E015 checklist |
| **F12** | Vespas de combate/recon: **Hornet, Vesper, Barbed** (além do Warden) — nomes e papéis conforme ficha | ficha Ryan |
| **F16** | **Condor** + **Corujas** = drones miméticos de Ryan, **operacionais** no Pack (demo 20/07). Não confundir com Vespas. Enxame mini-drones = só ideia (21/07) | ficha Ryan · board · sessão 012 |
| **F13** | Próximo número de resumo de sessão: ver `registro_arquivos.md` (não inventar o NNN) | registro_arquivos |
| **F15** | Valkirya **não** se refere a Ryan como **“herói”** / **“herói solitário”** (promessa pós-episódio **14/07/2026** na oficina/depósito). Preocupação = outras palavras. Gatilho ativo; memória **não** desbloqueada | [ryan_gatilhos_memorias.md](../fichas/notas_narrador/ryan_gatilhos_memorias.md) · relacionamentos |
| **F18** | **Ruleset mecânico** em vigor a partir da sessão **017** (versão atual: **v1.3.0** — [versionamento_regras.md](versionamento_regras.md)). Sessões **001–016** = pré-camada (**sem retcon**). Stats Ryan: [ryan_loadout.md](../fichas/ryan_loadout.md). NET: [10_netrunning.md](regras_red/10_netrunning.md). | regras_red · loadout |
| **F19** | **Agents WIREGHOST:** **Vault** (chip **implantado**, air-gap, **corte em qualquer anomalia**, wipeout se captura; L3–L4) · **Profissional** (stick **subdermal**, ops, **dummy** se suspeita) · **Honeypot** (Agent **visível** = cobertura + isca L0; sem Pack/L3 real) · **Arbiter** + **Watchdog** (política e trajetória). Soft-canon pós-Arasaka; SoT 2026-08-08. **Arbiter ≠** drone **Warden** (**F03**). Spec: [plans/agent_security.md](../plans/agent_security.md) | agent_security · loadout |

---

## Fatos de contexto local (preencher / invalidar via board)

Estes **não** são eternos. Se o `board` disser outra região, **ignorar** a linha desatualizada e confiar no board + context pack NOW.

| ID | Enquanto válido | Fato |
| -- | --------------- | ---- |
| **L01** | Ryan hospedado no Pack Badlands | Reyes = líder; Tio Gringo = forja; acampamento = base atual |
| **L02** | Downtime Pack (pós-011) | E010 concluída 10/07; protótipo externo OK; Node em progresso |
| **L03** | Segredo casas | Time produção + Tio Gringo **sabem**; E014 produção **aprovada**; pack geral aguarda **anúncio público** (F11 / E012) |

Quando Ryan for a **Night City** ou outra região: atualizar context pack NOW; marcar L0x como N/A no pack; não carregar pulso Pack por default.

---

## Proibições rápidas (atalho)

- Não fazer Warden voar ou “flutuar como drone aéreo” como regra padrão.
- Não chamar Stephania de “Doc” nem Elisa de “Stitch”.
- Não revelar casas modulares ao pack “porque é óbvio”.
- Não usar data de chat Grok (ex. 24/06) se o **board** diz julho/2026.
- Não criar NPC/facção/local já listado em `registro_arquivos` / mapa.
- Não colocar **Jax “Razor” Kane** (crew) nas Badlands em scav/incursão — usar **Scout** ([scout.md](../fichas/npc/scout.md)).
- Não tratar Jax como vendetta anti-Militech nem como tema de cyberpsychosis. Off-screen até NC / job conjunto.
- Não narrar **Sparrow** / **Steel** como software, modo Agent ou tipo de sinal — são **NPCs** (**F20**).
- Não despejar backstory da **Echo** (acidente, Correção Editorial, Chamber, flerte) numa cena do Pack. Off-screen até reencontro NC. ≠ Steel Rivera.
- Não fazer Valkirya chamar Ryan de **“herói”** / **“herói solitário”** (bordão ou “combinado?”) — promessa 14/07; gatilho que dói (**F15**). Usar *não vai sozinho*, *planeja comigo*, *leva o time*.
- Não reabrir Valkirya no boot como briefing/CO se o pack diz residual íntimo. Acordo 019 = **perguntar** uma vez antes de vetar; idle relacional ≠ “Valk cobra o plano”.
- Não tratar **Valk** como handle de rua. Handle = **Valkirya**. **Valk** = só Ryan (carinho), salvo NPC que tenha pego o apelido (**F21**). Logs antigos **não** reescrever.
- Não chamar o mentor de Alex de **Handler**. Não revelar que **Janus** é IA em cena do Pack. Não rolar Janus no lugar dela (**F22**).
- Não re-rolar nem “corrigir” outcomes das sessões **001–016** com a camada mecânica (**F18**). Ver [auditoria_combates_canonicos.md](../plans/auditoria_combates_canonicos.md) (só observação).
- Sob risco/oposição (sessão **017+**): não narrar sucesso automático; usar [regras_red](regras_red/00_integridade_regras.md) · atalho [11_referencia](regras_red/11_referencia.md).
- Não confundir **Arbiter** / **Watchdog** (Agents) com **Warden** drone (**F03** / **F19**).
- Não colocar dados reais do Pack / L3–L4 no Honeypot; Vault **sem** rede em idle; **anomalia no Vault = corte** (sem “duelo NET” no cofre).
- Sync Vault: **não** direto do Profissional; terceira interface (Neural one-shot) após validação — ver spec.

---

## Referências

- [Context pack atual](../logs/context_pack_atual.md) · [Comandos do jogador](comandos_jogador.md)
- [Instruções](instrucoes_projeto.md) · [Diretrizes IA](diretrizes_ia.md) · [Board](../board/board_campanha.md)
- [Regras RED](regras_red/00_integridade_regras.md) · [House rules](house_rules/regras_campanha.md) · [Versionamento](versionamento_regras.md)
