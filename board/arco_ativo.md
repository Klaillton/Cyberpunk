# Arco ativo (L1) + Off-screen de NPCs

**Finalidade:** dar **norte de progressão** sem trilho fechado.  
**Não é tier-0 completo** — o narrador lê sob demanda quando a cena estagna ou o arco avança.  
**Tier-0:** [context_pack_atual.md](../logs/context_pack_atual.md) (1 linha aponta para cá).  
**Inventário longo prazo:** [event_queue.md](../event_queue.md).  
**Atualizado:** ~26/07/2026 (pós-018) · sessão vigente **019**

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
- **Bom:** “Um burst de 3s, protocolo errado, morre. Não é a **Lina ‘Sparrow’ Park**; é ruído de outro tráfego.”  
- **Ruim:** “Canais ainda mudos. Estrelas. Água. Warden quieto.” (sem decisão / sem custo)

---

## 3. L1 — Arco em foco agora: **E015** (caminho NC / Kaz)

| Campo | Valor |
| ----- | ----- |
| **ID** | E015 (+ E005 latente, E011 no pacote NC) |
| **Fase** | **Aproximação NC** — industrial + pesquisa; canal de **Lina “Sparrow” Park** residual sem resposta (**B2 atrasado**) |
| **Local do PC** | Badlands / borda NC · zona **industrial abandonada** (chegada 019) |
| **Objetivo do arco** | Localizar rede via contatos **Sparrow** / **Steel** (NPCs) → Kaz; sem queimar discrição; Valk junto; **sem** ops solo sem extração |
| **Fora de foco (1 linha)** | Pack (Node, casas, olaria) roda sem Ryan · BT latente · Raffen residual |

### 3.1 Batidas possíveis (ordem flexível)

| # | Batida | Gatilho típico | Resultado possível (exemplos) |
| - | ------ | -------------- | ----------------------------- |
| B1 | **Decisão 25/07** | amanhecer / Valk cobra | Fica no cânion · 2º ping · muda posição |
| B2 | **Resposta de contato** | relógio off-screen **Steel** ou **Sparrow** (pessoas) | Resposta parcial · “não agora” · janela · silêncio *útil* com custo |
| B3 | **Movimento Badlands** | após B1 “move” | Chegada a próximo ponto (N9); 0–1 anomalia só se AGENDA/SoT |
| B4 | **Entrada / borda NC** | rota definida | Heat leve, escolha de entrada, não dump de plot |
| B5 | **Rede NC** | contato ok | Kaz / intermediário / Doc Moreau (E011) / crew |
| B6 | **Assunto pessoal Ryan** | em NC | sem fechar Pack; 1–2 cenas, não monólogo eterno |

### 3.2 Default se idle (PC não puxa)

Ordem fixa — narrador pega **1 item por bloco de idle**, não a lista inteira:

1. **Valk** fecha plano de manhã: 1 preferência + 1 alternativa (fica / ping / move) com horário.  
2. **Lira** faz **1 pergunta audível** (drone, o que fazem amanhã, olaria no Pack) — sem murmúrio vazio.  
3. **Off-screen §3.3:** 1 batida de **contato** (Steel / Sparrow / Kaz) **ou** avanço de relógio.  
4. Só então micro-logística (fogo, água, sono) — **nunca** sozinha como “delta”.

### 3.3 Off-screen agora (E015) — instância da §2.1

