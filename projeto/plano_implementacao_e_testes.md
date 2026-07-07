# Plano de Implementação e Testes por Fase

> Complementa [especificacao_tecnica_v1.1.md](./especificacao_tecnica_v1.1.md)  
> Regra: **nenhuma fase fecha sem sua bateria de testes verde.**

---

## Pirâmide de testes (estado atual)

```text
        E2E Playwright (UI + API browser)
       ─────────────────────────────────
      Integração HTTP (narracao_api real)
     ───────────────────────────────────
    Unitários (engine + helpers da API)
```

| Comando | Escopo |
|---------|--------|
| `npm run test:unit` | pytest `tests/unit` + `tests/integration` |
| `npm run test:e2e` | Playwright `tests/e2e` |
| `npm run test:all` | unit + e2e (gate completo) |

**Gate obrigatório antes de cada merge/commit de feature:** `npm run test:all`

---

## Por onde começar a implementação

Ordem recomendada — cada etapa **estende** o MVP, não reescreve do zero.

### Fase 0 — Fundação (AGORA) ✅ em progresso

**Objetivo:** rede de segurança antes de refatorar para FastAPI.

| Entrega | Status |
|---------|--------|
| pytest unit + integration | ✅ |
| E2E drawers + chat + API | ✅ |
| Docker compose LLM local | ✅ |
| Provider Ollama no MVP | ✅ |

**Testes desta fase:**

- `tests/unit/test_narracao_engine.py` — integridade, contexto, prompt
- `tests/unit/test_narracao_api.py` — markdown, journal, ollama mock
- `tests/integration/test_api_server.py` — HTTP real (subprocess)
- `tests/e2e/drawers.spec.js` — ficha, journal, NPC token
- `tests/e2e/chat.spec.js` — canal narrador, API profile/journal

**Não avançar para Fase 1 sem:** `npm run test:all` verde.

---

### Fase 1 — Paridade FastAPI ✅ concluída

**Objetivo:** substituir `http.server` por FastAPI mantendo contratos idênticos.

**Entregue:**

- `motor/` — settings, journal, markdown, character, npc, narration
- `api/main.py` + routers (`journal`, `character`, `npc`, `message`)
- `scripts/narracao_api.py` — thin wrapper → `uvicorn api.main:app`
- `requirements.txt` — fastapi, uvicorn, pydantic
- Testes: 24 pytest + 13 e2e = **37/37** verde

**Subir servidor:**

```bash
python -m uvicorn api.main:app --host 127.0.0.1 --port 8787
# ou
python scripts/narracao_api.py
```

**Critério de done:** ✅ endpoints legados retornam mesmos campos JSON; e2e sem alteração no front.

---

### Fase 2 — LLM local em produção (Ollama) ✅ concluída

**Objetivo:** narrativa real via Docker sem custo API.

**Entregue:**

- `tests/integration/test_ollama_smoke.py` — smoke `@slow` (skip se Ollama/modelo ausente)
- `tests/integration/test_docker_compose.py` — `docker compose config` + serviços esperados
- `tests/integration/ollama_helpers.py` — healthcheck Ollama + detecção de modelo
- `api/schemas.py` — campo `model` na resposta quando `provider: ollama`
- `npm run test:slow` — executa smoke contra Ollama real
- `pyproject.toml` — testes `@slow` excluídos do `test:unit` padrão

**Subir stack LLM local:**

```powershell
.\deploy\scripts\pull_models.ps1   # primeira vez — baixa modelos
docker compose -f deploy/docker-compose.yml --env-file deploy/.env up -d
```

**Smoke manual (com Ollama rodando):**

```bash
npm run test:slow
```

**Critério de done:** ✅ `POST /api/narracao` retorna texto do modelo local com `provider: ollama` e `model` preenchido (validado via `test:slow` quando Ollama está up).

---

### Fase 3 — Indexação (SQLite + FAISS) ✅ concluída

**Objetivo:** Markdown da campanha → `data/motor.db` + índice vetorial FAISS.

**Entregue:**

- `motor/storage/` — SQLite + migration `001_initial.sql`
- `motor/markdown/` — parser, chunker, `sync_engine`, descoberta de arquivos legados (`fichas/`, `board/`, etc.)
- `motor/index/` — `TfidfEmbedder` (padrão CI/Pi) + `MiniLmEmbedder` opcional
- `motor/entities/entity_resolver.py` — aliases (`Valk` → `lena_valk_kane`)
- `POST /api/search` — busca semântica com filtros `doc_type`
- `scripts/rebuild_index.py` — rebuild manual SQLite + FAISS
- Testes: **31 pytest** verde (+2 docker skip, +2 slow deselected)

