# Handoff atual — Continuidade para novo chat
**Gerado no corte:** sessão **024 em andamento** (ctrl ~70/90 · almoço)  
**Próximo resumo (quando finalizar):** **024** → `logs/sessao_resumo_024.md`  
**Data in-game ao cortar:** ~02 de Agosto de 2026 · almoço · Condor no ar  
**Branch canônica:** `feature/linha-estavel`  
**Última atualização deste handoff:** 31 de Agosto de 2026

> **Primeiro arquivo a ler:** `logs/context_pack_atual.md`  
> **Arco L1 + off-screen:** `board/arco_ativo.md`  
> **Voz Valkirya:** `board/arco_ativo.md` §7 + `sistema/diretrizes_narrador.md` §3.3  
> **Prosa downtime:** `sistema/motor_cena_1pager.md` + diretrizes §5.1  
> **Canon:** repo/RAW > handoff > memória de chat

**Cortar este chat.** Ctrl 70. Almoço é quebra limpa. O motor novo **não pega** num thread que já aprendeu o esqueleto magro. Não dar `[Refresh]` aqui — abrir chat **novo**.

---

## Prosa (ler no boot)

O SoT estava matando atmosfera: spec de personagem + ficha-index + MOTOR de 4 linhas. Anti-eco e anti-estagnação **continuam**. Downtime **pode ter carne**.

| Modo | Faça | Não faça |
| ---- | ---- | -------- |
| **DOWNTIME / relacional** | 3–6 linhas de corpo (calor, cheiro, poeira, ombro) + fala SHOW | Eco da caminhada; caderno; “três coisas” |
| **OPERAÇÃO / recon** | Resultado primeiro | Engordar SOP |

O beat do ctrl 70 (Valk no ombro da Sasha, oficina, pássaro no ar) está **certo em conteúdo**. No chat novo, o **almoço** pode ter cheiro e mesa sem virar briefing.

Valk: residual quente. Fala curta **e** quente. Não CO.

---

## Boot (ordem de leitura)

1. `logs/context_pack_atual.md` (NOW + MOTOR downtime + Voz Valk)  
2. Este handoff (prosa + corte)  
3. `sistema/fatos_duros.md` se dúvida  
4. `board/arco_ativo.md` §7 se Valk em cena  

**Confirmação (1 linha):**
```
Boot OK · ~02/08/2026 almoço · Pack · Condor no ar · Valk = residual quente · prosa downtime on · próximo resumo: 024 · Ruleset 1.3.0
```

---

## Estado atual (snapshot)

| Campo | Valor |
| ----- | ----- |
| Data | **~02/08/2026**, almoço |
| Local | Pack: Ryan **oficina**; Valk + Sasha + Lira **gancho Condor** |
| Condor | **No ar** (ponto no corredor); **sem pacote** ainda |
| Intermediário | Teto **à tarde** (ainda aberto) |
| Ryan × Valk | Residual íntimo alto; ela ficou com as duas (*“Eu fico. Ele está na oficina.”*) |
| Oficina (último beat) | Tio no ferro; Vespas limpas (Barbed no limite, Hornet com pedra — alinhado); Warden ok; HMG cinta no Mule; DMR limpa; estojo no trilho do hatch |
| Base militar | **Não entra agora**; gatilho = mensagem → manhã seguinte |
| 024 | **Não finalizada** — este corte continua a mesma sessão |
| Ruleset | **v1.3.0** |

### Cena de abertura
**Pack — almoço ~02/08.**  
Oficina vista. Almoço no ar. Condor voando. Valk no gancho. Ryan pode ir comer — prosa ok, sem eco do checklist.

### AGENDA
1. Almoço / downtime.  
2. Condor pousar / pacote.  
3. Teto do intermediário à tarde.

### Trava
- Não reabrir Condor/base/jantar 023 como briga.  
- 019 = **perguntar** uma vez, não cobrar.  
- Não herdar o registro magro do chat em ctrl 70 (listas, “Sem eco da caminhada” como estilo único).

---

## Prompt de abertura (copiar no novo chat)

```markdown
# Cyberpunk RED — Continuidade (Sessão 024, continua)

## Boot (tier-0)
- Repo: https://github.com/Klaillton/Cyberpunk · branch `feature/linha-estavel`
- Canon = arquivos do repo após sync / RAW
- **Chat anterior (ctrl 70) — não continuar.** Motor de prosa downtime atualizado neste RAW.
- Leia primeiro: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/context_pack_atual.md
- Handoff: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/handoff_atual.md
- Motor: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/sistema/motor_cena_1pager.md
- Voz Valk: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/board/arco_ativo.md

## Mecânica
- Ruleset **1.3.0** (F18); loadout sob demanda; sem inventar mods

## Estado
- **~02/08/2026 almoço** · Pack Badlands
- Ryan na oficina (Tio; Vespas/Warden/armas recém-vistos). Valk com Sasha/Lira no gancho.
- Condor **no ar**, sem pacote. Almoço no ar. Teto do intermediário **à tarde**.
- Ryan × Valk: residual quente; ela ficou (*“Eu fico. Ele está na oficina. Qualquer burst, a gente chama.”*)

## Trava
- Não reabrir Condor/base nem o jantar 023
- 024 **não** foi finalizada — esta é a mesma sessão até `[Finalizar]`

## Valk (voz)
- Curta **e** quente. Dengosa discreta. Não CO, não caderno.

## Prosa (obrigatório neste boot)
- DOWNTIME: 3–6 linhas de corpo (calor, cheiro, poeira, ombro) + fala. Anti-eco ≠ prosa zero.
- OPERAÇÃO/recon: resultado primeiro (não engordar).
- O almoço pode ter mesa e cheiro. Não listar ferro de novo se o PC já viu.

## Cena
Pack. Almoço no ar. Condor voando. Ryan pode ir comer.

## Narração
- N1–N11 com prosa de downtime (§5.1)
- Confirme boot em **1 linha** (inclua “Valk = residual quente” e “prosa downtime on”), imprima `ctrl 2/90`, e **aguarde o jogador**.
```
