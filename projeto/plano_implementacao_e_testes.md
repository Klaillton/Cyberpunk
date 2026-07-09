# Plano de Implementação e Testes por Fase

> Complementa [especificacao_tecnica_v1.1.md](./especificacao_tecnica_v1.1.md)  
> **Status vivo:** [status_projeto.md](./status_projeto.md) (atualizar a cada sprint)  
> Regra: **nenhuma fase fecha sem sua bateria de testes verde.**

**Última revisão:** 09/07/2026 · **107 pytest** (+2 slow) · **19 e2e**

---

## Pirâmide de testes (estado atual)

```text
        E2E Playwright (UI + API browser)     19 testes
       ─────────────────────────────────
      Integração HTTP (narracao_api real)
     ───────────────────────────────────
    Unitários (engine + helpers da API)      107 testes
```

| Comando | Escopo |
|---------|--------|
| `npm run test:unit` | pytest `tests/unit` + `tests/integration` |
| `npm run test:e2e` | Playwright `tests/e2e` |
| `npm run test:all` | unit + e2e (gate completo) |
| `npm run test:slow` | smoke Ollama real (`@slow`) |

**Gate obrigatório antes de cada merge/commit de feature:** `npm run test:all`

---

## Mapa de fases (visão geral)

```text
[Fases 0–5]  ✅ concluídas
[Fase 5.1]   ✅ MVP sessão solo (canais, brief, resumo, parser)
[Sprint A]   ✅ qualidade do turno (FAISS + router + gate no hot path)
[Sprint B]   ✅ UX, e2e, CI
[Sprint C]   ⏸ Pi + sync (opcional / adiado — ver status_projeto.md)
```

---

## Fases concluídas

### Fase 0 — Fundação ✅ concluída

**Objetivo:** rede de segurança antes de refatorar para FastAPI.

| Entrega | Status |
|---------|--------|
| pytest unit + integration | ✅ |
| E2E drawers + chat + API | ✅ |
| Docker compose LLM local | ✅ |
| Provider Ollama no MVP | ✅ |

---

### Fase 1 — Paridade FastAPI ✅ concluída

- `motor/`, `api/main.py`, routers, `scripts/narracao_api.py`
- Critério: endpoints legados + e2e verde ✅

---

### Fase 2 — LLM local (Ollama) ✅ concluída

- Smoke `@slow`, docker compose, campo `model` na resposta API
- Stack: `deploy/docker-compose.yml` + `pull_models.ps1`

---

### Fase 3 — Indexação (SQLite + FAISS) ✅ concluída

- `motor/storage/`, `motor/markdown/sync_engine`, `motor/index/`
- `POST /api/search`, `scripts/rebuild_index.py`
- **Nota:** indexação existe; **narração ainda não usa FAISS no contexto** → Sprint A

---

### Fase 4 — ProviderRouter + Quality Gate ✅ concluída (módulos)

- `motor/llm/router.py`, `quality_gate.py`, `routing_service.py`
- `GET /api/routing/policy`, `POST /api/routing/preview`
- **Nota:** router/gate **não estão no `generate_reply`** → Sprint A

---

### Fase 5 — Updates assistidos ✅ concluída

- `motor/update/`, `POST /api/save`, drawer Propostas, e2e `proposals.spec.js`
- Ingest de `UPDATE_PROPOSALS` apenas em `channel == "gestor"` (Sistema não ingere) → Sprint B

---

### Fase 5.1 — MVP sessão solo ✅ concluída

Extensão da branch `feat/narracao-solo-mvp` (não prevista no plano original):

| Entrega | Status |
|---------|--------|
| Canais Mestre + Sistema | ✅ |
| `GET /api/brief` | ✅ |
| Resumo de sessão com histórico | ✅ |
| Parser ação/fala/beat | ✅ |
| Histórico chat (narração, mestre, sistema) | ✅ |
| Contexto Mestre/Sistema + índice fichas | ✅ |
| Sidebar por grupos (Campanha, Personagem, Sessão) | ✅ |

---

## Sprint A — Qualidade do turno ✅ concluída

**Objetivo:** fechar lacunas do DoD v1.1 no fluxo real de narração.

| # | Entrega | Onde |
|---|---------|------|
| A1 | Contexto híbrido regex + FAISS + entidades | `motor/context_service.py` |
| A2 | `generate_turn` com `ProviderRouter` | `motor/narration.py` |
| A3 | `ResponseQualityGate` + 1 retry (local ou cloud) | `motor/narration.py` |
| A4 | `provider_routing_log` | `003_provider_routing_log.sql`, `motor/routing_log.py` |
| A5 | Metadados na API | `MessageResponse.routing_decision`, `quality_*` |