**Rebuild do índice:**

```bash
python scripts/rebuild_index.py
# ou via API (lazy sync na primeira busca)
curl -X POST http://127.0.0.1:8787/api/search -H "Content-Type: application/json" -d "{\"query\":\"Valk motorista\"}"
```

**Critério de done:** ✅ busca semântica retorna chunk de personagem/NPC conhecido (`lena_valk_kane`).

---

### Fase 4 — ProviderRouter + Quality Gate ✅ concluída

**Objetivo:** local por padrão, cloud só quando necessário.

**Entregue:**

- `motor/llm/router.py` — `ProviderRouter` + heurísticas (`SceneComplexityScorer`)
- `motor/llm/classifier.py` — tier heurístico (phi3:mini opcional depois)
- `motor/llm/quality_gate.py` — NPC inventado, contradição board, controle do protagonista
- `motor/routing_service.py` — monta manifest + entidades para preview
- `GET /api/routing/policy`, `POST /api/routing/preview`
- Settings: `LLM_ROUTING_POLICY`, `CLOUD_FALLBACK_ENABLED`, `CLOUD_PROVIDER`
- Testes: **41 pytest** verde

**Preview (sem gastar tokens de narração):**

```bash
curl -X POST http://127.0.0.1:8787/api/routing/preview \
  -H "Content-Type: application/json" \
  -d '{"message":"Observo o acampamento","channel":"narracao"}'
```

**Critério de done:** ✅ preview retorna `decision` auditável; `hybrid` escala para cloud em cena complexa; quality gate rejeita NPC inventado.

---

### Fase 5 — Updates assistidos ✅ concluída

**Objetivo:** propostas de mudança com aprovação humana.

**Entregue:**

- `motor/update/` — `parser`, `validator`, `applier`, `store`
- `POST /api/save` — aplica propostas aprovadas + reindexa FAISS
- `GET /api/proposals`, `POST /api/proposals/ingest`
- Integração em `POST /api/narracao` — extrai bloco `UPDATE_PROPOSALS`
- UI — drawer **Propostas** com badge, aprovar/rejeitar
- Testes: **46 pytest** + e2e `proposals.spec.js`

**Fluxo:**

```text
LLM responde com ---UPDATE_PROPOSALS--- → parser → validator → SQLite (pending)
Jogador aprova na UI → POST /api/save → applier → markdown + sync FAISS
```

**Critério de done:** ✅ proposta validada só persiste após aprovação explícita.

---

### Fase 6 — Raspberry + sync

**Objetivo:** Pi 24/7 com estado; laptop na sessão.

**Ordem:**

1. `deploy/docker-compose.pi.yml`
2. Script sync campanha Pi ↔ laptop
3. systemd unit

**Testes:** smoke Pi sem GPU; integridade após sync.

---

## Matriz: feature → teste mínimo

| Feature | Unit | Integration | E2E |
|---------|------|-------------|-----|
| Integridade arquivos | `test_narracao_engine` | — | — |
| Seleção de contexto | `test_narracao_engine` | — | — |
| Ficha personagem | `test_narracao_api` | `character-profile` | drawers |
| Journal CRUD | `test_narracao_api` | `test_journal_crud` | drawers + chat |
| Narração principal | `generate_reply` | `test_narracao_endpoint` | loading |
| Canal narrador | `generate_reply` | `test_narrador_endpoint` | chat |
| NPC token | — | `test_npc_asset` | drawers |
| Erro provider | `format_provider_failure` | — | drawers |
| Ollama | `run_ollama` mock | smoke `@slow` | mock route |
| Docker compose | — | `docker compose config` | — |

---

## CI recomendado (futuro)

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

## Resumo: comece por aqui

1. **Hoje:** rodar `pip install -r requirements-dev.txt` e `npm run test:all` — baseline verde.
2. **Semana 1:** Fase 1 — FastAPI com paridade total (testes de integração duplicados).
3. **Semana 2:** Fase 2 — Ollama no Docker + smoke test.
4. **Depois:** Fase 3 (indexação) — maior impacto na qualidade narrativa local.

Nunca pule fase sem testes verdes da fase anterior.