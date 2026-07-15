# Status do Projeto — Motor Narrativo Solo

> **Atualizado:** 15 de Julho de 2026  
> **Branch de referência:** `feat/narracao-solo-mvp`  
> **Documentos irmãos:** [plano_implementacao_e_testes.md](./plano_implementacao_e_testes.md) · [especificacao_tecnica_v1.1.md](./especificacao_tecnica_v1.1.md)

---

## Resumo executivo

| Item | Valor |
|------|-------|
| **Fase atual** | **Sprint E concluída** (jogar estável) |
| **Testes** | 160 pytest (+2 slow deselected) · 19 e2e Playwright |
| **Provider padrão** | Ollama local (`llama3.1:8b` perfil estável) |
| **Perfis Ollama** | `run-narracao-stable-local.ps1` (8B, diário) · `run-narracao-max-local.ps1` (14B, cenas críticas) |
| **Canon de estado** | Markdown + Git · SQLite/FAISS como índice derivado |
| **Topologia em uso** | **Laptop-only** (`docker-compose.yml` ou `narracao_api.py` local) |
| **Topologia Pi** | **Adiada** — ver [Decisão: Raspberry Pi](#decisão-raspberry-pi) |

---

## Fases concluídas

| Fase | Nome | Done |
|------|------|------|
| 0 | Fundação (pytest, e2e, Docker, Ollama) | ✅ |
| 1 | Paridade FastAPI | ✅ |
| 2 | LLM local (Ollama) | ✅ |
| 3 | Indexação SQLite + FAISS | ✅ |
| 4 | ProviderRouter + Quality Gate (módulos + preview API) | ✅ |
| 5 | Updates assistidos (propostas + UI) | ✅ |
| 5.1 | MVP sessão solo (canais, brief, resumo, parser) | ✅ |

### Sprint A — Qualidade do turno ✅

FAISS no contexto, router + gate no hot path, `provider_routing_log`, metadados na API.

### Sprint B — UX e canais ✅

Ingest Sistema, e2e canais/resumo/qualidade, drawer Roteamento, CI GitHub Actions.

### Sprint D — Criação ficha CPR ✅

Wizard CPR Complete Package, API `character_creation`, fichas migradas, motor de validação.

### Sprint E — Jogar estável ✅

| # | Item | Notas |
|---|------|-------|
| E1 | Script `run-narracao-stable-local.ps1` (8B) | Turno alvo ~30–90s |
| E2 | Helpers Ollama compartilhados | `scripts/lib/OllamaBootstrap.ps1` |
| E3 | Preflight Ollama no startup da API | `api/main.py` |
| E4 | Aviso frontend se API `degraded` | `buildOllamaHealthWarning` |
| E5 | Quality gate relaxado (ação simples + diálogo standard) | `quality_gate.py` |
| E6 | Meta UI: rescue Grok só se provider real for grok | `app.js` |
| E7 | Rescue Grok bloqueado em `local_only` | `router.py` + scripts |
| E8 | Auto-start container Ollama se parado | `Ensure-OllamaDocker` |

---

## Em andamento / próximo

| Prioridade | Item | Status |
|------------|------|--------|
| — | Sprint C (Pi 24/7) | ⏸ Adiado |
| Baixa | Endpoints `/api/scene`, `/api/world`, `/api/timeline` | ⬜ |
| Baixa | `migrate_legacy` → pasta `campanha/` | ⏸ |

**Uso recomendado para sessão:**

```powershell
docker compose -f deploy/docker-compose.yml up -d ollama
. scripts/run-narracao-stable-local.ps1   # diário (8B)
# . scripts/run-narracao-max-local.ps1    # cenas críticas (14B)
```

---

## Lacunas vs DoD v1.1

| Critério | Status |
|----------|--------|
| Ollama local na narração | ✅ |
| `/api/routing/preview` auditável | ✅ |
| `rebuild_index` + `/api/search` | ✅ |
| IntegrityChecker no turno | ✅ |
| Updates só após `POST /api/save` | ✅ |
| Router + gate no **hot path** | ✅ |
| `provider_routing_log` | ✅ |
| Hybrid retry cloud logado | ✅ (quando `hybrid` + cloud habilitado) |
| Perfil estável 8B para jogar | ✅ |
| `migrate_legacy` → pasta `campanha/` | ⏸ Adiado |
| Endpoints `/api/scene`, `/api/world`, `/api/timeline` | ⏸ Baixa prioridade |

---

## Decisão: Markdown vs banco de dados

**Manter markdown como fonte de verdade** (`fichas/`, `board/`, `relacionamentos/`, journal).  
SQLite (`data/motor.db`) e FAISS permanecem **índices derivados** via `sync_engine`.  
Não migrar canon para DB relacional nesta fase — Git + editabilidade humana valem mais para campanha solo.

---

## Decisão: Raspberry Pi

**Adiar Sprint C indefinidamente.** Laptop-only + GitHub cobre 100% do uso solo.  
Retomar Pi só se precisar de API read-only 24/7 na LAN sem ligar o laptop.  
Detalhes históricos mantidos na spec v1.1; scaffold `docker-compose.pi.yml` existe.

---

## Comandos úteis

```bash
npm run test:unit          # 160 pytest (2 slow deselected)
npm run test:e2e           # 19 Playwright
npm run test:all           # gate completo
npm run test:slow          # smoke Ollama real
npm run index:rebuild      # SQLite + FAISS

pwsh -File scripts/run-narracao-stable-local.ps1   # sessão diária
pwsh -File scripts/run-narracao-max-local.ps1      # qualidade máxima
```

---

## Histórico de atualizações deste arquivo

| Data | Mudança |
|------|---------|
| 2026-07-09 | Criação: status pós-Fase 5, Fase 5.1, decisão Pi adiado |
| 2026-07-09 | Sprints A e B concluídas |
| 2026-07-15 | Sprint D CPR, Sprint E jogar estável, perfis Ollama 8B/14B, decisão markdown vs DB |