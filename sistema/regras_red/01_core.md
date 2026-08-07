---
version: 1.0.0
status: stable
last_updated: 2026-08-07
source: Cyberpunk RED core (resumo operacional)
---

# Core — testes, DV, opostos, Luck

**Pré-requisito:** [00_integridade_regras.md](00_integridade_regras.md).  
Em dúvida de edge case → `base/Cyberpunk Red.pdf`.

---

## 1. Quando rolar

| Situação | Resolver |
| -------- | -------- |
| Trivial, sem risco, resultado óbvio | **Sem** rolagem |
| Habilidoso mas **seguro** (sem oposição, sem falha interessante) | Narrativo OK |
| Risco, oposição, ou consequência grave se falhar | **Rolagem** (ou oposto) |

```text
ROLAR QUANDO IMPORTA.
NÃO ROLAR QUANDO NÃO IMPORTA.
```

Ficha alta = **maior chance**, não isenção de teste sob risco.

---

## 2. Fórmula básica

```text
Total = STAT + Skill + 1d10 [+ modificadores]
```

- **Vs DV:** sucesso se Total ≥ DV.  
- **Oposto:** ambos rolam (ou um rola vs total estático se core indicar); **maior total vence**.  
- **Empate em oposto (MVP):** vence o **defensor** / status quo (alvo não é enganado, não é atingido em Evasion, etc.), salvo regra específica mais clara no core.

### Apresentação obrigatória (narrador)

Sempre que rolar, mostrar de forma legível:

1. Skill (e STAT)  
2. d10  
3. Mods (cada um justificado)  
4. **Total**  
5. DV **ou** total oposto  
6. Sucesso / falha / crítico / fumble  
7. Consequência em 1 frase  

---

## 3. DV de referência (atalho)

| DV | Rótulo (core) | Uso típico |
| -- | ------------- | ---------- |
| 9 | Everyday | Rotina sob leve pressão |
| 13 | Challenging | Requer treino |
| 15 | Difficult | Difícil para leigos |
| 17 | Professional | Nível profissional |
| 21 | Heroic | Heroico / elite |
| 24 | Incredible | Quase impossível |
| 29 | Legendary | Lendário |

Escolher DV pela **ficção** (dificuldade real), não para “equilibrar drama”.

---

## 4. d10 especial

| Face | Efeito (resumo core) |
| ---- | -------------------- |
| **10** | Crítico: rolar **+1d10** e somar (pode explodir de novo se o core/mesa usar explode em 10) |
| **1** | Fumble: rolar **1d10** e **subtrair** do total (piora o resultado) |

Detalhes de fumble em combate (arma trava, etc.) → core; no MVP narrar falha **significativa** alinhada ao total final.

---

## 5. Luck

- Gastar pontos de **Luck** da ficha **antes ou conforme core** para melhorar a rolagem (+1 por ponto gasto é a regra prática RED).  
- Luck gasta **não volta** até recovery de sessão/regra de recovery do core.  
- Anotar gasto no resumo se relevante.

---

## 6. Iniciativa

Quando a ordem de ações importar:

```text
Iniciativa = REF + 1d10  (+ mods se core/gear)
```

Maior age primeiro. Empate: maior REF; se empatar de novo, rolar de novo ou PC primeiro (escolher e ser consistente na cena).

---

## 7. Skills sem valor na ficha

Se a ficha não listar a Skill: usar **STAT + 1d10** (sem skill) **ou** default do core para untrained — no MVP, **STAT + 1d10** e declarar “sem skill”. Preferir completar a ficha depois (Fase 5).

---

## 8. Pipeline rápido (IA)

```text
Há risco/oposição/custo grave?
  NÃO → narrar
  SIM → STAT+Skill+1d10 vs DV/oposto → resultado → consequência → narrar
```

Stealth e drones: [house_rules/regras_campanha.md](../house_rules/regras_campanha.md).  
Combate: [02_combate.md](02_combate.md).  
Dano: [03_ferimentos.md](03_ferimentos.md).

---

## Changelog

### 1.0.0 — 2026-08-07

- MVP core: quando rolar, fórmula, DV, opostos, crítico/fumble, Luck, iniciativa.
