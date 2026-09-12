# Handoff atual — Continuidade para novo chat
**Gerado após:** sessão **025**  
**Próxima sessão:** **026** → `logs/sessao_resumo_026.md`  
**Data in-game ao fechar:** ~02 de Agosto de 2026 · noite · Pack · tenda do mapa do Reyes  
**Branch canônica:** `feature/linha-estavel`  
**Última atualização deste handoff:** 08 de Setembro de 2026

> **Primeiro arquivo a ler:** `logs/context_pack_atual.md`  
> **Arco L1:** `board/arco_ativo.md`  
> **Voz Valkirya:** `board/arco_ativo.md` §7 + diretrizes §3.3  
> **Prosa downtime:** `sistema/motor_cena_1pager.md` + diretrizes §5.1 · **N13 situar:** diretrizes §5.2  
> **Canon:** repo/RAW > handoff > memória de chat

**Não continuar o chat da 025.** Chat novo = 026.

---

## Boot (ordem de leitura)

1. `logs/context_pack_atual.md` (NOW + MOTOR + Voz Valk)  
2. Este handoff  
3. `sistema/fatos_duros.md` se dúvida  
4. `board/arco_ativo.md` se E015 / Cutter / estagnação  

**Confirmação (1 linha):**
```
Boot OK · ~02/08/2026 noite · Pack · tenda Reyes · Valk = residual quente · prosa downtime on · caixa 03/08 meio-dia · próximo resumo: 026 · Ruleset 1.3.0
```

---

## Estado atual (snapshot)

| Campo | Valor |
| ----- | ----- |
| Data | **~02/08/2026**, noite |
| Local | Pack: tenda do mapa do Reyes. Ryan + Valk **ainda no acampamento** |
| Condor | No chão (3 voos 02/08). Amanhã = leste visual (Sasha/Lira), sem chão |
| Intermediário | Janela **03/08 até meio-dia**; ponto = caixa no ombro da trilha velha, norte da 101 (ferro torto + 3 pedras); um salto; sem voz; sem ping antigo |
| Cutter | Corredor leste ~2h; camp não visitado; Reyes marca **um** corte após o céu |
| Ryan × Valk | 019 + residual íntimo alto; ela no **ombro** da trilha, não na caixa |
| Sasha / Lira | Jantar 025; leste amanhã visual; não vão à 101 |
| Reyes | Leste é Pack; 101 não é estrada do Pack; Ryan some e volta quando fechar |
| Base militar | **Não entra agora**; gatilho = mensagem → manhã seguinte |
| Economia | sem delta cash |
| Ruleset | **v1.3.0** |

### Cena de abertura (026)

**VIAGEM** Mule → corte. N9: fechar chegada. Depois AMBIENTE do ombro. Não filler de marcha. Não reabrir jantar/SOP Condor.

### AGENDA

1. Sair agora / dormir no corte.  
2. Caixa 03/08 meio-dia (um salto).  
3. Condor leste amanhã — visual; Reyes marca um corte.

### Trava

- Não reabrir Condor SOP / jantar 023 / base agora.  
- 019 = **perguntar** uma vez, não cobrar.  
- F15: Valk **não** chama Ryan de herói.  
- Cutter chão hoje = não.  
- NPCs ≠ frase-rádio; Reyes/Sasha/Lira têm boca própria. Valk-seca **não** vaza.
- Anti-máquina = sem *nome de regra* na prosa; personalidade (humor, cansaço, recusa) **obrigatória**.

### Voz Valkirya

Ops/público (Pack ouvindo / job): curta e seca. **Com Ryan agora:** curta **e** quente — frase de gente, não rádio. Curta ≠ dois vocábulos.  
**Proibido:** caderno, “três coisas”, “eu decido”, CO do Cutter, glosa de regra na prosa.  
**Bom (a dois):** Polegar no cinto. “Oficina e some. Eu pego o Mule.” Quase na boca. “O resto é tenda.”  
**Bom (Reyes, mesmo recado):** “Camp eu não tenho. Corredor, sim. (…) Tu some de novo no mesmo dia. A 101 não é minha estrada.”