| NPC / canal | Onde | O que está fazendo | Por que sem resposta (ainda) | Relógio | Como Ryan percebe | Default se idle |
| ----------- | ---- | ------------------ | ---------------------------- | ------- | ----------------- | --------------- |
| **Kaz “The Broker”** | Night City, **escondido** | Montando crew futura | Não é alvo do ping | Dias | Via intermediário / B5 | Ficha crew |
| **Marcus “Steel” Rivera** ([ficha](../fichas/npc/marcus_steel_rivera.md)) | NC | OPSEC / job / favores | Ping `RVW…` em fila ou risco | Relógio estourou → **019** | Burst, resposta, “depois”, silêncio com custo | **Pessoa**, não sistema; ≠ Echo Rivera |
| **Lina “Sparrow” Park** ([ficha](../fichas/npc/lina_park.md)) | NC | OPSEC / fila — residual fraco **sem resposta** (018) | Residual ≠ ela confirmou | **Imediato (019)** B2 | Resposta dela, “não agora”, ou residual morre com custo | **Pessoa** (handle Sparrow); **não** drone/sistema |
| **Crew NC** (Alex, etc.) | NC (off) | Vida normal / E004 latente | Fora do ping atual | Só se B5 ou reencontro | Cena ou boato | Não puxar sem gancho |
| **Pack** (Reyes, Tio Gringo, Node) | Badlands | Rotina + E019 em discussão lenta | Ryan saiu | Pulso diário se dia avança | Mensagem só se canal Pack aberto | Background; não compete com E015 na cena |

**Nota de mestragem:** **Steel** e **Sparrow** são **NPCs humanos** com handle de rádio. A **resposta de um deles** deve existir no relógio (chegar, recusar, ou falhar de forma útil). Silêncio eterno sem custo **quebra** o L1. Não narrar “Sparrow” como modo/Agent/protocolo. Kaz **não** precisa responder ao ping.

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
| 2 | **B2** — resposta de **Steel** ou **Sparrow** (NPCs · §3.3) | Mundo / rádio | Resposta útil **ou** silêncio com custo — não jargão solto “ACK Sparrow” |
| 3 | Lira/Sasha — abertura residual **com fala** | Lira (Sasha reage) | 1 pergunta ou limite audível; sem murmúrio vazio |

---

## 5. L3 — Temas de longo prazo (estáveis)

| Frente | Estado 1 linha |
| ------ | -------------- |
| Pack / casas / Node / olaria | Autonomia crescente; Ryan pode voltar depois de NC |
| Biotechnica (E001/E006) | Latente |
| Raffen (E008) | Heat residual, não chase ativo no cânion |
| Crew / polycule / NC | Reencontros **após** E015 / crew montada; fases **opcionais** ([polycule](../relacionamentos/crew_polycule_ryan_valk_alex_reina.md)) |
| Doc Moreau (E011) | Visita com Valk em NC; lore pesado / BD 7 anos **bloqueado** até condições (ficha Doc) |
| Latentes / procedural | Pista sob crisis — [gatilhos](../fichas/notas_narrador/ryan_gatilhos_memorias.md); soft [ideas_concepts](../ideas_concepts/README.md) |

---

## 6. Checklist rápido (narrador, 5s)

```text
[ ] Fase do arco ainda correta?
[ ] Off-screen dos contatos quentes preenchido (não “sumidos”)?
[ ] Idle? → default §3.2 / protocolo §2 — 1 batida com conteúdo
[ ] Delta ≥60%? Sem eco de mood do PC
[ ] SHOW relacional (§7) se Lira/Sasha/Valk em foco
[ ] Local novo / ação no terreno? → bloco AMBIENTE ([cena_ambientacao_ganchos.md](../sistema/cena_ambientacao_ganchos.md))
[ ] Gancho final com conteúdo (não “o que você faz?” vazio)
[ ] F10 ok?
```

---

## 7. Batidas-modelo relacionais (estado 018 — SHOW)

> **Uso:** quando o PC abre espaço ou idle relacional. **1 batida por bloco**, não as três de uma vez.  
> Valk **não** resume o progresso das outras — elas **mostram**.  
> Ambientação de lugar: [cena_ambientacao_ganchos.md](../sistema/cena_ambientacao_ganchos.md).

### 7.0 Estado emocional (SoT curto pós-cena Sasha / mirante)

| Quem | Onde está na cabeça | O que já aconteceu | Próximo passo orgânico |
| ---- | ------------------- | ----------------- | ---------------------- |
| **Valk** | Protege ritmo; ciúme leve mas confia; quer Ryan + plano de manhã | Viu Ryan feliz com a ideia das duas; clarificou “gosta do Pack ≠ romance” | Cobra decisão 25/07; residual carinho **com** conteúdo |
| **Lira** | Mais aberta; olaria; Vespa; curiosidade sem pressa | Conversas 017; assobio na caça; menos cena densa na 018 | **Fala própria** (não só “solta” no relatório da Valk) |
| **Sasha** | Medo de abandono; gosta do que Ryan fez; não prometeu NC | Cena aves: “mais tempo”, “não some sem avisar”, NC “eu penso” | **Residual** (distância/ajuda/silêncio) — não sumir da trama |

