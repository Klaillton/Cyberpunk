# Ambientação, opções e ganchos (RPG textual)

**Finalidade:** o jogador **não vê o mapa** — a narração tem de **mostrar o lugar** e **abrir ações**, sem matar ritmo nem virar wallpaper.  
**Complementa:** [motor_cena_1pager.md](motor_cena_1pager.md) · [arco_ativo.md](../board/arco_ativo.md) · [npc_agencia_cena.md](npc_agencia_cena.md)  
**Comandos:** `[Ambientar]` · `[O que eu vejo?]` · (opcional) `[Imagem do lugar]` — ver [comandos_jogador.md](comandos_jogador.md)

---

## 1. Princípio

| Precisa | Não precisa |
| ------- | ----------- |
| **Onde** estou + **como** chego/safo + **3–5 opções** legíveis | Parágrafo eterno de poesia a cada turno |
| **Mudança de local** = bloco AMBIENTE novo | Re-descrever o mesmo cânion em todo turno |
| **Ação depende do ambiente** = detalhes operacionais | Inventar landmark só para encher |

**RPG só texto:** se o PC não “vê”, não pode escolher. Ambientação é **ferramenta de agência**, não enfeite.

---

## 2. Bloco AMBIENTE (início de cena / local novo)

Usar em:

1. **Chegada** a local novo (N9 fecha viagem → este bloco).  
2. **Mudança** relevante (dia↔noite, entra no Mule, sobe o paredão, entra em NC).  
3. Comando `[Ambientar]` / `[O que eu vejo?]`.  
4. Quando a **próxima ação depende** de layout (cobertura, linha de visão, água, rota, heat).

**Não** repetir o bloco inteiro em turnos de diálogo íntimo no mesmo sítio — só **1 detalhe que mudou**.

### 2.1 Formato fixo (colar mentalmente)

```text
## AMBIENTE — <nome curto do local>
- Sentidos (3–5): luz, cheiro, som, temperatura, poeira/névoa
- Layout (o que o corpo entende): onde fica o Mule / fogo / água / paredão / estrada / horizonte
- Cobertura & risco: quem te vê, onde esconder, linha de fuga
- Recursos óbvios: água, lenha, sombra, sinal de rádio, trilha
- Pessoas na cena: posição relativa (1 linha cada)
- Opções no ar (3–5, sem menu rígido): o que dá para FAZER daqui
```

**Tamanho:** ~8–14 linhas. Depois disso: **gancho** (N6) ou fala de NPC.

### 2.2 Esqueleto de resposta (chegada / local novo)

```text
## AMBIENTE — …
(bloco §2.1)

[1 batida de mundo ou NPC se AGENDA pedir]

**Gancho:** fato + escolha implícita (não “o que você faz?” vazio)
```

### 2.3 Turnos seguintes no mesmo local

```text
[Delta ≥60%: fala NPC / resultado / tempo]
[0–2 linhas de ambiente SÓ se algo mudou: luz, vento, fogo, rádio]
[Gancho]
```

---

## 3. Opções sem menu de videogame

Não listar `A) B) C)` a menos que o jogador peça.  
Embutir opções no **layout** e no **gancho**:

| Ruim | Bom |
| ---- | --- |
| “O que você faz?” | “O paredão cobre o Mule do norte; a trilha sul desce em 10 min até um ombro com linha de rádio melhor — e frio.” |
| Menu de 6 itens | 3 caminhos **visíveis** no texto de ambiente |
| Opção sem custo | “Segundo ping gasta bateria e sobe assinatura; esperar até 04h gasta água.” |

**Regra:** se a ação seguinte **depende** do terreno, o ambiente **já** entregou o dado (altura, cobertura, distância aproximada, silhueta de NC, etc.).

---

## 4. Ganchos que puxam o jogador (equilíbrio)

Toda resposta de RP (exceto fechamento de sessão) termina com **≥1**:

| Tipo | Exemplo |
| ---- | ------- |
| **Decisão com horário** | Valk (ops, se o plano ainda está aberto): “Saímos às quatro ou espera o recado?” — **não** se o plano já fechou |
| **NPC com voz** | Lira pergunta; Sasha marca limite |
| **Ambiente que convida ação** | “Há lenha seca a 30 m sob o paredão.” |
| **Canal / tempo** | Burst fraco; silêncio útil com custo |
| **Relacional residual** | Olhar, distância, oferta de ajuda pós-cena |

