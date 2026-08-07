---
version: 1.0.0
status: stable
last_updated: 2026-08-07
source: Cyberpunk RED core (resumo operacional)
---

# Netrunning — MVP de mesa

**Pré-requisito:** [01_core.md](01_core.md) · [07_roles.md](07_roles.md) (Interface).  
**Netrunner da crew:** [alex_specter_kane.md](../../fichas/netrunner%20-%20alex_specter_kane.md).  
**Ryan:** Techie — suporte meat/tech, **não** Interface.  
Em dúvida de arquitetura/ICE full → `base/Cyberpunk Red.pdf`.

**Escopo MVP:** rodar uma infiltração NET em job sem copiar o livro inteiro.  
**Fora:** simulação de mega-corp full, todos os programas, black ICE catalog completo.

---

## 1. Quem age na NET

| Papel | Regra |
| ----- | ----- |
| **Netrunner** (Alex) | Role Ability **Interface** = NET Actions por turno (rank na ficha ≈ 6–8 → **3–4** actions) |
| Outro PC | Só se tiver Interface; senão meatspace / support |
| Techie | Desligar power, jam, hardware — testes TECH, não NET Actions |

---

## 2. Conceitos

| Termo | Uso em mesa |
| ----- | ----------- |
| **NET Architecture** | Mapa de níveis/nós do alvo (quanto mais profundo, mais perigoso) |
| **Interface** | Total típico: INT ou TECH + Interface rank + 1d10 (seguir core/ficha) |
| **Cyberdeck** | Slots de programas; sem deck = sem full run |
| **Programs** | Sword, Shield, Worm, Pathfinder, etc. — da ficha/deck |
| **ICE** | Defesa do sistema; impede, alarma ou fere |
| **Meatspace** | Corpo vulnerável; aliados cobrem |

---

## 3. Fluxo de uma run (MVP)

```text
1. Objetivo (dado, abrir porta, câmeras, copiar arquivo)
2. Jack in (precisa acesso físico ou wireless autorizado pela ficção)
3. Por turno NET:
   a. Gastar NET Actions (Interface)
   b. Cada ação: Interface + 1d10 vs DV do nó/ICE ou oposto
   c. Usar 1 program se a ação exigir
4. ICE reage se falha / alarme / black ICE
5. Jack out (seguro ou forçado)
6. Consequências meat (alarme, traço, Heat)
```

**DV de referência (nós):**

| Dificuldade | DV | Exemplo |
| ----------- | -- | ------- |
| Rotina / low security | 13 | Câmera de armazém |
| Profissional | 15–17 | Corp mid, hotel |
| Hardened | 21+ | Lab Biotechnica, vault |

---

## 4. Ações Interface (atalho — nomes core)

| Ação | Uso |
| ---- | --- |
| **Pathfinder / Scanner** | Mapear níveis, achar caminho |
| **Eye-Dee** | Identificar arquivo/objeto digital |
| **Cloak / Slide** | Evitar detecção / deslizar por nó |
| **Control** | Câmeras, portas, drones do sistema (se o nó permitir) |
| **Backdoor / Virus** | Abrir caminho persistente, sabotagem |
| **Zap / Sword** | Atacar ICE ou programa inimigo |
| **DeckKRASH / etc.** | Conforme programa no deck |

Sem o programa listado no deck: ação só se o core permitir “bare Interface” — senão DV pior ou impossível.

---

## 5. ICE (resumo)

| Tipo (conceitual) | Efeito MVP |
| ----------------- | ---------- |
| White / barreira | Bloqueia; pode alarmar se falhar |
| Gray | Drena, atrasa, força retrace |
| Black | Dano ao netrunner (HP/mental) ou stun — **perigoso** |

Resolução típica: Interface vs DV da ICE **ou** programa de ataque vs defesa da ICE.  
**Falha crítica / 1 no d10:** alarme, trace, dano, jack-out forçado.

---

## 6. Tempo e meatspace

- Enquanto jacked: corpo imóvel / vulnerável — aliados em [02_combate](02_combate.md).  
- Alarme NET → segurança meat em X rounds (narrar 1–3 se não houver timer).  
- **Heat:** vazamento / corp trace → [heat.md](../../heat.md) se público ou investigável.  
- Echo: não filmar rosto do netrunner em op ([echo_exposicao](../echo_exposicao.md)).

---

## 7. Alex — defaults de mesa

| Campo | Valor (ficha / resumo) |
| ----- | ---------------------- |
| Interface | 6–8 → **3–4 NET Actions** |
| Deck | Standard+ / 7+ slots (sugerido) |
| Programs | Sword, DeckKRASH, Worm, Shield, … (completar no Finalizar se job exigir lista exata) |
| Meat | Handgun/SMG leve, SP 11 |

Se o job precisar de programa específico e a ficha não listar: **DV +2** ou “Alex não tem — Ryan/Kaz providenciam downtime”.

---

## 8. Ryan e a NET

- Pode **preparar** hardware, antenas, jam analógico, cortar cabo.  
- **Não** gasta Interface.  
- Drones + Electronic Security = suporte à run ([08_techie](08_techie.md)).

---

## 9. O que registrar

- Sucesso/falha do objetivo digital  
- Alarme / Heat  
- Dano a Alex (HP/HL se black ICE)  
- Programas consumidos / deck danificado  
- `Ruleset: 1.3.0` no resumo se NET foi central  

---

## Changelog

### 1.0.0 — 2026-08-07

- MVP: Interface, fluxo de run, ICE resumo, meatspace, Alex defaults.
