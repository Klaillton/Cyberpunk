# Fatos Duros (anti-alucinação)

**Finalidade:** lista **estável** de fatos que a IA **não pode inventar nem inverter**.  
**Uso:** tier-0 com `logs/context_pack_atual.md`; comando `[Verificar fato]`; boot/refresh.  
**Última revisão estrutural:** 15 de Julho de 2026 (F14 — Scout ≠ Razor)

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
| **F04** | **Stitch** = Dr. Stephania Voss (MedTech da **crew**). **Doc** = Elisa “Doc” Moreau (passado de Ryan). Nunca trocar os nomes | Ficha Stitch; ficha Ryan § Contatos |
| **F05** | Ryan e Stephania compartilham sobrenome **Voss** por coincidência — **sem parentesco** | Ficha Stitch / ryan_relacionamentos |
| **F06** | Protagonista jogável: **Ryan “Wireghost” Voss** (Techie). Valk, Alex, Reina, Kaz, Stitch, **Jax “Razor” Kane** = **crew** (NC) | mapa_relacional |
| **F14** | **Scout** = sentinela/recon do Pack Badlands (apelido; scavs). **≠** Jax **“Razor” Kane** (Solo crew). Razor **não** está nas Badlands | [scout.md](../fichas/npc/scout.md) |
| **F07** | Ryan × Valk = relação **consolidada** (amor declarado); Valk costuma escolher roupa em saídas | ryan / lena relacionamentos; guarda-roupa |
| **F08** | **The Mule** = veículo de Valk; equipe operacional **Valk + Mule** | vehicle - the_mule; ficha Valk |
| **F09** | Job 001 (extração Vossler / Biotechnica) e incursões Raffen são **passados registrados** em `logs/` — não reinventar o outcome | job_001, incidentes, sessões |
| **F10** | NPCs só sabem o que viram/ouviram in-fiction (**anti meta-game**) | diretrizes_narrador |
| **F11** | Casas modulares dobráveis = projeto de Ryan; **segredo** até protótipo / revelação consciente | board / event_queue E012 |
| **F12** | Vespas de combate/recon: **Hornet, Vesper, Barbed** (além do Warden) — nomes e papéis conforme ficha | ficha Ryan |
| **F13** | Próximo número de resumo de sessão: ver `registro_arquivos.md` (não inventar o NNN) | registro_arquivos |

---

## Fatos de contexto local (preencher / invalidar via board)

Estes **não** são eternos. Se o `board` disser outra região, **ignorar** a linha desatualizada e confiar no board + context pack NOW.

| ID | Enquanto válido | Fato |
| -- | --------------- | ---- |
| **L01** | Ryan hospedado no Pack Badlands | Reyes = líder; Tio Gringo = forja; acampamento = base atual |
| **L02** | Downtime Pack (pós-011) | E010 concluída 10/07; protótipo externo OK; Node em progresso |
| **L03** | Segredo casas | Time produção + Tio Gringo **sabem**; pack geral aguarda Reyes (F11 parcial) |

Quando Ryan for a **Night City** ou outra região: atualizar context pack NOW; marcar L0x como N/A no pack; não carregar pulso Pack por default.

---

## Proibições rápidas (atalho)

- Não fazer Warden voar ou “flutuar como drone aéreo” como regra padrão.
- Não chamar Stephania de “Doc” nem Elisa de “Stitch”.
- Não revelar casas modulares ao pack “porque é óbvio”.
- Não usar data de chat Grok (ex. 24/06) se o **board** diz julho/2026.
- Não criar NPC/facção/local já listado em `registro_arquivos` / mapa.
- Não colocar **Jax “Razor” Kane** (crew) nas Badlands em scav/incursão — usar **Scout** ([scout.md](../fichas/npc/scout.md)).

---

## Referências

- [Context pack atual](../logs/context_pack_atual.md) · [Comandos do jogador](comandos_jogador.md)
- [Instruções](instrucoes_projeto.md) · [Diretrizes IA](diretrizes_ia.md) · [Board](../board/board_campanha.md)