**Proibido como único gancho:** “O que Ryan faz?” sem conteúdo.  
**Proibido:** coreografia de idle (cantil/fogo) como substituto de gancho.

Equilíbrio por modo:

| Modo | Ambiente | Relacional | Arco/ops |
| ---- | -------- | ---------- | -------- |
| Chegada / local novo | **Alto** (bloco §2) | Baixo–médio | 1 batida se AGENDA |
| DOWNTIME mesmo sítio | Baixo (só delta) | **Alto** se NPCs presentes | Idle → arco_ativo |
| OPERAÇÃO | Médio (terreno útil) | Baixo | Resultado primeiro |
| INTIMIDADE | Mínimo | **Alto** (SHOW) | Não matar com ops |

---

## 5. Relacionamento: SHOW, não TELL (atalho)

| Evitar | Fazer |
| ------ | ----- |
| Valk resume “Lira solta / Sasha segura” | Lira **fala** ou age; Sasha **escolhe** distância/ajuda |
| Abraço em 6 linhas sem info | ≤2 linhas de corpo + **1 fala com delta** |
| NPC “presente” sem voz o turno inteiro | Se em cena e relevante: **≥1** voz **ou** escolha por bloco |
| Cena emocional e sumiço | **1 residual** em ≤2 turnos (gesto, silêncio diferente, pergunta) |

Modelos situacionais (estado 018): [arco_ativo.md](../board/arco_ativo.md) §7.

---

## 6. Imagem do lugar — política (opcional)

### 6.1 O que eu acho

| Abordagem | Prós | Contras | Uso recomendado |
| --------- | ---- | ------- | --------------- |
| **Só texto (bloco AMBIENTE)** | Rápido, canônico, zero ruído de era | Exige disciplina do narrador | **Default sempre** |
| **Gerar imagem (Imagine/Grok)** | Ajuda visual imediata; bom em local novo | Latência/token; estilo pode “2077” demais; inconsistente entre cenas | **Sob pedido** ou 1ª chegada a landmark |
| **Puxar da internet** | Referência rápida | Errado de era (2077≠RED 2045), copyright, facções/look errados | **Só** como ref. de *mood* genérico (deserto, cânion, skyline) — **não** como “foto canônica” do SoT |

**Recomendação de campanha:**  
1) Texto rico no §2 **sempre** em local novo.  
2) Imagem **opcional** com comando `[Imagem do lugar]` — 1 por local/chegada, não por turno.  
3) Não depender de imagem para opções: o texto **já** lista layout e ações.  
4) Se gerar: prompt **RED/2045**, Badlands sujos, sem UI de jogo, sem logo de corpo 2077; descrever o que o **bloco AMBIENTE** já disse (consistência texto→imagem).

### 6.2 Quando oferecer imagem (narrador)

- Chegada a **Night City** / bairro novo / facility / marco visual.  
- Jogador pede.  
- **Não** em turnos de só diálogo íntimo no mesmo acampamento.

### 6.3 Prompt-base (gerar)

```text
Cyberpunk RED 2045 aesthetic, grounded, dusty Badlands / [local],
practical gear not glossy, muted colors, no game UI, no logos,
wide establishing shot of [layout do bloco AMBIENTE em 1 frase]
```

---

## 7. Checklist 5s (narrador)

```text
[ ] Local novo ou ação depende do terreno? → bloco AMBIENTE
[ ] 3–5 opções embutidas (não menu vazio)
[ ] Delta ≥60%? Eco ≤2 linhas?
[ ] SHOW relacional se NPCs em foco
[ ] Gancho final com conteúdo
[ ] Imagem só se pedido / landmark — texto já basta para jogar
```

---

## Referências

- [motor_cena_1pager.md](motor_cena_1pager.md) · [diretrizes_narrador.md](diretrizes_narrador.md) §7.1  
- [arco_ativo.md](../board/arco_ativo.md) · [context_pack_atual.md](../logs/context_pack_atual.md)  
- [comandos_jogador.md](comandos_jogador.md)
