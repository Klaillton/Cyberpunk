# Status do Projeto — Motor Narrativo Solo

> **Atualizado:** 09 de Julho de 2026  
> **Branch de referência:** `feat/narracao-solo-mvp`  
> **Documentos irmãos:** [plano_implementacao_e_testes.md](./plano_implementacao_e_testes.md) · [especificacao_tecnica_v1.1.md](./especificacao_tecnica_v1.1.md)

---

## Resumo executivo

| Item | Valor |
|------|-------|
| **Fase atual** | **Sprint B concluída** |
| **Testes** | 107 pytest (+2 slow deselected) · 19 e2e Playwright |
| **Provider padrão** | Ollama `llama3.1:8b` no laptop |
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
| 5.1 | MVP sessão solo (ver abaixo) | ✅ |

### Fase 5.1 — MVP sessão solo (não estava no plano original)

Entregue na branch atual, além do escopo das Fases 0–5:

| Entrega | Arquivos principais |
|---------|---------------------|
| Canais **Mestre** e **Sistema** | `api/routers/message.py`, prompts em `scripts/narracao_engine.py` |
| **Brief** da campanha | `motor/brief_service.py`, `GET /api/brief` |
| Comandos de **resumo de sessão** | `motor/session_command_handler.py` |
| Parser jogador **ação / fala / beat** | `motor/player_message.py`, `frontend/app.js` |
| Histórico no chat (narração, mestre, sistema) | `frontend/app.js`, `api/schemas.py` |
| Contexto inteligente Mestre/Sistema | `select_context_files`, índice de fichas |
| Filtro de templates na indexação | `motor/markdown/campaign_paths.py` |
| Menu sidebar por grupos | `frontend/app.js`, `styles.css` |

---

## Em andamento / próximo

### Sprint A — Qualidade do turno ✅ concluída

| # | Item | Status | Notas |
|---|------|--------|-------|
| A1 | FAISS + EntityResolver no contexto | ✅ | `motor/context_service.py` |
| A2 | ProviderRouter no hot path | ✅ | `motor/narration.generate_turn` |
| A3 | ResponseQualityGate + retry (máx. 1) | ✅ | Correção local ou cloud fallback |
| A4 | Tabela `provider_routing_log` | ✅ | migration `003_*.sql` + `RoutingLogStore` |
| A5 | Metadados na API (`routing_decision`, `quality_*`) | ✅ | `MessageResponse` estendido |
| A6 | Quality gate reconhece NPCs do board/fichas | ✅ | `quality_gate.py` |

### Sprint B — UX e canais ✅ concluída

| # | Item | Status | Notas |
|---|------|--------|-------|
| B1 | UPDATE_PROPOSALS no canal Sistema (`channel == "sistema"`) | ✅ | `message.py` + `test_message_router.py` |
| B2 | E2E canal Sistema + resumo de sessão + meta qualidade | ✅ | `chat.spec.js`, `session-summary.spec.js` |
| B3 | UI routing preview | ✅ | drawer `Roteamento` + `routing-preview.spec.js` |
| B4 | CI GitHub Actions | ✅ | `.github/workflows/test.yml` |

### Sprint C — Infra opcional (Pi)

| # | Item | Status |
|---|------|--------|
| C1 | Validar `docker-compose.pi.yml` em ARM | ⬜ Adiado |
| C2 | Script sync Pi ↔ laptop | ⬜ Adiado |
| C3 | systemd unit | ⬜ Adiado |

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
| `migrate_legacy` → pasta `campanha/` | ⏸ Adiado (layout legado na raiz funciona) |
| Endpoints `/api/scene`, `/api/world`, `/api/timeline` | ⏸ Baixa prioridade |

---

## Decisão: Raspberry Pi

### Papel original (spec v1.1)

O Pi seria um **hub de estado 24/7** — sem LLM:

- `campanha/` (git/rsync)
- `data/motor.db` leve
- API read-only opcional (ficha, journal)
- Laptop assume Ollama + FAISS + sessão

### Hardware disponível (documentado)

| Dispositivo | Papel ideal | LLM 7–8B |
|-------------|-------------|----------|
| **Laptop** (i7-12650H, 64 GB, **RTX 4070**) | Sessão completa: motor + Ollama + embeddings | ✅ GPU |
| **Raspberry Pi 4 (8 GB)** | API leve, sync, estado | ❌ impraticável |
| **GitHub** | Source of truth remoto | — |
| **Cloud** (Grok etc.) | Fallback via ProviderRouter | ✅ por token |

### Recomendação (Jul/2026)

**Não descartar o Pi do projeto, mas adiar a Fase 6 (Sprint C) indefinidamente.**

| Abordagem | Veredito |
|-----------|----------|
| **Laptop-only + Git** (atual) | ✅ **Padrão** — cobre 100% do uso solo: sessão, indexação, Ollama na GPU |
| **Pi como hub 24/7** | ⏸ **Opcional** — só vale se houver necessidade concreta de acessar ficha/journal/API **sem ligar o laptop** |
| **Pi rodando LLM** | ❌ **Descartado** — 8 GB RAM não sustenta `llama3.1:8b` com qualidade |
| **Azure/AKS** | ❌ **Fora de escopo** para campanha solo — custo e complexidade sem ganho para 1 jogador |

### Vantagens reais do Pi (quando faria sentido)

1. **Disponibilidade LAN** — consultar ficha/NPC/journal de tablet/celular na rede local com laptop desligado.
2. **Âncora física do estado** — Pi sempre no mesmo IP, volume `motor_data` montado, menos “esqueci de dar pull”.
3. **Baixo consumo** — manter índice SQLite + API read-only 24/7 sem manter RTX/laptop ligados.

### Por que adiar (não implementar agora)

1. **GitHub já é o hub de sync** — `git pull` antes da sessão resolve canon remoto.
2. **Complexidade extra** — script bidirecional Pi↔laptop, drift de `data/motor.db`, systemd, ARM builds.
3. **Sessão exige laptop de qualquer forma** — Ollama na 4070 é o gargalo; Pi não substitui isso.
4. **Scaffold existe** (`docker-compose.pi.yml`) — retomar quando houver requisito explícito de acesso 24/7.

### Alternativa mais simples que o Pi

Se o objetivo for só **backup/sync**, priorizar:

```text
GitHub (canon)  →  git pull no laptop  →  sessão  →  commit/push pós-sessão
```

Opcional depois: **GitHub Actions CI** (Sprint B4) — mais valor imediato que Pi.

---

## Comandos úteis

```bash
npm run test:unit          # 107 pytest
npm run test:e2e           # 19 Playwright
npm run test:all           # gate completo
npm run test:slow          # smoke Ollama real
npm run index:rebuild      # SQLite + FAISS

python scripts/narracao_api.py   # API local :8787
```

---

## Histórico de atualizações deste arquivo

| Data | Mudança |
|------|---------|
| 2026-07-09 | Criação: status pós-Fase 5, Fase 5.1, decisão Pi adiado, backlog Sprints A–C |
| 2026-07-09 | Sprint A: ContextService, TurnOrchestrator, routing log, API metadata |
| 2026-07-09 | Sprint B: ingest Sistema, e2e canais/resumo/qualidade, CI, meta UI |
| 2026-07-09 | B3: drawer Roteamento (routing preview), e2e estável workers:1 |