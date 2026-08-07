# Fase 2 — Combate expandido, armas, Techie/Maker, veículos

**Status:** pronto para implementação  
**Base:** [plans/add-cyberpunk-red-mechanics.md](C:\workspace\Cyberpunk\plans\add-cyberpunk-red-mechanics.md)  
**Ruleset alvo:** **1.1.0** (MINOR — novos módulos + expansão de `02`)  
**Pré-requisito:** Fase 1 done (`regras_red/00–03` v1.0.0, F18 cutoff 017+)  
**Não-escopo desta fase:** cyberware/HL detalhado (Fase 3), roles completas Solo/Fixer/Media (Fase 3), netrunning (Fase 4), retcon 001–016, Python engine

---

## Objetivo

Dar ao narrador ferramentas para:

1. **Combate além do 1v1** — autofire/ROF básico, múltiplos alvos, ponte para combate veicular
2. **Armas** — categorias, ROF, alcance, dano genérico + links para Ghostwire / Mule
3. **Techie (Maker)** — Role Ability, inventar/fabricar/reparar/melhorar, drones como produto
4. **Veículos** — SDP/SP, Drive, perseguição, colisão, **The Mule** + Valk (Nomad)

Critério de sucesso (Fase 2):

| Cena                                          | Pipeline                                         |
| --------------------------------------------- | ------------------------------------------------ |
| Rajada / ROF > 1                              | Usar `02` + `04` sem inventar ROF                |
| Ryan fabrica peça / repara Mule / itera drone | `08_techie` + ficha Maker + economia se material |
| Perseguição no Mule / colisão / HMG de teto   | `09_veiculos` + ficha Mule + Drive de Valk       |
| Continua stealth kill 1 alvo                  | Ainda funciona com `01–03` (regressão)           |

---

## Entregáveis

### A. Novos módulos

| Arquivo                             | Conteúdo (resumo operacional + citação core)                                                                                                                                                                                                                                                                                                                                              |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `sistema/regras_red/04_armas.md`    | Tipos (Pistol, SMG, Assault, Shotgun, Sniper, Melee, Thrown, Exotic); **ROF**; alcance (Close / Medium / Long / Extreme como DV mods); munição; qualidade/excelente; ponte “dano → 03”; tabela **atalho** de DVs; **não** copiar book de armas inteiro — “default: ficha do personagem / core p.XXX”                                                                                      |
| `sistema/regras_red/08_techie.md`   | **Maker** Rank (Expertise / Invention / Fabrication / Upgrade / Jury Rig — nomes alinhados ao core e à ficha Ryan); tempo/custo/materiais (faixas, link `economia.md`); reparo vs upgrade vs invention; **drones** (criar, manter, controlar sob pressão → 01/02); Field repairs em combate; o que **não** inventar (stats de arma nova sem Finalizar)                                    |
| `sistema/regras_red/09_veiculos.md` | SDP, SP veicular, Speed, Handling; skill **Drive Land Vehicle** (e Water/Air se surgir); perseguição (opostos Drive); colisão (dano SDP); combate **do** veículo (mounts: pintle/side/hidden); ponte Nomad **Moto** (Family/rank — resumo + “ver ficha Valk”); **bloco The Mule** (SDP 95, SP 20, Vanisher, MIAC-5, HMG) com link `fichas/vehicle - the_mule.md` — sem reescrever a ficha |

### B. Expandir existente

