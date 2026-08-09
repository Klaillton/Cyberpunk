# Arco ativo (L1) + Off-screen de NPCs

**Finalidade:** dar **norte de progressão** sem trilho fechado.  
**Não é tier-0 completo** — o narrador lê sob demanda quando a cena estagna ou o arco avança.  
**Tier-0:** [context_pack_atual.md](../logs/context_pack_atual.md) (1 linha aponta para cá).  
**Inventário longo prazo:** [event_queue.md](../event_queue.md).  
**Atualizado:** 24/07/2026 (pós-017) · sessão vigente **018**

---

## 0. Regras do arquivo (hard)

| # | Regra |
| - | ----- |
| 1 | **1 arco em foco** por vez (os outros = 1 linha em “Filas”). |
| 2 | Batidas são **possíveis**, não obrigatórias. Jogador pode ignorar. |
| 3 | **Idle default:** se o PC não puxa por ≥1 sessão ou mood ≥3 turnos sem delta → usar **default se idle** do arco (não inventar plot fora da tabela). |
| 4 | **F10:** NPC off-screen só “aparece” no que Ryan pode perceber (rádio, boato, encontro, tempo). |
| 5 | **Sem retcon.** Fail-forward ok. Não forçar combate só para destravar. |
| 6 | Atualizar este arquivo no **Finalizar** se a fase do arco mudou. |

---

## 1. Camadas (modelo genérico — reutilizar sempre)

| Camada | Horizonte | Onde vive | Uso |
| ------ | --------- | --------- | --- |
| **L0 Cena** | esta sessão / horas | AGENDA no context pack | Anti-estagnação local |
| **L1 Arco ativo** | 1–3 sessões | **este arquivo §3** | Norte de progressão |
| **L2 Filas** | semanas | `event_queue.md` | E0XX prioritários |
| **L3 Temas** | longo prazo | §5 abaixo | Frentes estáveis |

---

## 2. Protocolo OFF-SCREEN (genérico — qualquer NPC)

> Use sempre que um contato/NPC relevante **não está na cena** mas o arco depende dele.  
> Não precisa de cena dedicada: basta o narrador **saber o que estão fazendo** e liberar batida quando o relógio ou a AGENDA pedirem.

### 2.1 Tabela (preencher / atualizar por arco)

| NPC / canal | Onde (off-screen) | O que está fazendo (1 linha) | Por que ainda não responde / não aparece | Relógio (quando algo muda) | Como Ryan pode perceber (F10) | Se idle do PC → default |
| ----------- | ----------------- | ---------------------------- | ---------------------------------------- | -------------------------- | ----------------------------- | ----------------------- |
| *(exemplo)* | NC / Pack / estrada | … | ocupado / risco / sem sinal / escolha | ex.: +1 dia in-game | rádio, boato, encontro | … |

### 2.2 Estados de canal (genérico)

| Estado | Significado | Narrador pode… |
| ------ | ----------- | -------------- |
| **Mudo (aguardando)** | Mensagem pode ter chegado ou não; sem ACK | Confirmar silêncio útil **1×**; não repetir “canais mudos” como filler |
| **Ocupado** | NPC viu / priorizou outra coisa | Atrasar resposta; depois 1 batida parcial |
| **Risco / OPSEC** | Responder agora é perigoso | Resposta curtíssima, janela curta, ou intermediário |
| **Em trânsito** | Indo a ponto X | Chegada vira batida de tempo |
| **Ativo (agenda própria)** | Faz algo que muda o tabuleiro sem o PC | Resultado chega por canal plausível |
| **Respondido** | Contato estabelecido | Fechar estado; atualizar arco |

### 2.3 Regras de batida off-screen

1. **Todo contato quente tem linha na tabela §2.1** enquanto o arco depender dele.  
2. Silêncio **não é vazio**: o NPC está em um estado da §2.2.  
3. Após **1 noite** ou **1 sessão** de espera sem decisão do PC → liberar **1** de:  
   - resposta parcial / recusa / “me liga em X”; **ou**  
   - confirmação *útil* de silêncio + custo de tempo; **ou**  
   - NPC *presente* (Valk/Lira) propõe próximo passo com horário.  
