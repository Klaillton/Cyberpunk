---
version: 1.2.0
status: stable
last_updated: 2026-10-03
source: Cyberpunk RED core (resumo operacional)
---

# Cyberware e Humanity Loss (MVP)

**Pré-requisito:** [01_core.md](01_core.md) · ferimentos [03](03_ferimentos.md).  
**Ficha exemplo:** Ryan — chrome + HL total em [techie - ryan_wireghost_voss.md](../../fichas/techie%20-%20ryan_wireghost_voss.md).  
**Instalação:** Stitch (crew) ou Doc Moreau / ripper — [07_roles](07_roles.md) · [elisa_doc_moreau](../../fichas/npc/elisa_doc_moreau.md).

**Não** é catálogo do livro. Resolve instalação, HL, e como o chrome entra na jogada.

---

## 1. Humanidade

```text
Humanidade atual ≈ EMP × 10   (após HL acumulado — usar valor da ficha se listado)
```

| Conceito | Uso |
| -------- | --- |
| **HL** | Humanity Loss ao instalar / certos efeitos |
| **EMP** | Pode cair se HL for alto (core); anotar na ficha |
| **Cyberpsycose** | Limiar core; se atingir, cena de perda de controle (não pular) |

Ryan “não se importa com Humanity” = **ficção** — ainda registra HL ([house](../house_rules/regras_campanha.md)).

---

## 2. Instalação (pipeline)

```text
1. Item e slot (braço, neural, etc.)
2. Quem instala (Surgery / Medtech / ripper)
3. Teste se risco (falha = dano, HL extra, tempo)
4. Pagar HL (rolar ou usar valor da ficha/core)
5. Atualizar ficha: lista chrome + HL total + EMP se mudou
6. Finalizar
```

**Upgrade Expertise (Maker):** pode reduzir HL em implantes elegíveis (1d6 off — ficha Ryan rank 3) — [08_techie](08_techie.md).

---

## 3. HL — faixas (atalho)

| Categoria | HL típico (resumo) |
| --------- | ------------------ |
| Fashionware / cosmético leve | 0–1d6/2 |
| Neural básico (Link, plugs) | 1d6 – 2d6 |
| Optics / audio | 1d6 – 2d6 |
| Cyberlimb | 2d6+ |
| Speedware (Kerenzikov, etc.) | 2d6 – 3d6 |
| Armor implant (subdermal, skinweave) | 1d6 – 2d6 |

Usar **números da ficha/core** se existirem.

**Ryan (reconciliação SoT):**  
- **HL histórico 78** = pico/acumulado (dado cheio + Maker); **não** é HL em aberto.  
- **Humanidade atual 63/70** (EMP 7) = pós-**Doc Moreau**; residual ~7 (fragmentação; E011).  
- Chrome de combate **permanece**; Doc restaurou Humanidade o bastante para jogar, não “zerou o passado”.  
- Detalhe: [ficha Ryan](../../fichas/techie%20-%20ryan_wireghost_voss.md) § Humanidade e Cyberware.

---

## 4. Na jogada — número ou função

Duas camadas. As duas entram. Não são a mesma coisa.

| Camada | O que é | No dado |
| ------ | ------- | ------- |
| **Número** | Bônus ou cancelamento já escrito nesta tabela ou na ficha | Soma no total, uma vez, nomeado |
| **Função** | O que a peça faz na cena | Acontece. **Não** vira +1 |

**Livro não completa número.** Peça sem número aqui e sem número na ficha não ganha dado. A vantagem dela é a função. HL pago não vira +N.

### 4.1 Antes de fechar o total

1. Abrir o chrome **desta** ficha.
2. Somar cada **número** que casa com este teste.
3. Aplicar cada **função** que muda esta cena: informação, ordem, acesso, ou cancelar uma penalidade já escrita.
4. Se nada casa: declarar `chrome: nenhum neste teste`.

Na apresentação do [01](01_core.md), uma linha `Chrome:` com o número nomeado e a função usada, ou “nenhum neste teste”.

Função não autoriza sucesso automático sob risco. O teste continua. O chrome muda o que a pessoa pode perceber, fazer ou ignorar, e o número entra no total.

### 4.2 Peças da campanha

