# Criação de Ficha — Cyberpunk RED (CPR)

> Complementa [especificacao_tecnica_v1.1.md](./especificacao_tecnica_v1.1.md) §6.3  
> Referência visual: *Cyberpunk RED* p.450–452 (ficha em branco)  
> Fluxo de criação: p.40–42 (Complete Package)

## Tiers de ficha

| Tier | Uso | Exemplos na campanha |
|------|-----|----------------------|
| `protagonist` | PC jogável | Ryan |
| `crew_full` | Aliados com CPR completa | Valk, Jax, Kaz, Stephania, Reina, **Alex** |
| `npc_reference` | Recorrentes com função | Reyes, Tio Gringo, Lira, **Rusty** |
| `npc_generic` | Arquétipo de facção | Raffen Shiv soldado |

## Layout visual (p.450–452)

- **Página mecânica:** 10 STATs, Skills por categoria, armas, armadura
- **Página vida:** Lifepath, HL/EMP, €$, estilo de vida
- **Página chrome:** slots Internal/External/Fashionware/Borgware

Frontend: `frontend/cpr-sheet.js` + `cpr-sheet.css` — componente `CprSheetView` no drawer Ficha.

## Protagonista — Complete Package

1. Role (Ability = 4)
2. Lifepath (texto livre na v1)
3. STATs — 62 pts, min 2 max 8
4. Skills — 86 pts, max 6, básicas ≥ 2
5. Identidade (nome, handle, slug, aparência, background)

API:

- `GET /api/character-creation/catalog`
- `POST /api/character-creation/validate`
- `POST /api/characters`
- `PUT /api/characters/{id}/protagonist`
- `GET /api/characters/{id}/sheet`

Wizard: Admin → **Criar protagonista**

## Facções — roster semeado

`data/factions/pack_badlands_roster.json` define papéis:

| Função | NPC |
|--------|-----|
| Líder | Reyes |
| Ferreiro | Tio Gringo |
| Mecânico veículos | Rusty |
| Jovem incursões | Lira |

`POST /api/factions/pack_badlands/seed-roster` — cria fichas faltantes.

## Migração

```bash
python scripts/migrate_fichas_cpr.py
```

Adiciona frontmatter às fichas conhecidas e executa seed do Pack. Backup em `fichas/_backup_pre_cpr/`.

## Módulos

- `motor/character_creation/` — parser, validator, renderer, resolver, faction_roster
- `fichas/templates/cpr_*.md` — templates por tier
- `scripts/migrate_fichas_cpr.py`

## Sprint D — status

| Fase | Entrega |
|------|---------|
| D0 | Este documento + templates + roster JSON |
| V1 | CprSheetView + GET sheet |
| M1 | Migração + Rusty + Raffen archetype |
| D1–D3 | Wizard + API protagonista |
| F1 | API seed roster facção |
| N1 | Promoção automática NPC (backlog) |
| D4 | Narração parametrizada (backlog) |