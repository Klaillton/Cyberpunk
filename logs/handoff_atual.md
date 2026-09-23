# Handoff atual — Continuidade para novo chat
**Gerado após:** sessão **027**  
**Próxima sessão:** **028** → `logs/sessao_resumo_028.md`  
**Data in-game ao fechar:** ~04 de Agosto de 2026 · manhã · Mule → Pack  
**Branch canônica:** `feature/linha-estavel`  
**Última atualização deste handoff:** 23 de Setembro de 2026

> **Primeiro arquivo a ler:** `logs/context_pack_atual.md`  
> **Canon:** repo/RAW > handoff > memória de chat

**Não continuar o chat da 027.** Chat novo = 028.

---

## Boot (ordem de leitura)

1. `logs/context_pack_atual.md`  
2. Este handoff  
3. `sistema/fatos_duros.md` se dúvida  
4. `board/arco_ativo.md` se E015 / Cutter / estagnação  

**Confirmação (1 linha):**
```
Boot OK · ~04/08/2026 manhã · Pack · Mule volta · Valk = residual (ops→tenda quente) · prosa downtime on · chip lacre intacto · hop NC 05/08 21h · corte 027 feito · próximo resumo: 028 · Ruleset 1.3.0
```

---

## Estado atual (snapshot)

| Campo | Valor |
| ----- | ----- |
| Data | **~04/08/2026**, manhã |
| Local | Mule no rasto de volta ao Pack |
| Chip E015 | **Lacre intacto**; hop NC **05/08 após 21h** |
| Cutter | Corte 04/08 **feito** (recon, sem tiro). 7 quentes; lona = fogueira morta. Debrief pendente. |
| Condor | Unmanned; pousou 03/08; Sasha/Lira no gancho/visor |
| Ryan × Valk | 019 + residual alto; ela no volante no corte |
| Reyes | No Mule; debrief depois de dormir |
| Base militar | **Não entra agora** |
| Ruleset | **v1.3.0** |

### Cena de abertura (028)

Pack manhã. Volta do corte. Dormir. Debrief. Chip **fechado**. Não reabrir jantar 023 / SOP Condor / caixa 101 / canyon.

### AGENDA

1. Dormir / debrief Reyes.  
2. Abrir o chip.  
3. Hop NC 05/08 após 21h.

### Trava

- Não reabrir Condor SOP / jantar 023 / base agora / caixa 101 / canyon do corte.  
- 019 = perguntar uma vez. F15 sem “herói”. F21 Valkirya / Valk.  
- F16 Condor unmanned.  
- Ryan pode cortar; NPC **não** copia o corte.

---

## Prompt de abertura (copiar no novo chat)

```markdown
# Cyberpunk RED — Continuidade (Sessão 028)

## Boot (tier-0)
- Repo: https://github.com/Klaillton/Cyberpunk · branch `feature/linha-estavel`
- Canon = arquivos do repo após sync / RAW
- **Não continuar o chat da 027.**
- Leia primeiro: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/context_pack_atual.md
- Resumo 027: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/sessao_resumo_027.md
- Handoff: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/handoff_atual.md
- Motor: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/sistema/motor_cena_1pager.md
- Voz Valk: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/board/arco_ativo.md

## Mecânica
- Ruleset **1.3.0** (F18); loadout sob demanda; sem inventar mods

## Estado
- **~04/08/2026 manhã** · Pack · Mule volta do corte
- Chip E015 **lacre intacto**; hop NC **05/08 após 21h**
- Corte Cutter 027 feito (recon, sem tiro; 7 quentes; lona morta). Debrief pendente.
- Condor unmanned (F16)

## Trava
- Não reabrir jantar 023 nem SOP Condor nem a caixa da 101 nem o canyon
- 019 = ela pergunta uma vez antes de vetar
- F15: sem “herói” · F21: Valkirya / Valk · F16: Condor unmanned
- NPCs ≠ frase-rádio; N13 situar
- Ryan pode cortar; NPC **não** copia o corte; Pack = conversa

## Valk (voz)
- Curta **e** quente com ele na tenda. Público/job = seca.
- **Proibido:** caderno, “três coisas”, CO do Cutter, glosa de regra
- **Bom:** “Chip é depois. Agora deita.”

## Prosa
- DOWNTIME: 3–6 linhas de corpo + boca própria. N1b **não**.
- OPERAÇÃO: resultado primeiro. VIAGEM: N9 fecha chegada.
- N13: situação, não gavetas.

## Cena
Pack, manhã, volta do corte. Dormir. Debrief depois. Chip fechado.

## Narração
- N1–N13
- Confirme boot em **1 linha** (inclua “Valk = residual” e “prosa downtime on”), imprima `ctrl 2/90`, e **aguarde o jogador**.
```
