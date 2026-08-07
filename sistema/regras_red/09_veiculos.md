---
version: 1.0.0
status: stable
last_updated: 2026-08-07
source: Cyberpunk RED core (resumo operacional) + ficha The Mule
---

# Veículos — condução, perseguição, combate

**Pré-requisito:** [01_core.md](01_core.md) · [02_combate.md](02_combate.md) · [04_armas.md](04_armas.md).  
**The Mule (SoT de stats):** [vehicle - the_mule.md](../../fichas/vehicle%20-%20the_mule.md).  
**Pilota / equipe:** [nomad - lena_valk_kane.md](../../fichas/nomad%20-%20lena_valk_kane.md) · F08 Valk + Mule.

---

## 1. Stats veiculares (o que ler na ficha)

| Campo | Significado |
| ----- | ----------- |
| **SDP** | “HP” do veículo — destruído / imobilizado em 0 |
| **SP** | Armadura do chassi |
| **Speed** | Velocidade máxima / relativa em perseguição |
| **Handling / Manobrabilidade** | Mods em testes de Drive |
| **Seats / cargo** | Capacidade |

Dano ao veículo: similar a [03](03_ferimentos.md) — dano − SP → SDP; ablação se aplicável (resumo core).

---

## 2. Condução

```text
Total = REF + Drive Land Vehicle + 1d10 + mods
```

| Situação | DV / resolução |
| -------- | -------------- |
| Estrada normal | Trivial — sem rolagem |
| Terreno ruim / chuva / fuga leve | DV 13–15 |
| Off-road Badlands sob fogo | DV 15–17 |
| Manobra extrema / Vanisher full | DV alto + trade-off Handling (ficha Mule) |

Skills de outros meios (Water / Air) só se a cena e a ficha tiverem.

---

## 3. Perseguição

1. Ambos os lados rolam Drive (ou um rola vs DV se o outro for “mook estático”).  
2. Comparar totais + vantagens de Speed.  
3. **The Mule — Vanisher:** bônus de velocidade com **penalidade de manobra** (valores na ficha do Mule).  
4. Contramedidas (fumaça, óleo, gás): teste do perseguidor ou DV extra — cargas na ficha Mule.  
5. Falha crítica: colisão, perda de controle, abandono da rota.

---

## 4. Colisão

- Impacto → dano a **SDP** (e possivelmente aos ocupantes — resumo core: BODY saves / dano).  
- Alvo peão vs van: peão sofre o pior.  
- Dois veículos: ambos testam / ambos tomam dano proporcional (narrar + números se a cena exigir).

---

## 5. Combate e veículos

| Situação | Resolução |
| -------- | --------- |
| Atirar **de** veículo em movimento | +DV ao atacante (MVP +2 a +4 conforme velocidade) |
| Atirar **no** veículo | Ataque vs chassi (pode ser DV fixo) ou hit location; dano → SP/SDP |
| Mount (pintle HMG, side GL) | Skill de arma ([04](04_armas.md)); ROF/dano da ficha do veículo |
| Arma oculta (MIAC-5) | Setup / revelar mount = tempo ou ação; munição **escassa** |
| Ocupante vs ocupante (CQB dentro) | Combate normal [02](02_combate.md) |

---

## 6. Nomad — Moto (ponte)

- Role Ability **Moto** / Family (core): bônus com veículos da família / pack — ver ranks na ficha da **Valk**.  
- Em dúvida: Valk + Mule = pacote tático (F08); bônus de Moto só se a ficha tiver rank listado.  
- **Não** aplicar bônus Nomad a Ryan por default (ele não é Nomad).

---

## 7. Bloco campanha — The Mule (resumo; SoT = ficha)

| Stat | Valor (ficha) |
| ---- | ------------- |
| SDP | 95 |
| SP | 20 |
| Speed | ~110 km/h normal; Vanisher modos +speed / −Handling |
| Config | 8x8, blindagem, run-flat |
| Armas | HMG teto · GL lateral · **MIAC-5** oculto |
| Equipe | **Valk** comanda; Ryan mantém/upgrades |

Anti-ID / Void List em jobs com Echo: ver ficha Mule + [echo_exposicao](../echo_exposicao.md).

**Projeto Reina bike:** [reina_byke_project.md](../../fichas/reina_byke_project.md) — **não canônico / não ativo** até o SoT dizer o contrário.

---

## Changelog

### 1.0.0 — 2026-08-07

- Drive, perseguição, colisão, combate veicular, Nomad ponte, Mule resumo.
