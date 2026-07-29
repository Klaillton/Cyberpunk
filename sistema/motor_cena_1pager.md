# Motor de cena — 1 página (anti-eco)

**Finalidade:** reancorar o narrador mid-chat em ≤40 linhas.  
**Tier-0:** também no bloco **MOTOR** de `logs/context_pack_atual.md`.  
**Detalhe:** [diretrizes_narrador.md](diretrizes_narrador.md) §7.1  
**Comando:** `[Motor de cena]` / `[Anti-eco]` — [comandos_jogador.md](comandos_jogador.md)

---

## Regras (N1–N9, resumo)

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

**Pressão:** AGENDA DA CENA → pendências do pack → `event_queue` (só local atual, F10).  
**Não inventar** NPCs/facções/plot fora do SoT. **Não** inventar encontro aleatório só para encher caminho.

---

## Esqueleto OPERAÇÃO / recon

```text
[Resultado sensor/teste]
[Intel visual / modelo / dado novo]
[Terreno / risco / tempo]
[Gancho]
```

## Esqueleto VIAGEM limpa (N9)

```text
[Anomalia no caminho?] se sim → 1 beat
[Se não] → chegada ao destino (1 bloco). Fim da marcha.
```

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

_Atualizado: 29 de Julho de 2026 (v2.1 + estoque)_