| Arquivo                               | De → Para         | Mudança                                                                                                                                                                                                                                      |
| ------------------------------------- | ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `regras_red/02_combate.md`            | 1.0.0 → **1.1.0** | Seções: **ROF / autofire** (resumo core: múltiplos tiros, penalidades); **suppressive** (1 parágrafo); **múltiplos combatentes** (iniciativa, mooks em grupo); **melee reach** curto; link `04` e `09`; remover “adiado Fase 2” desses itens |
| `house_rules/regras_campanha.md`      | 1.0.0 → **1.1.0** | Craft no Pack (oficina Tio Gringo = bônus de ficção, não +5 mágico); drones Condor/Corujas em **combate veicular/alerta** (não loadout bolso); craft consome estoque `economia` se P-item                                                    |
| `regras_red/00_integridade_regras.md` | 1.0.0 → **1.1.0** | Lista de módulos + link 04/08/09; ruleset 1.1.0                                                                                                                                                                                              |
| `sistema/versionamento_regras.md`     | —                 | Ruleset **1.1.0**; linhas novos módulos; changelog                                                                                                                                                                                           |

### C. Wire-up (leve)

| Arquivo                                  | Mudança                                                                                                                |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `sistema/registro_arquivos.md`           | Linhas: armas → 04; Maker/craft → 08; veículos/Mule → 09; “perseguição”                                                |
| `sistema/diretrizes_narrador.md`         | §2: links 04/08/09 se combate/craft/veículo                                                                            |
| `sistema/fatos_duros.md`                 | Opcional: **F18** texto “v1.0.0+” ou nota “ruleset atual ver versionamento” (manter cutoff 017; **não** mudar 001–016) |
| `logs/context_pack_atual.md`             | 1 linha: Ruleset **1.1.0** (se 017+ já em vigor)                                                                       |
| `plans/add-cyberpunk-red-mechanics.md`   | Fase 2 → `done`                                                                                                        |
| `plans/README.md`                        | Status atualizado                                                                                                      |
| `fichas/techie - ryan_wireghost_voss.md` | Link no bloco Maker → `08_techie.md` (1 linha)                                                                         |
| `fichas/vehicle - the_mule.md`           | Link mecânica → `09_veiculos.md` (1 linha)                                                                             |
| `fichas/nomad - lena_valk_kane.md`       | Link Drive/Moto → `09` se couber 1 linha                                                                               |

---

## Conteúdo — decisões de design

### 04 Armas (MVP de tabela, não catálogo)

```text
Ataque → skill da categoria (Handgun, Shoulder Arms, …)
ROF = tiros por ação (ficha/core)
Alcance: Close / Medium / Long / Extreme → mods de DV (resumo)
Dano: da ficha da arma; se só tipo genérico → faixa core
```

| Categoria           | Skill típica     | Notas campanha                          |
| ------------------- | ---------------- | --------------------------------------- |
| Pistol / SMG        | Handgun          | Ghostwire pistols se na ficha           |
| Assault / LMG / HMG | Shoulder Arms    | Mule HMG                                |
| Shotgun             | Shoulder Arms    |                                         |
| Sniper / DMR        | Shoulder Arms    | Phantom Mk.II                           |
| Melee               | Melee / Brawling | Shadowblades etc.                       |
| Thrown              | Athletics        |                                         |
| Cannon / Exótico    | Situacional      | MIAC-5: DV alto, ROF 1, munição escassa |

**House:** armas **custom Techie** (Ghostwire) usam stats da ficha; se faltar número, **não inventar** — DV 15 e “anotar no Finalizar”.

### 08 Techie / Maker

Alinhar à ficha Ryan (Maker, Invention 1, Upgrade Expertise 3, Basic Tech 7, Electronics 7):

| Capacidade              | Uso em mesa                                                                                 |
| ----------------------- | ------------------------------------------------------------------------------------------- |
| Fabrication / Workshop  | Produzir item com tempo + materiais (faixas: horas / dias / multi-sessão)                   |
| Invention               | Item **novo** (drone, gimmick) — DV alto + protótipo + risco de falha                       |
| Upgrade                 | Melhorar gear existente (arma, Mule, drone)                                                 |
| Jury Rig / Field repair | Reparo rápido sob pressão (teste, duração limitada)                                         |
| Drones                  | Stats = ficha; controle sob fogo = teste; craft enxame só quando SoT tiver protótipo (E017) |

**Integração economia:** se consumir chrome/chapas/P003 → atualizar `economia.md` no Finalizar.  
**Não** dar arma 10d6 de graça sem custo/tempo.

