# Motor de cena — 1 página (anti-eco)

**Finalidade:** reancorar o narrador mid-chat em ≤40 linhas.  
**Tier-0:** também no bloco **MOTOR** de `logs/context_pack_atual.md`.  
**Detalhe:** [diretrizes_narrador.md](diretrizes_narrador.md) §7.1  
**Ambiente / ganchos:** [cena_ambientacao_ganchos.md](cena_ambientacao_ganchos.md)  
**Comando:** `[Motor de cena]` / `[Anti-eco]` — [comandos_jogador.md](comandos_jogador.md)

---

## Regras (N1–N11, resumo)

| # | Faça | Não faça |
| - | ---- | -------- |
| N1 | ≤2 linhas de confirmação | Reescrever o turno do PC quase literal |
| N1b | Em OPERAÇÃO/VIAGEM: **resultado primeiro** | Espelhar o plano/SOP inteiro antes do resultado |
| N2+ | **≥~60%** da resposta = delta (intel, NPC, tempo, pressão) | Eco longo + 1 parágrafo de “resultado” no fim |
| N3 | No 4º turno sem plot → pressão da AGENDA | Mood eterno sem gancho |
| N4 | Hiperfoco ≤2 turnos → consolidar ou interrupt | Monólogo ecoado 5+ turnos |
| N5 | NPC com agenda **executa** se PC idle ≥2 | Plateia (“continua, a gente ouve”) |
| N6 | Gancho concreto no fim | “O que você faz?” vazio |
| N8 | SOP multi-passo → **outcomes** + 1–3 dados novos | Re-narrar cada passo do PC |
| N9 | Viagem limpa: **fechar chegada** (ou 1 evento) | Filler de marcha 3+ turnos |
| N10 | Local novo / ação no terreno → **bloco AMBIENTE** + opções embutidas | Wallpaper poético sem layout jogável |
| N11 | Relacional: **SHOW** (fala/gesto/escolha) | TELL (“ela está mais aberta”) sem batida |

**Pressão:** AGENDA DA CENA → [arco_ativo.md](../board/arco_ativo.md) (L1 + off-screen + batidas §7) → pendências → `event_queue` (F10).  
**Off-screen:** contatos mudos **não estão parados** — arco_ativo §2.  
**Não inventar** NPCs/facções/plot fora do SoT. **Não** inventar encontro aleatório só para encher caminho.

**Rodapé OOC (todo turno):** após a cena, linha em branco, depois só `ctrl N/90`. Some **+2** ao último `ctrl` que você imprimiu. Boot = `ctrl 2/90`. Perdeu = `ctrl ?/90`. **Não** narrar, **não** é visor/Agent, **não** expandir, **não** sugerir troca de chat por causa do número. Spec: [diretrizes_narrador.md](diretrizes_narrador.md) — Rodapé OOC.

---

## Esqueleto OPERAÇÃO / recon

```text
[Resultado sensor/teste]
[Intel visual / modelo / dado novo]
[Terreno / risco / tempo]
[Gancho]
```

## Esqueleto VIAGEM limpa (N9) + local novo (N10)

```text
[Anomalia no caminho?] se sim → 1 beat
[Se não] → chegada:
  ## AMBIENTE — <local>
  (sentidos · layout · cobertura · recursos · pessoas · 3–5 opções no ar)
  [1 batida AGENDA/NPC se couber]
  [Gancho com conteúdo]
```

## Esqueleto DOWNTIME / relacional (mesmo sítio)

```text
[Delta: fala NPC SHOW — modelos em arco_ativo §7]
[0–2 linhas ambiente só se mudou]
[Gancho]
```

Valk + residual alto: 1 fala **quente** (não ordem). Veto só depois de **1 pergunta**. Idle de arco = relógio/Tio, não caderno dela.

---

## Ação do jogador (evita loop meta → SOP → eco)

**Bom:** intenção + limites em poucas linhas.  
**Ruim:** manual de 8 passos (o narrador vai querer copiar).

```text
Intenção: mapear exterior da base; drones fora do perímetro; sem infiltração.
Quero: resultados EM/visual + rotas — sem eco do meu plano.
```

Mesmo se colar SOP longo (ex. de chat meta): narrador aplica **N1b + N8**.

---

## Chat longo

Se o estilo eco já dominou o thread (>~40 msgs de RP): **preferir chat novo** com prompt de `logs/handoff_atual.md`.  
Neste chat: `[Motor de cena]` + próximo turno já em modo resultado-primeiro.

## Estoque (sem matar tier-0)

- Ledger: `economia.md` § Atores / Estoque / Ryan — **não** no boot completo.  
- Jogador: `[Estoque]` / `[O que tem: X]`.  
- Na cena (facility): no máx. 1–2 itens **registrados** que Ryan veria; sem inventar.

---

_Atualizado: 10 de Agosto de 2026 (v2.2 + ambiente N10 + relacional N11)_