Quem não tem a peça não usa a linha. Texto da ficha que estreita a função vence esta tabela. Leo mal registra o Biomonitor. Reina não ganha dado de braço até a cena dizer.

| Peça | Número | Função |
| ---- | ------ | ------ |
| **Kerenzikov** | **+2** na Iniciativa e **+2** em cada teste cujo STAT é **REF**. Uma vez por teste. | Percebe o movimento nascer e pode agir antes de ele se completar. Fora de iniciativa formal, a narração dá essa antecipação. Se virar teste, o +2 entra nesse teste de REF. Não pula o teste quando há risco: a antecipação é quem começa, não o resultado. **Não** soma em Perception (INT) nem em Evasion (DEX). |
| **Pain Editor** | Enquanto ligado, **cancela o −2** de Seriously Wounded ([03](03_ferimentos.md)). | Não cura. HP, Death Save e ablação seguem. A dor não avisa. A janela é o trecho de cena em que ficou ligado, não o dia inteiro. Ao desligar, o −2 volta se ainda estiver SW. |
| **Neural Link** | nenhum | Liga a pessoa ao que a ficha nomear: veículo, arma smart, deck, agent. Sem o link, smart e jack não respondem. |
| **Interface Plugs** | nenhum | O plugue. Encaixa no veículo, no deck, na arma. |
| **Smartgun Link** | **+1** no ataque com arma smart e alvo marcado, se esse +1 **não** estiver já no WA da arma | Phantoms do Ryan: o +1 já está no WA. Não dobrar. Sem marcação, sem +1. |
| **Kiroshi / cybereye** | nenhum | O que a ficha listar: zoom, HUD, low-light, marcação, gravação, leitura. Entrega essa informação. Não soma Perception. |
| **Cyberaudio** | nenhum | O que a ficha listar: filtro, direção do som, voice stress, scrambler, gravação, dampening. Entrega o que ouviu. Não soma Human Perception. |
| **Cyberarm** | nenhum | A função escrita na ficha: ferramenta, pop-up, grip, garra, força. A ferramenta já está no braço. O teste de risco usa a skill normal. |
| **Biomonitor** | nenhum | Lê o próprio corpo. A pessoa sabe o estado (HP, SW) sem First Aid em si. Não cura. |
| **Grafted Muscle and Bone Lace** | **+2 BODY** (BODY da compra + 2). Não leva o BODY a 11 ou mais. HP, limiar de SW e Death Save usam esse BODY ([03](03_ferimentos.md)). | Músculo e osso mais densos. O +2 é o número. Não soma outra vez em Athletics ou Brawling. |
| **Reinforced Tendons** | nenhum | House. O nome é do 2077. Na mesa **não** é double jump. Arranque curto, salto e mudança de direção na mesma movimentação. MOVE e o dado de Athletics não mudam. |
| **Subdermal Armor / Skinweave** | o **SP** já escrito na ficha ou no loadout | Não somar de novo por cima desse SP. Sem SP escrito, a pele é reforçada na ficção e o SP de combate continua o da armadura vestida. |
| **Vault, pocket, fashionware** | nenhum em teste de skill | OPSEC (F19) ou o visual da ficha. Não entram no total. |

### 4.3 Quem tem Kerenzikov

Ryan, Valkirya, Reina, Jax. Alex não tem speedware.

Iniciativa é um teste. O tiro, a direção ou outro teste de REF é outro. Cada um recebe o seu +2. Os dois não se somam no mesmo total. Não é só a rolagem de iniciativa.

---

## 5. Registrar

| Mudou | Onde |
| ----- | ---- |
| Novo implante / HL | Ficha personagem |
| EMP | Ficha |
| Instalação por Stitch/Doc | Relacionamentos se drama |

---

## Changelog

### 1.2.0 — 2026-10-03

- Grafted Muscle and Bone Lace: +2 BODY, com teto. HP, SW e Death Save usam esse BODY. Reinforced Tendons continua sem dado e sem double jump. HL pago não vira bônus.

### 1.1.0 — 2026-10-03

- Chrome na jogada: número soma, função acontece. Kerenzikov é +2 (iniciativa e REF) e antecipa o movimento. Sem número novo para peça que a ficha não tinha.

### 1.0.0 — 2026-08-07

- Instalação, HL faixas, humanidade, link Maker/Stitch/Doc.