**Testes:** `test_context_service.py`, `test_narration_turn.py`, `test_routing_log.py`

---

## Sprint B — UX, testes e CI ✅ concluída

| # | Entrega | Status |
|---|---------|--------|
| B1 | Ingest de propostas no canal Sistema | ✅ |
| B2 | E2E: Sistema, resumo de sessão, meta qualidade | ✅ |
| B3 | Drawer routing preview | ✅ |
| B4 | `.github/workflows/test.yml` | ✅ |

**Testes novos:** `test_message_router.py`, `chat.spec.js`, `session-summary.spec.js`, `routing-preview.spec.js`

---

## Sprint C — Raspberry Pi (opcional / adiado)

> **Decisão:** adiar. Laptop-only + GitHub cobre o uso solo. Retomar só se precisar de API 24/7 na LAN sem laptop. Detalhes: [status_projeto.md § Decisão Pi](./status_projeto.md#decisão-raspberry-pi).

| # | Entrega | Status |
|---|---------|--------|
| C1 | `deploy/docker-compose.pi.yml` validado em ARM | scaffold ✅ / smoke ⬜ |
| C2 | Script sync campanha Pi ↔ laptop | ⬜ |
| C3 | systemd unit | ⬜ |

**Substituto mais simples:** `git pull` / `git push` + CI (Sprint B4).

---

## Matriz: feature → teste mínimo

| Feature | Unit | Integration | E2E |
|---------|------|-------------|-----|
| Integridade arquivos | `test_narracao_engine` | — | — |
| Seleção de contexto (regex) | `test_narracao_engine` | — | — |
| Contexto Mestre/Sistema | `test_narracao_engine` | — | — |
| Ficha personagem | `test_narracao_api` | `character-profile` | drawers |
| Journal CRUD | `test_narracao_api` | `test_journal_crud` | drawers |
| Narração principal | `generate_reply` | `test_narracao_endpoint` | chat |
| Canal Mestre | `test_narracao_engine` | — | chat (mock) |
| Canal Sistema | `test_narracao_engine` | `test_sistema_endpoint` | chat (mock) |
| Brief campanha | `brief_service` | `GET /api/brief` | — |
| Resumo de sessão | `test_session_command_handler` | `test_narracao_summary_command` | session-summary |
| Meta qualidade turno | `test_narration_turn` | `routing_decision` em narracao | chat (mock) |
| Busca FAISS | `test_search_*` | `test_search_api` | — |
| Routing preview | `test_provider_router` | `routing/preview` | routing-preview |
| Propostas update | `test_update_*` | `proposals` | proposals.spec |
| Player message parser | `test_player_message` | — | — |
| Ollama | mock | smoke `@slow` | mock route |
| Docker compose | — | `test_docker_compose` | — |
| Lista fichas (Sistema) | `list_campaign_sheets` | — | — |

---

## CI recomendado (Sprint B4)

```yaml
# .github/workflows/test.yml
jobs:
  unit-integration:
    runs-on: ubuntu-latest
    steps:
      - run: pip install -r requirements-dev.txt
      - run: pytest tests/unit tests/integration -q

  e2e:
    runs-on: ubuntu-latest
    steps:
      - run: npm ci && npx playwright install chromium
      - run: npm run test:e2e
```

---

## Topologia de deploy

| Perfil | Quando usar | Compose |
|--------|-------------|---------|
| **Laptop** (padrão) | Sessão com Ollama na GPU | `deploy/docker-compose.yml` |
| **Dev local** | `python scripts/narracao_api.py` | — |
| **Pi** (opcional) | Hub estado 24/7 sem LLM | `deploy/docker-compose.pi.yml` |

Hardware alvo documentado: laptop RTX 4070 8 GB VRAM · Pi 4 8 GB (só API/sync).

---

## Referências

- [status_projeto.md](./status_projeto.md) — tracker vivo + decisão Pi
- [especificacao_tecnica_v1.1.md](./especificacao_tecnica_v1.1.md) — contratos e DoD
- [especificacao_inicial.md](./especificacao_inicial.md) — visão original (Pi-centric; superseded parcialmente pela v1.1)
- [arquitetura_narracao_solo.md](../sistema/arquitetura_narracao_solo.md) — MVP e roadmap narrativo