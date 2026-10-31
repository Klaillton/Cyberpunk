# Handoff atual — Continuidade para novo chat
**Gerado após:** sessão **031**  
**Próxima sessão:** **032** → `logs/sessao_resumo_032.md`  
**Data in-game ao fechar:** ~05 de Agosto de 2026 · noite · oficina_rua · Watson · Northside  
**Branch canônica:** `feature/linha-estavel`  
**Última atualização deste handoff:** 31 de Outubro de 2026

> **Primeiro arquivo a ler:** `logs/context_pack_atual.md`  
> **Obrigatório no boot:** `sistema/fatos_duros.md`  
> **Boca:** ramo antes da frase — bloco abaixo e no context pack  
> **Canon:** repo/RAW > handoff > memória de chat

**Não continuar o chat da 031.** Chat novo = 032.

---

## Boot (ordem de leitura)

1. `logs/context_pack_atual.md` (NOW + NORTE + MOTOR + Boca)
2. `sistema/fatos_duros.md` (obrigatório)
3. `sistema/vozes.md` (referência de boca; não é estado)
4. Este handoff
5. `logs/sessao_resumo_031.md`

**Confirmação (1 linha):**
```
Boot OK · ~05/08/2026 noite · oficina_rua · Watson · Northside · Valk = residual · boca ramo 1 (ops; Pack = ramo 2) · chip aberto (token) · hop fechado · busca aberta · debrief Reyes pendente · próximo resumo: 032 · Ruleset 1.4.0
```

---

## Estado atual (snapshot)

| Campo | Valor |
| ----- | ----- |
| Data | **~05/08/2026**, noite |
| Local | oficina_rua · Watson · Northside · Mule parado na porta de metal |
| Chip E015 | **Lacre aberto**; token de um uso; hop **fechado** (031). Stick apontou Kaz. Canal antigo mudo. No Warden (compartimento morto) |
| Cutter | Corte 04/08 **feito** (recon, sem tiro). 7 quentes; lona = fogueira morta. Debrief **ainda pendente**. |
| Condor | Unmanned; pousou 03/08; Sasha/Lira no gancho/visor |
| Ryan × Valk | 019 + residual alto; intimidade 028–029; Lena em intimidade |
| Reyes | Debrief do corte **não feito** (aviso via Rusty) |
| Base militar | **Não entra agora** |
| Ruleset | **v1.4.0** (chrome = número ou função; 017–028 ficam em 1.3.0) |

### Cena de abertura (032)

Oficina_rua, noite, Watson · Northside. Mule parado. Valkirya no volante. Warden no corpo. Pill no fundo do Mule. Vespas em perímetro. Hop fechado. Sem contato. Busca pela mão do Kaz aberta. Residual íntimo alto. Não reabrir jantar 023 / SOP Condor / caixa 101 / canyon.

### AGENDA

1. Busca na oficina_rua (Kaz aparece de vez em quando).  
2. Debrief Reyes na volta.  
3. Cobertura no Mule. Valk age no primeiro turno: braço, fome, o Mule, ou cuidar dele. Sem hop na boca.

### Trava

- Não reabrir Condor SOP / jantar 023 / base agora / caixa 101 / canyon do corte.  
- 019 = perguntar uma vez. F15 sem “herói”. F21 Valkirya / Valk / Morena (Ryan; Morena = carinho usual). Lena = nome. Morena ≠ NPC nova.  
- F16 Condor unmanned. F25: Pill = mula no fundo do Mule, não mochila. F03: a mochila é o Warden. Vespas no perímetro.  
- Ryan pode cortar; NPC **não** copia o corte.

### Boca (ramo antes da frase)

NOW = ops na oficina_rua → **ramo 1**. Reyes / refeitório / pátio → **ramo 2**. O ramo de cima não vaza.

1. **Rádio / ops / combate:** curta, seca, pessoa. Resultado primeiro.
2. **Pack social:** conversa diegética e fluida; uma fala de gente; corpo no meio; pode ter mais corpo; cada um pela ficha.
3. **A sós:** uma fala, um fôlego, diegética e fluida. Pode ter mais corpo. Selo de duas frases não serve. Chip, Reyes e hop fora desta boca. Ela responde a ele ou traz uma coisa dela. Uma. Sem menu.