4. **Proibido:** coreografia de idle (encher cantil / olhar fogo) como substituto de batida de arco.  
5. **Proibido:** inventar NPC novo só para carregar a resposta (usar contatos já no SoT).

### 2.4 Frases-modelo (anti-filler)

- **Bom:** “Canal morto de verdade — sem carrier. Valk: *amanhã cedo a gente decide: segundo ping ou move.*”  
- **Bom:** “Um burst de 3s, protocolo errado, morre. Não é Sparrow; é ruído de outro tráfego.”  
- **Ruim:** “Canais ainda mudos. Estrelas. Água. Warden quieto.” (sem decisão / sem custo)

---

## 3. L1 — Arco em foco agora: **E015** (caminho NC / Kaz)

| Campo | Valor |
| ----- | ----- |
| **ID** | E015 (+ E005 latente, E011 no pacote NC) |
| **Fase** | **Espera pós-ping** (Steel/Sparrow tentados 24/07, sem resposta) |
| **Local do PC** | Cânion Badlands · acampamento leve · noite 24/07 → manhã 25/07 |
| **Objetivo do arco** | Localizar / reaproximar rede de Ryan em NC (via Sparrow/Steel → Kaz) sem queimar discrição; Valk junto |
| **Fora de foco (1 linha)** | Pack (Node, casas, olaria) roda sem Ryan · BT latente · Raffen residual |

### 3.1 Batidas possíveis (ordem flexível)

| # | Batida | Gatilho típico | Resultado possível (exemplos) |
| - | ------ | -------------- | ----------------------------- |
| B1 | **Decisão 25/07** | amanhecer / Valk cobra | Fica no cânion · 2º ping · muda posição |
| B2 | **Resposta de canal** | relógio off-screen Steel/Sparrow | ACK parcial · “não agora” · janela · silêncio *confirmado* com custo |
| B3 | **Movimento Badlands** | após B1 “move” | Chegada a próximo ponto (N9); 0–1 anomalia só se AGENDA/SoT |
| B4 | **Entrada / borda NC** | rota definida | Heat leve, escolha de entrada, não dump de plot |
| B5 | **Rede NC** | contato ok | Kaz / intermediário / Doc Moreau (E011) / crew |
| B6 | **Assunto pessoal Ryan** | em NC | sem fechar Pack; 1–2 cenas, não monólogo eterno |

### 3.2 Default se idle (PC não puxa)

Ordem fixa — narrador pega **1 item por bloco de idle**, não a lista inteira:

1. **Valk** fecha plano de manhã: 1 preferência + 1 alternativa (fica / ping / move) com horário.  
2. **Lira** faz **1 pergunta audível** (drone, o que fazem amanhã, olaria no Pack) — sem murmúrio vazio.  
3. **Off-screen §3.3:** 1 batida de canal **ou** avanço de relógio (Steel/Sparrow/Kaz).  
4. Só então micro-logística (fogo, água, sono) — **nunca** sozinha como “delta”.

### 3.3 Off-screen agora (E015) — instância da §2.1