### 7.1 Modelo **Lira** (abertura com voz)

**Gatilho:** idle ≥2 · café/fogo · menção a Pack/drone/amanhã · Ryan sozinho perto dela.

**Fazer (exemplo de forma, não script literal):**
- 1–2 falas **audíveis** com pedido ou observação concreta (Vespa, olaria, “dorme cedo?”, “amanhã a gente move?”).
- 1 gesto (assobio, sentar mais perto, sorriso de canto) **ligado** à fala.
- Deixar **gancho** para Ryan responder em 1 linha.

**Não fazer:** murmúrio inaudível; só reagir ao sorriso dele; Valk explicar que “ela está mais solta”.

**Gancho típico pós-batida:** pergunta dela no ar **ou** escolha prática (vigia / sono / ajudar no Mule).

### 7.2 Modelo **Sasha** (residual pós-cena forte)

**Gatilho:** ≤2 turnos após batida emocional · fogueira · preparo de saída · Ryan passa perto.

**Fazer:**
- **Não** repetir o monólogo das aves.  
- 1 residual: ajuda prática, distância calibrada diferente, frase curta (“Ainda não prometi nada sobre NC” / “Só… avisa se for sumir”) **ou** silêncio **ativo** (trabalha perto sem olhar).  
- Se idle longo: ela confirma perímetro **e** 1 linha que lembra o medo de perda sem drama.

**Não fazer:** sumir do bloco; virar romance forçado; Valk traduzir o sentimento dela.

**Gancho típico:** ela espera resposta **ou** segue trabalhando deixando espaço — Ryan pode falar ou respeitar.

### 7.3 Modelo **Valk** (vínculo + arco, sem TELL)

**Gatilho:** intimidade · mirante · pós-conversa com as duas · manhã de decisão.

**Fazer:**
- ≤2 linhas de corpo + **1 fala com delta**: plano (horário/ping/move), limite, humor, medo, ou pergunta sobre o que ele *não* resolveu (Sasha/canal).  
- Se falar das duas: **no máximo 1 meia-frase**, e em seguida **elas** aparecem ou a conversa volta para o casal/decisão.  
- Preferir: “Amanhã às quatro. Eu dirijo o primeiro trecho.” em vez de “A Lira está solta e a Sasha segura.”

**Não fazer:** eco longo de abraço; status report do polycule implícito; plateia.

**Gancho típico:** decisão com horário **ou** convite (“fica mais um pouco / volta pro Mule”).

### 7.4 Como combinar com ambiente e ops

| Situação | Ordem na resposta |
| -------- | ----------------- |
| **Chegada a local novo** | Bloco AMBIENTE → 1 batida NPC/arco → gancho |
| **Mesmo acampamento + relacional** | Delta fala/gesto (§7.x) → 0–1 linha ambiente se mudou → gancho |
| **Ops (ping, caça, viagem)** | Resultado primeiro → 1 residual relacional se couber → gancho |
| **Idle sem PC puxar** | Default §3.2 **usando modelos §7** (não cantil/fogo sozinhos) |

---

## Referências

- [context_pack_atual.md](../logs/context_pack_atual.md) · [event_queue.md](../event_queue.md) · [board_campanha.md](board_campanha.md)  
- [cena_ambientacao_ganchos.md](../sistema/cena_ambientacao_ganchos.md) · [motor_cena_1pager.md](../sistema/motor_cena_1pager.md) · [npc_agencia_cena.md](../sistema/npc_agencia_cena.md)  
- [sessao_resumo_017.md](../logs/sessao_resumo_017.md)  
- Soft longo prazo: [ideas_concepts/README.md](../ideas_concepts/README.md) (não boot)