### 09 Veículos + Mule

| Conceito                | Resolução                                                                                  |
| ----------------------- | ------------------------------------------------------------------------------------------ |
| Pilotar sob pressão     | Drive Land Vehicle + REF + 1d10 vs DV terreno / oposto perseguição                         |
| Perseguição             | Opostos Drive; Vanisher = mods de speed com trade-off Handling (ficha Mule)                |
| Colisão                 | Dano a SDP; SP veicular; ocupantes podem tomar dano (resumo core)                          |
| Atirar de/para veículo  | Mods DV (movimento, cobertura chassi) + skill arma                                         |
| Mount HMG / GL / MIAC-5 | ROF/dano da ficha Mule; munição limitada; MIAC oculto = setup                              |
| Nomad Moto              | Rank Moto da ficha Valk = bônus Family / vehicle conforme core (1 parágrafo + “ver ficha”) |

### 02 Combate 1.1.0

- **Autofire / ROF:** se ROF ≥ 2, resumo: múltiplos ataques ou regra de autofire do core em 1 parágrafo + “detalhe no livro”.
- **Grupo:** mooks compartilham iniciativa ou act as group; PC age no init próprio.
- **Suppressive:** ação que impõe DV/penalidade a quem se expõe (1 parágrafo).
- Links explícitos para 04 e 09.

---

## Versionamento

| Item                   | Versão                                                                          |
| ---------------------- | ------------------------------------------------------------------------------- |
| Ruleset campanha       | **1.1.0**                                                                       |
| `00`, `02`, house      | bump **1.1.0**                                                                  |
| `01`, `03`             | permanecem **1.0.0** (sem mudança obrigatória; opcional 1 linha “ver 04/08/09”) |
| Novos `04`, `08`, `09` | **1.0.0** (primeira versão do módulo)                                           |

Cabeçalho de resumo de sessão: `Ruleset: 1.1.0`.

---

## Ordem de implementação

```text
1. 04_armas.md
2. 02_combate.md → 1.1.0 (ROF, grupo, links)
3. 08_techie.md
4. 09_veiculos.md (+ bloco Mule)
5. house_rules 1.1.0 + 00_integridade 1.1.0
6. versionamento_regras.md
7. Wire-up registro, narrador, fichas (links), context pack F18/ruleset, plans
```

---

## Definition of Done

| #   | Critério                                                                  |
| --- | ------------------------------------------------------------------------- |
| 1   | `04`, `08`, `09` existem e linkam core/fichas                             |
| 2   | `02` documenta ROF/grupo e aponta 04/09                                   |
| 3   | Ruleset **1.1.0** no versionamento                                        |
| 4   | registro_arquivos e planos atualizados                                    |
| 5   | Smoke: perseguição Mule + HMG; craft com Maker; autofire sem inventar ROF |
| 6   | Sem retcon 001–016; sem módulos 05–07/10–11                               |

---

## Fora de escopo (explícito)

- Medicine / Operator / Credibility / Interface completos
- Humanity Loss tabelas longas
- Reina bike como veículo canônico (projeto futuro — no máx. 1 linha “não ativo”)
- Autofire opcional hyper-detailed / every ROF chart from book
- Commit/push sem pedido do usuário

---

## Riscos

| Risco                        | Mitigação                                             |
| ---------------------------- | ----------------------------------------------------- |
| 08 vira homebrew de craft OP | Tempos/DV altos; materiais; Finalizar                 |
| 09 reescreve ficha Mule      | Só resumo + link; stats ficam na ficha                |
| 04 vira wiki de armas        | Categorias + “usar ficha”; exemplos Ghostwire/Mule só |
| Tier-0 engorda               | Continuar **sob demanda**                             |

---

## Após aprovação

Implementar na ordem acima; ao terminar, marcar Fase 2 `done` em `plans/add-cyberpunk-red-mechanics.md`.