### Prosa

DOWNTIME / social Pack (jantar, corredor, tenda, oficina, Reyes): 3–6 linhas de corpo + fala. SHOW + boca própria = delta. N1b **não** aplica.  
VIAGEM: N9 fecha chegada. OPERAÇÃO/recon/combate: resultado primeiro.  
**N13:** cada fato na situação a que pertence. Não gavetas (`Cobertura:`, `EM:`). Não omitir o dado.  
**Registro:** Ryan pode cortar; NPC **não** copia o corte. Pack = conversa.

---

## O que acabou de acontecer (025)

- Tarde 02/08 com Valk; SOP Condor reancorada.  
- 2º voo: pacote pede resposta no canal até o fim do dia.  
- 3º voo: janela 03/08 meio-dia + caixa 101.  
- Leste adiado para amanhã (Sasha/Lira, visual).  
- Reyes briefado. Freeze: ainda no Pack.

Detalhe: [sessao_resumo_025.md](sessao_resumo_025.md)

---

## Prompt de abertura (copiar no novo chat)

```markdown
# Cyberpunk RED — Continuidade (Sessão 026)

## Boot (tier-0)
- Repo: https://github.com/Klaillton/Cyberpunk · branch `feature/linha-estavel`
- Canon = arquivos do repo após sync / RAW
- **Não continuar o chat da 025.**
- Leia primeiro: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/context_pack_atual.md
- Resumo 025: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/sessao_resumo_025.md
- Handoff: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/handoff_atual.md
- Motor: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/sistema/motor_cena_1pager.md
- Voz Valk: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/board/arco_ativo.md

## Mecânica
- Ruleset **1.3.0** (F18); loadout sob demanda; sem inventar mods

## Estado
- **~02/08/2026 noite** · Pack · tenda do mapa do Reyes
- Ryan + Valk **ainda no acampamento**. Não saíram.
- Decisão: saem agora, dormem no corte (ombro da trilha velha, norte da 101), recon de madrugada; caixa ~meio-dia 03/08.
- Ryan na caixa; Valk no ombro.
- Cutter/leste: Condor com Sasha/Lira amanhã, visual, sem chão. Reyes marca um corte quando o pássaro voltar.
- Reyes: leste é dele; 101 não é estrada do Pack; Ryan some e volta quando fechar.

## Trava
- Não reabrir jantar 023 nem SOP Condor
- 019 = ela pergunta uma vez antes de vetar
- F15: sem “herói”
- Cutter chão ≠ cena de abertura
- NPCs ≠ frase-rádio; Valk-seca não vaza; N1b só ops/viagem/combate; N13 situar (não gavetas)

## Valk (voz)
- Curta **e** quente com ele (frase de gente, não rádio). Público/job = seca.
- Curta ≠ dois vocábulos. Valk-seca **não** vaza para Reyes/Sasha/Lira.
- **Proibido:** caderno, “três coisas”, CO do Cutter, glosa de regra
- **Bom:** “Oficina e some. Eu pego o Mule. O resto é tenda.”

## Prosa
- VIAGEM: N9 fecha chegada. Depois AMBIENTE do ombro.
- DOWNTIME / social Pack (jantar, Reyes, tenda): 3–6 linhas de corpo + boca própria = delta. N1b **não**.
- OPERAÇÃO/combate: resultado primeiro.
- **N13:** situar o dado (não gavetas; não omitir). AMBIENTE = checklist interno, uma situação na tela.
- NPCs ≠ frase-rádio. Ryan operador **não** vaza. Anti-máquina = vocabulário de regra, não personalidade.

## Cena
Abre VIAGEM Mule → corte. Fecha chegada. AMBIENTE ombro 101.

## Narração
- N1–N13
- Confirme boot em **1 linha** (inclua “Valk = residual quente” e “prosa downtime on”), imprima `ctrl 2/90`, e **aguarde o jogador**.
```