“Três coisas” = ultimato, não teto de frase.

---

## Prompt de abertura (copiar no novo chat)

```markdown
# Cyberpunk RED — Continuidade (Sessão 032)
## Boot (tier-0)
- Repo: https://github.com/Klaillton/Cyberpunk · branch `feature/linha-estavel`
- Canon = arquivos do repo após sync / RAW
- **Não continuar o chat da 031.**
- Leia primeiro: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/context_pack_atual.md
- Leia obrigatório: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/sistema/fatos_duros.md
- Vozes (referência de boca, não é estado): https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/sistema/vozes.md
- Resumo 031: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/sessao_resumo_031.md
- Handoff: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/handoff_atual.md
## Mecânica
- Ruleset **1.4.0** (F18); loadout sob demanda; chrome na jogada = número ou função; sem inventar mods
## Estado
- **~05/08/2026 noite** · oficina_rua · Watson · Northside
- Chip E015 **aberto** (token um uso); hop **fechado** (031); stick apontou Kaz; canal antigo mudo
- Corte Cutter 027 feito (recon, sem tiro; 7 quentes; lona morta). Debrief ainda pendente.
- Condor unmanned (F16)
## Sandbox
- O que não está no arquivo não entra na cena.
- Sem NPC, facção ou tech nova.
- Lugar físico: o cartão **SET NOW** do pack. Destino indefinido não vira lugar.
- Indefinido não se narra. Momento importante sem nó no pack não ganha evento. Frase no chat não é nó.
- `fatos_duros` vence a memória do chat.
- Repo / RAW vencem este prompt se divergirem.
## Trava
- Não reabrir jantar 023 nem SOP Condor nem a caixa da 101 nem o canyon
- 019 = ela pergunta uma vez antes de vetar
- F15: sem “herói” · F21: Valkirya / Valk / Morena (Ryan) · Lena = nome · Morena ≠ NPC nova · F16: Condor unmanned · F25: Pill no fundo do Mule, não mochila · F03: mochila = Warden
- N13 situar o lugar (não gavetas), em todo ramo. Na fala do ramo 3 não entra hop, horário, lugar, janela, debrief nem “ainda não é o ponto”
## Boca (ramo antes da frase — esta seção ganha das outras)
NOW = ops na oficina_rua → ramo 1. Reyes / Pack social → ramo 2. O ramo de cima não vaza. Quem fala muda o vocabulário, não o ramo. Ryan pode cortar; ninguém copia o corte.
1. Rádio / ops / combate: curta, seca, pessoa. Resultado primeiro.
2. Pack social: conversa diegética e fluida. Uma fala de gente, corpo no meio. Pode ter mais corpo. Cada um pela ficha. Quem está no NOW traz uma coisa sua, já escrita. Sem menu.
3. A sós: uma fala, um fôlego, diegética e fluida. Pode ter mais corpo. Ela responde a ele ou traz uma coisa dela. Uma. Humor seco, sem despacho, sem menu. Coisa dela nesta cena: braço, fome, o Mule, ou cuidar dele. Chip, Reyes e hop fora desta boca. Ele veta ou ajusta.
“Três coisas” = ultimato de condições, não teto de frase. Sem herói. Sem tom de CO. 019 = perguntar uma vez.
N13 situa o fato escrito, sem gaveta. N9 fecha a viagem se o destino está escrito; destino indefinido não vira lugar. N1b só no ramo 1. Corpo nos ramos 2 e 3: 3–6 linhas é piso, e o lugar muda. A mesma mão não volta no turno seguinte.
## Cena
Oficina_rua, noite, Watson · Northside. Mule parado. Valkirya no volante. Warden no corpo. Pill no fundo do Mule. Vespas em perímetro. Hop fechado. Sem contato. Quem fala: `sistema/vozes.md`. Pack congelado em `logs/context_pack_pack.md` — não abrir no boot.
## Narração
- N1–N13
- Confirme boot em **1 linha** (inclua “Valk = residual” e “boca ramo 1 (ops; Pack = ramo 2)”), imprima `ctrl 2/90`, e **aguarde o jogador**.
```
