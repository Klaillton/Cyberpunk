# Context Pack — Template

> Copiar para `logs/context_pack_atual.md` e preencher. Alvo: **≤ ~120 linhas / ~4 KB**.  
> Procedimento: [sistema/comandos_jogador.md](../sistema/comandos_jogador.md) · Fatos: [sistema/fatos_duros.md](../sistema/fatos_duros.md)

**Gerado após sessão:** `NNN` · **Próxima:** `NNN+1` · **Branch:** `feature/linha-estavel`

---

## MOTOR (todo turno de RP)

1. **Não ecoar** o PC (≤2 linhas). Se descreveu procedimento/SOP → pular para **resultado**.  
2. **Delta** = **maior parte** da resposta (~≥60%): intel, NPC, tempo com efeito, pressão AGENDA.  
3. Em `OPERAÇÃO` / `VIAGEM`: **resultado primeiro** (não espelhar o plano).  
4. **VIAGEM limpa (N9):** sem anomalia/AGENDA no caminho → **fechar chegada** (sem filler de marcha).  
5. Fonte de pressão: **AGENDA DA CENA** → **NORTE curto** → [arco_ativo](../board/arco_ativo.md) (L1) → `event_queue` (F10).  
6. Escorregou? `[Motor de cena]` / `[Anti-eco]` · Estagnou? `[Avançar cena]` / `[Pressão]`.  
7. **Rodapé OOC:** linha em branco + `ctrl N/90` (+2 / resposta). Boot `ctrl 2/90`. Perdeu `ctrl ?/90`. Não narrar; não chrome; não mudar cena pelo número.

Detalhe: [diretrizes_narrador.md](../sistema/diretrizes_narrador.md) §7.1 · [motor_cena_1pager.md](../sistema/motor_cena_1pager.md)

---

## NOW (location-agnostic)

| Campo | Valor |
| ----- | ----- |
| Data in-game | |
| Período do dia | |
| Região | Badlands / Night City / Estrada / Outro |
| Local específico | |
| Facção / base local | |
| Cena / gancho | |
| Prioridade | **NORTE curto** |
| Segredos ativos | |
| Temperatura Ryan × Valkirya | baseline ops / residual íntimo / aftercare / frio público — **vence a ficha** |

---

## NORTE (orientação, não quest log)

> Horizontes. **Não** é trilho nem lista para fechar nesta resposta.  
> Curto = esta sessão. Médio = L1 (1–3 sessões). Longo = frentes, **sem** spoiler.  
> Operação: AGENDA (L0) · [arco_ativo](../board/arco_ativo.md) (L1) · `event_queue` (L2) · arco §5 (L3).  
> **Finalizar:** só a linha cujo horizonte mudou. Se não mudou, não tocar.  
> **Uma fonte:** não copiar esta tabela no board / dashboard.

| Horizonte | Norte |
| --------- | ----- |
| **Curto** (hoje / sessão) | |
| **Médio** (1–3 sessões) | |
| **Longo** (campanha) | |
| **Fora agora** | |

---

## Fatos duros em vigor

Citar IDs de `sistema/fatos_duros.md` (F01–F21 + L0x se aplicável):

- F03, F04, F11, …
- L0x: …

---

## Pendências quentes

> Só o que pode estourar **hoje** e **não** está na AGENDA / NORTE curto. Inventário: `event_queue.md`. Máx. **3**.

| ID | Uma linha |
| -- | --------- |
| | |

---

## AGENDA DA CENA (anti-estagnação)

> **Schema fixo · instâncias por cena.** Válido em qualquer região/local.  
> Preencher com ganchos do **local/região atuais** e pendências plausíveis (F10).  
> Atualizar em: boot de sessão · **mudança de local** (reescrever inteira) · Finalizar · quando um gancho resolver.  
> Máx. **3** ganchos. Preferir IDs de `event_queue` / NPCs já no SoT.  
> Motor: [diretrizes_narrador.md](../sistema/diretrizes_narrador.md) §7.1 (N1–N7).

| # | Gancho (1 linha) | Quem age se idle | Se Ryan idle / mood ≥3 turnos → o narrador faz |
| - | ---------------- | ---------------- | ---------------------------------------------- |
| 1 | | NPC ou mundo | ação concreta + resultado perceptível |
| 2 | | | |
| 3 | | | |

| Campo | Valor |
| ----- | ----- |
| **Modo atual** | OPERAÇÃO / DOWNTIME / INTIMIDADE / VIAGEM / COMBATE |
| **Turnos sem delta (estimado)** | 0 |
| **Região / local (NOW)** | *(espelhar bloco NOW — não é campo Pack-only)* |

**Preenchimento (qualquer mapa):**

1. Ler NOW (data, região, local, prioridade).  
2. Até 3 itens de **NORTE curto** / Pendências quentes **relevantes a este local**.  
3. Tarefas abertas de NPCs **presentes ou em alcance de comunicação**.  
4. Mudou de local (ex. Pack → estrada → NC)? → **reescrever a agenda inteira**; não carregar ganchos de outro lugar sem canal plausível.  
5. Local novo na narração → bloco **AMBIENTE** ([cena_ambientacao_ganchos.md](../sistema/cena_ambientacao_ganchos.md)); relacional SHOW ([arco_ativo.md](../board/arco_ativo.md) §7 se arco ativo).

---

## Vestindo agora (só quem está em cena)

> Estado completo: [fichas/notas_narrador/crew_vestindo_agora.md](../fichas/notas_narrador/crew_vestindo_agora.md) · Cards: [roupa_por_ocasiao.md](../fichas/notas_narrador/roupa_por_ocasiao.md)  
> **≤15 linhas.** Não colar o catálogo de 194 looks.

| Quem | Arquivo | 1 linha | Origem |
| ---- | ------- | ------- | ------ |
| | | | dona / empréstimo (?) |

Atualizar em: mudança de local · manhã · job · intimidade/gala · `[Roupa …]`.

---

## Carga de contexto

| Tier | Quando | Arquivos |
| ---- | ------ | -------- |
| **0** | Sempre / refresh | Este pack → `fatos_duros` → `board` se pack suspeito |
| **1** | Cena atual | *preencher conforme região* · roupa: cards + vestindo agora |
| **2** | Sob demanda | via `registro_arquivos.md` · catálogo guarda-roupas só se detalhe/# |

### Tier-1 sugerido para ESTE snapshot

- …

---

## RAW (se sandbox falhar)

Base: `https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/`

- `logs/context_pack_atual.md`
- `board/board_campanha.md`
- `sistema/fatos_duros.md`
- `logs/handoff_atual.md`
- `event_queue.md`
- último `logs/sessao_resumo_XXX.md`

---

## Confirmação de boot (formato fixo)

```
Boot OK · [data] · [região/local] · prioridade: [E0XX] · próximo resumo: NNN
```

Hierarquia: **RAW/repo > sandbox > memória de chat**.
