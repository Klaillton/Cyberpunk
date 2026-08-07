# Camada mecânica Cyberpunk RED — plano de implementação

**Status:** `approved`  
**Atualizado:** 2026-08-07  
**Arquivo canônico:** este (`plans/add-cyberpunk-red-mechanics.md`)  
**Substitui:** `plans/add_cyberpunk_mecanichs.md` (typo + conteúdo não faseado)

**Objetivo:** fortalecer a resolução mecânica (Cyberpunk RED) **sem retcon** da história; cobrir Roles da **crew real**; versionar regras; endurecer o fechamento de sessão **sobre** o Finalizar já existente.

**Dependências:** `base/Cyberpunk Red.pdf` (SoT RAW) · `fichas/` · `sistema/comandos_jogador.md` (Finalizar) · `logs/sessao_resumo_*`

**Cutoff proposto:** primeira sessão **após** merge da Fase 1 (MVP) — registrar em `fatos_duros` + `00_integridade_regras.md`.  
*(Se o merge ocorrer antes da 017, a 017 já usa a nova camada. Não reabrir combates 001–016.)*

---

## 1. Princípios (inegociáveis)

### 1.1 Passado ≠ futuro

```text
PASSADO → CANON CONSOLIDADO → NOVA RESOLUÇÃO MECÂNICA → FUTURO
```

Não re-rolar mortes, scavs, torres, jobs ou neutralizações já nos logs.

### 1.2 Anti-super-herói / anti-dice-spam

```text
ROLAR QUANDO IMPORTA.
NÃO ROLAR QUANDO NÃO IMPORTA.
```

- Ficha alta = **alta probabilidade**, não sucesso automático sob risco/oposição.
- Porta destrancada / rotina trivial = **sem** rolagem.

### 1.3 RAW > House Rule > Decisão provisória

- `sistema/regras_red/` = resumo operacional alinhado ao core book (citar, **não** copiar o livro inteiro).
- `sistema/house_rules/` = adaptações desta campanha (explícitas).
- Provisório de sessão → só vira house rule se o jogador confirmar no Finalizar.

### 1.4 Versionamento ≠ estado da campanha

| Camada | Muda quando… |
| ------ | ------------ |
| `regras_red/*` semver | A **regra** muda |
| Board / resumo / pack | A **ficção** muda |

Ryan tomar dano **não** gera v1.0.1 de `01_core.md`.

### 1.5 Não nerfar Ryan retroativamente

Competência + preparação + drones + vantagem tática → resultados excepcionais **legítimos**.  
Objetivo = integridade de decisões sob **risco real**.

---

## 2. Correções em relação ao rascunho antigo

| Rascunho (`mecanichs`) | Correção |
| ---------------------- | -------- |
| “67 Raffen Shiv” | **Não é fato do SoT.** Casos de teste = Inc. 001, Inc. 002 (~16), Torre 04/07, torre chrome 16–17/07, etc. |
| Pasta `registro/sessoes/` | **Não criar.** Usar `logs/sessao_resumo_NNN.md` + playbook Finalizar |
| Session Commit paralelo | **Estender** checklist do Finalizar (HP, SP/ablação, HL, inventário, ruleset version) |
| Lawman / Exec / Rockerboy prioritários | **Fora da crew** → stub opcional, não MVP |
| Enciclopédia RED de uma vez | **Fases** 0–5 |
| Motor Python d10 | Fora de escopo enquanto `motor/`/`api/` forem só artefatos locais |

---

## 3. Inventário de Roles (crew real)

| Personagem | Role | Prioridade mecânica |
| ---------- | ---- | ------------------- |
| Ryan | Techie (Maker) | **P0** |
| Valk | Nomad (Moto / Mule) | **P0** (veículo) |
| Reina, Jax | Solo | P1 |
| Stitch | Medtech | P1 (ferimentos) |
| Kaz | Fixer | P1 |
| Echo | Media | P1 (já há `echo_exposicao`) |
| Alex | Netrunner | P2 (NET denso) |
| — | Lawman / Exec / Rockerboy | **Não-MVP** |

---

## 4. O que já existe (não reinventar)

| Conceito | Onde |
| -------- | ---- |
| Fechamento de sessão | `[Finalizar sessão]` · `logs/sessao_resumo_*` · context pack · handoff |
| Rolar com risco (curto) | `sistema/diretrizes_narrador.md` §2 |
| Estado mundo | board, event_queue, heat, reputacao, economia |
| Fonte RAW | `base/Cyberpunk Red.pdf` (+ DLCs em `base/`) |

### Mapeamento Session Commit → projeto

```text
LOGS (sessao_resumo)     → eventos da sessão
SESSION COMMIT           → = Finalizar + matriz de ledgers (já existe)
CONTEXT PACK / HANDOFF   → NOW para boot
regras_red version       → campo novo no cabeçalho do resumo (Fase 1+)
```

---

## 5. Estrutura de arquivos alvo