| NPC / canal | Onde | O que está fazendo | Por que sem resposta (ainda) | Relógio | Como Ryan percebe | Default se idle |
| ----------- | ---- | ------------------ | ---------------------------- | ------- | ----------------- | --------------- |
| **Kaz** | Night City, **escondido** | Montando / reativando **crew futura** (gente, favores, buracos seguros) — baixo perfil | Não é o alvo do ping; rede ainda fragmentada; OPSEC | Avança em **dias** in-game mesmo sem o PC; reencontrável via Sparrow/Steel ou E005 | Só via intermediário, boato de fixer, ou contato na B5 | Não “some do mundo”: cada 1–2 dias de espera, 1 passo invisível na montagem (só vira fato se canal abrir) |
| **Steel** | NC / rede de contatos | Agenda própria (trabalho, OPSEC, ou evitando calor) | Ping `RVW30sG1mBL_P?` pode estar em fila, filtrado, ou arriscado demais na hora | **25–26/07** (1ª janela útil) se PC não forçar; 2º ping do PC pode antecipar | Burst curto, ACK, “depois”, ou silêncio *com* razão implícita | Se PC espera sem 2º ping: **1 batida** até fim de 25/07 (resposta parcial **ou** silêncio útil) |
| **Sparrow** | NC / rede de contatos | Idem / canal paralelo a Steel | Mesmo protocolo; pode estar em job ou muda | **25–26/07** (pode ser o 1º a responder **ou** o 2º) | Idem Steel; não precisa dos dois no mesmo turno | Alternar com Steel: **não** dois silêncios vazios seguidos sem custo de tempo |
| **Crew NC** (Alex, etc.) | NC (off) | Vida normal / E004 latente | Fora do ping atual | Só se B5 ou reencontro | Cena ou boato | Não puxar sem gancho |
| **Pack** (Reyes, Tio Gringo, Node) | Badlands | Rotina + E019 em discussão lenta | Ryan saiu | Pulso diário se dia avança | Mensagem só se canal Pack aberto | Background; não compete com E015 na cena |

**Nota de mestragem:** a resposta de Steel/Sparrow **deve existir no relógio** (chegar, recusar, ou falhar de forma útil). Silêncio eterno sem custo **quebra** o L1. Kaz **não** precisa responder ao ping; precisa **estar ocupado com a crew** para o reencontro ter peso.

### 3.4 O que **não** fazer neste arco (agora)

- Inventar combate Raffen/BT só porque a noite está quieta.  
- Revelar paradeiro exato de Kaz sem canal.  
- Transformar Lira/Sasha em tutorial eterno no lugar de B1/B2.  
- Eco de mood / música como substituto de batida de arco.

---

## 4. L0 — AGENDA sugerida (espelho; SoT da cena = context pack)

> Se o pack divergir, **vence o pack**. Isto é rascunho alinhado ao cânion 24–25/07.

| # | Gancho com conteúdo | Quem age se idle | Ação concreta |
| - | ------------------- | ---------------- | ------------- |
| 1 | **B1** — amanhã: fica / 2º ping / move (Valk tem preferência de discrição) | Valk | Propõe horário + opção preferida em **fala** |
| 2 | **B2 / off-screen** — Steel ou Sparrow (relógio §3.3) | Mundo / rádio | 1 batida de canal **ou** silêncio *útil* + custo |
| 3 | Lira/Sasha — abertura residual **com fala** | Lira (Sasha reage) | 1 pergunta ou limite audível; sem murmúrio vazio |

---

## 5. L3 — Temas de longo prazo (estáveis)

| Frente | Estado 1 linha |
| ------ | -------------- |
| Pack / casas / Node / olaria | Autonomia crescente; Ryan pode voltar depois de NC |
| Biotechnica (E001/E006) | Latente |
| Raffen (E008) | Heat residual, não chase ativo no cânion |
| Crew / polycule / NC | Reencontro quando E015 avançar |
| Doc Moreau (E011) | Pacote da ida a NC com Valk |

---

## 6. Checklist rápido (narrador, 5s)

```text
[ ] Fase do arco ainda correta?
[ ] Off-screen dos contatos quentes preenchido (não “sumidos”)?
[ ] Idle? → default §3.2 / protocolo §2 — 1 batida com conteúdo
[ ] Delta ≥60%? Sem eco de mood do PC
[ ] F10 ok?
```

---

## Referências

- [context_pack_atual.md](../logs/context_pack_atual.md) · [event_queue.md](../event_queue.md) · [board_campanha.md](board_campanha.md)  
- [motor_cena_1pager.md](../sistema/motor_cena_1pager.md) · [npc_agencia_cena.md](../sistema/npc_agencia_cena.md)  
- [sessao_resumo_017.md](../logs/sessao_resumo_017.md)
