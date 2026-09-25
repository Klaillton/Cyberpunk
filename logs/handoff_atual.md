# Handoff atual — Continuidade para novo chat
**Gerado após:** sessão **027**  
**Próxima sessão:** **028** → `logs/sessao_resumo_028.md`  
**Data in-game ao fechar:** ~04 de Agosto de 2026 · manhã · Mule → Pack  
**Branch canônica:** `feature/linha-estavel`  
**Última atualização deste handoff:** 25 de Setembro de 2026

> **Primeiro arquivo a ler:** `logs/context_pack_atual.md`  
> **Obrigatório no boot:** `sistema/fatos_duros.md`  
> **Boca:** ramo antes da frase — bloco abaixo e no context pack  
> **Canon:** repo/RAW > handoff > memória de chat

**Não continuar o chat da 027.** Chat novo = 028.

---

## Boot (ordem de leitura)

1. `logs/context_pack_atual.md` (NOW + NORTE + MOTOR + Boca)
2. `sistema/fatos_duros.md` (obrigatório)
3. Este handoff
4. `logs/sessao_resumo_027.md`

**Confirmação (1 linha):**
```
Boot OK · ~04/08/2026 manhã · Pack · Mule volta · Valk = residual (ops→tenda quente) · boca ramo 2 (Mule; tenda = ramo 3) · chip lacre intacto · hop NC 05/08 21h · corte 027 feito · próximo resumo: 028 · Ruleset 1.3.0
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

### Boca (ramo antes da frase)

NOW = Mule com Reyes → **ramo 2**. Tenda, quando ficarem a sós → **ramo 3**. O ramo de cima não vaza.

1. **Rádio / ops / combate:** curta, seca, pessoa. Resultado primeiro.
2. **Pack social:** conversa; uma fala de gente; corpo no meio; cada um pela ficha.
3. **A sós:** uma fala, um fôlego. Selo de duas frases não serve. Chip, Reyes e hop fora desta boca.

“Três coisas” = ultimato, não teto de frase. Exemplos no prompt de abertura.

---

## Prompt de abertura (copiar no novo chat)

```markdown
# Cyberpunk RED — Continuidade (Sessão 028)

## Boot (tier-0)
- Repo: https://github.com/Klaillton/Cyberpunk · branch `feature/linha-estavel`
- Canon = arquivos do repo após sync / RAW
- **Não continuar o chat da 027.**
- Leia primeiro: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/context_pack_atual.md
- Leia obrigatório: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/sistema/fatos_duros.md
- Resumo 027: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/sessao_resumo_027.md
- Handoff: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/handoff_atual.md

## Mecânica
- Ruleset **1.3.0** (F18); loadout sob demanda; sem inventar mods

## Estado
- **~04/08/2026 manhã** · Pack · Mule volta do corte
- Chip E015 **lacre intacto**; hop NC **05/08 após 21h**
- Corte Cutter 027 feito (recon, sem tiro; 7 quentes; lona morta). Debrief pendente.
- Condor unmanned (F16)

## Sandbox
- O que não está no arquivo não entra na cena.
- Sem NPC, facção ou tech nova.
- Sem lugar que o pack não descreveu (banho, box, cerca, oficina).
- `fatos_duros` vence a memória do chat.
- Repo / RAW vencem este prompt se divergirem.

## Trava
- Não reabrir jantar 023 nem SOP Condor nem a caixa da 101 nem o canyon
- 019 = ela pergunta uma vez antes de vetar
- F15: sem “herói” · F21: Valkirya / Valk · F16: Condor unmanned
- N13 situar (não gavetas), em todo ramo

## Boca (ramo antes da frase — esta seção ganha das outras)
NOW = Mule com Reyes → ramo 2. Tenda, a sós → ramo 3. O ramo de cima não vaza. Quem fala muda o vocabulário, não o ramo. Ryan pode cortar; ninguém copia o corte.
1. Rádio / ops / combate: curta, seca, pessoa. Resultado primeiro. ≤2 linhas só confirmam a ação do PC.
   Ex.: “Mule no leste, abort no rádio. Eu no volante. Tu marca a janela.”
2. Pack social (refeitório, oficina, pátio, corredor, Reyes, Mule parado): conversa. Uma fala de gente, corpo no meio. Cada um pela ficha.
   Ex. Reyes: “Camp eu não tenho. Corredor, sim. O céu amanhã me diz onde corto — um, não um raid. Tu some de novo no mesmo dia. A 101 não é minha estrada.”
3. A sós (tenda, banho, cama): uma fala, um fôlego. Quieta pode. Selo de duas frases não serve. Chip, Reyes e hop fora desta boca.
   Modelo de fôlego (copia o tamanho; não repete esta cena): “Você fala fico como se eu fosse te expulsar. Não vou. Fiquei este tempo todo com você pra você não levantar no automático, e agora que levantou ainda está aqui. Tá bom. Fica. Eu gosto quando você para de tratar o corpo como ferramenta que precisa ir embora. O resto do mundo espera do lado de fora. Aqui ainda é só isso.”
“Três coisas” = ultimato de condições, não teto de frase. Sem herói. Sem tom de CO. 019 = perguntar uma vez.
N13 em todo ramo. N9 fecha viagem limpa. N1b só no ramo 1. Corpo nos ramos 2 e 3: 3–6 linhas é piso.

## Cena
Pack, manhã, volta do corte. Dormir. Debrief depois. Chip fechado.

## Narração
- N1–N13
- Confirme boot em **1 linha** (inclua “Valk = residual” e “boca ramo 2 (Mule; tenda = ramo 3)”), imprima `ctrl 2/90`, e **aguarde o jogador**.
```