```text
sistema/
├── regras_red/
│   ├── 00_integridade_regras.md   # hierarquia, cutoff, proibições
│   ├── 01_core.md                 # teste, DV, oposto, crítico, Luck, iniciativa
│   ├── 02_combate.md
│   ├── 03_ferimentos.md           # HP, SP, SW, Death Save, First Aid
│   ├── 04_armas.md                # resumo + link ficha/core
│   ├── 05_cyberware.md            # HL, instalação
│   ├── 06_skills.md
│   ├── 07_roles.md                # crew only + stub “outras”
│   ├── 08_techie.md               # Maker, drones, craft (prioridade campanha)
│   ├── 09_veiculos.md             # Mule, perseguição básica
│   ├── 10_netrunning.md
│   └── 11_referencia.md           # tabelas DV / atalhos
├── house_rules/
│   ├── README.md
│   └── regras_campanha.md         # stealth+drones, pack, etc.
└── versionamento_regras.md
```

Metadados no topo de cada módulo:

```markdown
---
version: 1.0.0
status: draft|stable
last_updated: YYYY-MM-DD
source: Cyberpunk RED core (resumo operacional)
---
```

---

## 6. Fases de implementação

| Fase | Status | Entrega | Paths principais |
| ---- | ------ | ------- | ---------------- |
| **0** | `done` | Convenção `plans/` + **este** plano | `plans/README.md`, este arquivo |
| **1 MVP** | `done` (2026-08-07) | Integridade + core + combate MVP + ferimentos + stealth/drones house + cutoff F18 + wire-up | `regras_red/00–03`, `house_rules/`, `fatos_duros`, `diretrizes_*`, `sessao_resumo_template`, Finalizar |
| **2** | pending | Combate + armas resumo + Techie/Maker + veículos (Mule) | `02`, `04`, `08`, `09` |
| **3** | pending | Roles crew restantes + cyberware/HL + eddies explícitos | `05–07`, patch `economia.md` |
| **4** | pending | Netrunning + referência | `10`, `11` |
| **5** | pending | Auditoria combates **canônicos** (OBSERVAÇÃO, não RETCON) + Finalizar com HP/SP/HL | relatório em `plans/` ou `logs/` |

### Critério de sucesso (MVP — Fase 1)

Para: *“Ryan tenta eliminar silenciosamente um inimigo consciente com risco real”*:

```text
Existe risco? → Skill? → Oposição? → Regra? → Mods? → Rolagem? → Resultado? → Consequência? → Narração
```

Sem rolagem para ação trivial. Canon pré-cutoff intacto.

### Fora de escopo (MVP)

- Reescrever incidentes com dados
- Engine Python de combate
- Lawman / Exec / Rockerboy
- Reimpressão integral do core book

---

## 7. Ordem de resolução (manter)

```text
1 INTENÇÃO → 2 AÇÃO → 3 RISCO → 4 REGRA → 5 FICHA → 6 MODS
→ 7 ROLAGEM → 8 RESULTADO → 9 CONSEQUÊNCIA → 10 ESTADO → 11 NARRAÇÃO
```

Narrar **depois** de resolver. Não inventar rolagem para justificar desfecho já decidido.

---

## 8. Stealth (prioridade campanha)

Distinguir:

```text
Não ser percebido  ≠  Invisível por default
```

Quando houver risco relevante, considerar: skill, ambiente, percepção inimiga, distância, luz, cobertura, ruído, sensores, drones, falha e alarme.

House rules de drones (Warden F03, Vespas, Condor/Corujas F16) ficam em `house_rules/regras_campanha.md`, não misturadas como se fossem RAW silencioso.

---

## 9. Auditoria inicial (Fase 5 — observação)

Perguntas (sem retcon):

1. Quais combates documentados teriam exigido rolagem sob a nova camada?
2. Quais foram legítimos por vantagem decisiva / preparação?
3. Quais skills/roles da crew ainda são só narrativa?
4. A ficha de Ryan (Maker, drones, SP) está coerente com o core?

Formato de saída:

```text
OBSERVAÇÃO: …   |   HISTÓRICO: permanece canon.
```

---

## 10. Checklist Finalizar (a adicionar na Fase 1)

Além do playbook atual, avaliar:

```text
[ ] HP / ferimentos / Seriously Wounded
[ ] SP / ablação de armadura
[ ] Humanity / HL se chrome mudou
[ ] Inventário tático / munição relevante
[ ] Ruleset version usada na sessão (ex. Ruleset: 1.0.0)
[ ] Decisões provisórias vs house rules candidatas
```

---

## 11. Versionamento

- Semver `MAJOR.MINOR.PATCH` em cada módulo.
- `sistema/versionamento_regras.md` = tabela central.
- Changelog curto por arquivo (o que mudou e por quê).
- Sessões antigas permanecem válidas sob a versão vigente **na época**.

---

## 12. Próximo passo de execução

1. ~~Pull sessão 016~~ (feito: `29aac0e`)
2. ~~Fase 0: `plans/README` + este plano~~
3. ~~Fase 1 MVP: `regras_red/00–03` + house_rules + F18 + wire-up~~
4. **Próximo (quando pedir):** Fase 2 — armas resumo, Techie/Maker, veículos (Mule)

---

## Referências

- Core: `base/Cyberpunk Red.pdf`
- Boot: `sistema/diretrizes_ia.md` · `sistema/diretrizes_narrador.md`
- Finalizar: `sistema/comandos_jogador.md` § C
- Estado: `logs/context_pack_atual.md` (NOW pós-016: 23/07 tarde · saída 24/07 · próxima **017**)
- Índice de planos: [README.md](README.md)
