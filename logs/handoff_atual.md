# Handoff atual — Continuidade para novo chat
**Gerado após:** sessão **019**  
**Próxima sessão:** **020** → `logs/sessao_resumo_020.md`  
**Data in-game ao fechar:** ~27 de Julho de 2026 · noite  
**Branch canônica:** `feature/linha-estavel`  
**Última atualização deste handoff:** 14 de Agosto de 2026

> **Primeiro arquivo a ler:** `logs/context_pack_atual.md`  
> **Arco L1 + off-screen:** `board/arco_ativo.md`  
> **Ambiente / ganchos:** `sistema/cena_ambientacao_ganchos.md`  
> **Canon:** repo/RAW > handoff > memória de chat  

---

## Links rápidos

| Recurso | URL |
| ------- | --- |
| Context pack (RAW) | https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/context_pack_atual.md |
| Sessão 019 (RAW) | https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/sessao_resumo_019.md |
| Handoff (RAW) | https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/handoff_atual.md |
| Arco ativo | https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/board/arco_ativo.md |
| Board | https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/board/board_campanha.md |
| Ambientação | https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/sistema/cena_ambientacao_ganchos.md |
| Procedimento novo chat | https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/sistema/novo_chat_procedimento.md |

---

## Boot (ordem de leitura)

1. `logs/context_pack_atual.md`  
2. `sistema/fatos_duros.md` (dúvida de fato)  
3. Este handoff  
4. `board/arco_ativo.md` se E015/canal/estagnação  
5. Board se divergir  

**Confirmação (1 linha):**
```
Boot OK · ~27/07/2026 noite · Pack Badlands · prioridade: ad (~3d) + residual Sparrow + downtime · próximo resumo: 020 · Ruleset 1.3.0
```

---

## Estado atual (snapshot)

| Campo | Valor |
| ----- | ----- |
| Data | **~27/07/2026**, noite |
| Local | Pack Badlands (tenda Ryan/Valk) |
| Pessoas | Ryan + Valk (Pack); Lira + Sasha no Pack com residual positivo |
| Drones | Vespas + Warden com Ryan; Condor/Corujas no Pack |
| Canais | **Lina Park (Sparrow):** residual sem ACK (silêncio deliberado); **Marcus Rivera (Steel):** mudo; Kaz off-screen montando crew |
| Ryan × Valk | **Acordo 019:** ele dá mínimo de plano antes do operador; ela pergunta antes de subir o tom. Intimidade reforçada. |
| Sasha | Residual positivo 019; “não some sem avisar” mantido |
| Lira | Residual positivo 019; aberta a novas saídas |
| Plano | Ad anônimo no ar (100 ed/dia; pacote a cada 3 dias); aguardar respostas |
| Ruleset | **v1.3.0** |

### Cena de abertura
**Pack — noite / manhã seguinte.**  
Downtime. Ad no ar. Residual Sparrow ainda sem ACK. Acordo Valk em vigor.  
Gancho: o que Ryan faz?

### AGENDA
1. Relógio do ad (~3 dias).  
2. Residual Lina Park / rede NC.  
3. Pack rotina / E019 olaria / residual Sasha-Lira.

---

## O que acabou de acontecer (019)
- Industrial: pesquisa BT (exposição baixa) + padrões Sparrow/Steel (OPSEC alta).  
- Ad anônimo no ar com fragmento Kaz.  
- Retorno Pack; conversa explícita ops solo → **acordo de comunicação**.  
- Residual positivo Sasha/Lira. Thread relacional reforçado com Valk.

Detalhe: [sessao_resumo_019.md](sessao_resumo_019.md)

---

## Pendências quentes

| ID | Evento |
| -- | ------ |
| **E015** | Ad ativo; residual Sparrow; Steel mudo; Kaz off |
| Ad | Primeiro pacote ~3 dias |
| E011 | Doc Moreau c/ Valk |
| E019 | Olaria Pack |
| E012 / E007 / E008 | Background |

---

## Regras duras (boot)

| ID | Regra |
| -- | ------ |
| F03 | Warden **não voa** |
| F04 | Stitch ≠ Doc Moreau |
| F15 | Valk **não** “herói” |
| F18 | Ruleset **1.3.0**; sem retcon 001–016 |
| F19 | Agents ≠ Warden |
| F20 | Sparrow = Lina Park (NPC); Steel = Marcus Rivera (NPC) |
| Motor | N1–N11: sem eco; delta ≥60%; AMBIENTE em local novo; SHOW relacional |

---

## Prompt de abertura (copiar no novo chat)

```markdown
# Cyberpunk RED — Continuidade (Sessão 020)

## Boot (tier-0)
- Repo: https://github.com/Klaillton/Cyberpunk · branch `feature/linha-estavel`
- Canon = arquivos do repo após sync / RAW
- Leia primeiro: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/context_pack_atual.md
- Resumo 019: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/sessao_resumo_019.md
- Handoff: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/handoff_atual.md
- Arco L1: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/board/arco_ativo.md
- Ambientação: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/sistema/cena_ambientacao_ganchos.md
- Procedimento: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/sistema/novo_chat_procedimento.md

## Mecânica
- Ruleset **1.3.0** (F18); loadout sob demanda; sem inventar mods

## Estado
- **~27/07/2026 noite** · Pack Badlands
- Ryan + Valk (acordo comunicação ops 019 fechado)
- Ad anônimo no ar (pacote ~3 dias); residual **Lina Park** sem ACK; **Marcus Rivera** mudo
- Sasha/Lira: residual positivo da viagem 019
- Plano: downtime Pack / aguardar ad / eventual E019

## Cena
Pack. Downtime. **SHOW** residual se NPCs falarem. Gancho: o que Ryan faz?

## Narração
- N1–N11 · delta ≥60% · sem eco de mood/abraço
- Confirme boot em **1 linha** e aguarde o jogador.
```
