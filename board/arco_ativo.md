# Arco ativo (L1) + Off-screen de NPCs

**Finalidade:** dar **norte de progressão** sem trilho fechado.  
**Não é tier-0 completo** — o narrador lê sob demanda quando a cena estagna ou o arco avança.  
**Índice no boot:** bloco **NORTE** em [context_pack_atual.md](../logs/context_pack_atual.md) (curto / médio / longo / fora). Este arquivo = operação L1. **Não** copiar os bullets do pack aqui.  
**Inventário longo prazo:** [event_queue.md](../event_queue.md).  
**Atualizado:** ~03/08/2026 (pós-026) · sessão vigente **026** · próxima **027**

---

## 0. Regras do arquivo (hard)

| # | Regra |
| - | ----- |
| 1 | **1 arco em foco** por vez (os outros = 1 linha em “Filas”). |
| 2 | Batidas são **possíveis**, não obrigatórias. Jogador pode ignorar. |
| 3 | **Idle default:** se o PC não puxa por ≥1 sessão ou mood ≥3 turnos sem delta → usar **default se idle** do arco (não inventar plot fora da tabela). |
| 4 | **F10:** NPC off-screen só “aparece” no que Ryan pode perceber (rádio, boato, encontro, tempo). |
| 5 | **Sem retcon.** Fail-forward ok. Não forçar combate só para destravar. |
| 6 | Atualizar este arquivo no **Finalizar** se a fase do arco mudou. Se o objetivo L1 mudou, 1 linha no **NORTE médio** do pack. |

---

## 1. Camadas (modelo genérico — reutilizar sempre)

| Camada | Horizonte | Onde vive | Uso |
| ------ | --------- | --------- | --- |
| **L0 Cena** | esta sessão / horas | AGENDA + **NORTE curto** no pack | Anti-estagnação local |
| **L1 Arco ativo** | 1–3 sessões | **este arquivo §3** · índice **NORTE médio** no pack | Norte de progressão |
| **L2 Filas** | semanas | `event_queue.md` | E0XX prioritários |
| **L3 Temas** | longo prazo | §5 abaixo · índice **NORTE longo** no pack | Frentes estáveis |

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

- **Bom:** “Canal morto de verdade — sem carrier.” Valk (residual alto, sem caderno): *“Ainda nada. Vem.”* Ou, se o plano ainda estiver aberto: *“Espera o recado ou move amanhã cedo?”*  
- **Bom:** “Um burst de 3s, protocolo errado, morre. Não é a **Lina ‘Sparrow’ Park**; é ruído de outro tráfego.”  
- **Ruim:** “Canais ainda mudos. Estrelas. Água. Warden quieto.” (sem decisão / sem custo)

---

## 3. L1 — Arco em foco agora: **E015** (caminho NC / Kaz)

| Campo | Valor |
| ----- | ----- |
| **ID** | E015 (+ E005 latente, E011 no pacote NC) |
| **Fase** | Caixa 101 **coletada** 03/08. Chip preto **lacre intacto** + tira: hop NC **05/08 após 21h**; ponto = o chip; sem voz; sem ping antigo. Sparrow sem ACK; Steel mudo; Kaz off |
| **Local do PC** | Pack Badlands (~03/08 **tarde** · tenda Ryan/Valk · descanso) |
| **Objetivo do arco** | Abrir o chip → hop NC 05/08 21h (Valk junto); rede Sparrow/Steel → Kaz; **sem** ops solo sem extração; acordo 019 = **perguntar**, não cobrar |
| **Fora de foco (1 linha)** | Célula **Cutter** (E008) = um corte **depois** do Condor leste pousar · Pack Node/casas/olaria · BT latente · E020 cobra Reyes · **não** reabrir caixa 101 |

### 3.1 Batidas possíveis (ordem flexível)

| # | Batida | Gatilho típico | Resultado possível (exemplos) |
| - | ------ | -------------- | ----------------------------- |
| B1 | **Decisão 25/07** | **feita** (cânion) | — |
| B2 | **Resposta de contato** | relógio off-screen **Steel** ou **Sparrow** (pessoas) | Resposta parcial · “não agora” · janela · silêncio *útil* com custo |
| B3 | **Movimento Badlands** | após B1 “move” | Chegada a próximo ponto (N9); 0–1 anomalia só se AGENDA/SoT |
| B4 | **Entrada / borda NC** | rota definida | Heat leve, escolha de entrada, não dump de plot |
| B5 | **Rede NC** | contato ok | Kaz / intermediário / Doc Moreau (E011) / crew |
| B6 | **Assunto pessoal Ryan** | em NC | sem fechar Pack; 1–2 cenas, não monólogo eterno |
| B7 | **Coleta Condor** | 30/07 15h–17h | **Feita** — 1º pacote anônimo; intermediário 48–72h |
| B8 | **Dead drop 101** | 03/08 meio-dia | **Feita** — chip lacre + tira hop NC 05/08 21h |
| B9 | **Hop NC** | 05/08 após 21h | Entrada / intermediário / silêncio com custo |

### 3.2 Default se idle (PC não puxa)

Ordem fixa — narrador pega **1 item por bloco de idle**, não a lista inteira:

1. **Chip:** lacre intacto — Ryan abre em casa **ou** o relógio 05/08 21h aperta.  
2. **Condor leste:** pouso / recado na tenda **ou** silêncio até o pássaro voltar.  
3. **Valk:** 1 batida SHOW (toque + 1 linha quente). **Sem** caderno. **Sem** reabrir a caixa.  
4. **Reyes / Cutter:** um corte **quando o céu pousar**; **não** raid hoje; 101 fechou.

### 3.3 Off-screen agora (E015) — instância da §2.1

| NPC / canal | Onde | O que está fazendo | Por que sem resposta (ainda) | Relógio | Como Ryan percebe | Default se idle |
| ----------- | ---- | ------------------ | ---------------------------- | ------- | ----------------- | --------------- |
| **Kaz “The Broker”** | Night City, **escondido** | Montando crew futura | Não é alvo do ping | Dias | Via intermediário / B5 | Ficha crew |
| **Marcus “Steel” Rivera** ([ficha](../fichas/npc/marcus_steel_rivera.md)) | NC | OPSEC / job / favores | Ping `RVW…` em fila ou risco | Relógio estourou → **019** | Burst, resposta, “depois”, silêncio com custo | **Pessoa**, não sistema; ≠ Echo Rivera |
| **Lina “Sparrow” Park** ([ficha](../fichas/npc/lina_park.md)) | NC | OPSEC / fila — residual fraco **sem ACK** (018–026) | Silêncio deliberado registrado 019 | Hop **05/08 21h** (chip ainda fechado) | Resposta dela, “não agora”, ou residual morre com custo | **Pessoa** (handle Sparrow); **não** drone/sistema |
| **Crew NC** (Alex, etc.) | NC (off) | Vida normal / E004 latente | Fora do ping atual | Só se B5 ou reencontro | Cena ou boato | Não puxar sem gancho |
| **Pack** (Reyes, Tio Gringo, Node) | Badlands | Rotina + E019 em discussão lenta | Ryan presente | Pulso diário se dia avança | Mensagem só se canal Pack aberto | Background; não compete com E015 na cena |

**Nota de mestragem:** **Steel** e **Sparrow** são **NPCs humanos** com handle de rádio. A **resposta de um deles** deve existir no relógio (chegar, recusar, ou falhar de forma útil). Silêncio eterno sem custo **quebra** o L1. Não narrar “Sparrow” como modo/Agent/protocolo. Kaz **não** precisa responder ao ping.

### 3.4 O que **não** fazer neste arco (agora)

- Inventar **segundo** combate Raffen/BT hoje (Cutter = um corte após o céu, Reyes).  
- Reabrir a caixa da 101 ou narrar o conteúdo do chip **antes** de Ryan abrir.  
- Revelar paradeiro exato de Kaz sem canal.  
- Transformar Lira/Sasha em tutorial eterno no lugar de B2.  
- Eco de mood / música como substituto de batida de arco.  
- Reabrir Valk como CO / caderno de 3 itens / “cobra o plano” — especialmente no boot.

---

## 4. L0 — AGENDA sugerida (espelho; SoT da cena = context pack)

> Se o pack divergir, **vence o pack**. Rascunho alinhado ao Pack pós-026.

| # | Gancho com conteúdo | Quem age se idle | Ação concreta |
| - | ------------------- | ---------------- | ------------- |
| 1 | Chip lacre intacto (abrir em casa) | Ryan / mundo | Relógio 05/08 21h se idle |
| 2 | Condor leste ainda no ar | Sasha / Lira / Reyes | Pouso + recado; Reyes marca **um** corte |
| 3 | Hop NC 05/08 após 21h | Mundo / intermediário | Sem voz; sem ping antigo; não forçar Sparrow/Steel |

---

## 5. L3 — Temas de longo prazo (estáveis)

> Índice de 1 linha: pack **NORTE longo**. Esta tabela = frentes. Soft / spoiler: [ideas_concepts](../ideas_concepts/README.md) (não boot).

| Frente | Estado 1 linha |
| ------ | -------------- |
| Pack / casas / Node / olaria | Autonomia crescente; Ryan pode voltar depois de NC |
| Biotechnica (E001/E006) | Latente |
| Raffen (E008) | Heat residual, não chase ativo |
| Crew / polycule / NC | Reencontros **após** E015 / crew montada; fases **opcionais** ([polycule](../relacionamentos/crew_polycule_ryan_valk_alex_reina.md)) |
| Doc Moreau (E011) | Visita com Valk em NC; lore pesado / BD 7 anos **bloqueado** até condições (ficha Doc) |
| Latentes / procedural | Pista sob crisis — [gatilhos](../fichas/notas_narrador/ryan_gatilhos_memorias.md); soft [ideas_concepts](../ideas_concepts/README.md) |
| Ideia Reyes (cobra mimética, E020) | Conceito 020 (era bola); tempo livre; **não** apresentada |

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

## 7. Batidas-modelo relacionais (estado 026 — SHOW)

> **Uso:** quando o PC abre espaço ou idle relacional. **1 batida por bloco**, não as três de uma vez.  
> Valk **não** resume o progresso das outras — elas **mostram**.  
> Ambientação de lugar: [cena_ambientacao_ganchos.md](../sistema/cena_ambientacao_ganchos.md).

### 7.0 Estado emocional (SoT curto pós-026)

| Quem | Onde está na cabeça | O que já aconteceu | Próximo passo orgânico |
| ---- | ------------------- | ----------------- | ---------------------- |
| **Valk** | Residual íntimo alto; volante na 101 (não no bordo); chip é depois | 026: tenda 02/08; caixa; volta Pack | SHOW quente; **não** reabrir jantar/caixa; **não** CO do Cutter |
| **Lira** | Residual positivo; leste visual 03/08 | Off-screen no Condor | **Fala própria** quando pousar |
| **Sasha** | Residual positivo; assusta com operador | Off-screen no Condor | Residual (ajuda/distância) — não sumir |

### 7.1 Voz Valkirya — exemplos (obrigatório no boot)

> **Curta ≠ dois vocábulos.** Copiar o teto (frase de gente), não o chão (rádio).  
> Valk-seca **não** vaza: Reyes / Sasha / Lira falam pela ficha, não neste registo.

| Ruim (chat 023 contaminado — **não copiar**) | Bom (residual alto / downtime) |
| -------------------------------------------- | ------------------------------ |
| “Três coisas. Sem ordem bonita.” | (toque no pulso) “Ainda nada no link. Vem. Eu fico.” |
| “Qual desses três você quer fechar antes de dormir.” | “Oficina ou sombra. Eu vou com você.” |
| “Sem isso eu não top.” / “Eu decido o como.” | “Se marcar o dia, eu cubro. Quer isso — ou espera o recado?” |
| “Não transformar café em tribunal.” / “bonitinha de encomenda.” | “Cara amarrada passou.” + beijo / copo / ombro |
| Silêncio de cooldown a noite inteira como resposta afetiva | 1–3 linhas baixas + corpo colado; se estiver chateada, **fala** |
| Glosa: “não é ordem” / “sem briefing” / “Teto às cinco” no beijo | Polegar no cinto. “Oficina e some. Eu pego o Mule.” Quase na boca. “O resto é tenda.” |
| Frase-rádio (“Corte.” / “Reyes.” / “Agora.”) como única fala | Frase de gente: o recado cabe num período composto |

**Ops (plano aberto e Ryan pediu):** curta, seca, leal — *“Mule no leste, abort no rádio. Eu no volante. Tu marca a janela.”* (ainda é pessoa; não três vocábulos.)  
**Ops (plano já fechado — trava 023):** **não** reabre. Uma confirmação: *“Continua o combinado. Eu vou com você.”*

**Reyes (não herda Valk):** *“Camp eu não tenho. Corredor, sim. O céu amanhã me diz onde corto — um, não um raid. Tu some de novo no mesmo dia. A 101 não é minha estrada.”*

Acordo 019 = **uma pergunta** antes de vetar. Idle de arco **não** é ela virar CO.

---

## Referências

- [context_pack_atual.md](../logs/context_pack_atual.md) · [event_queue.md](../event_queue.md) · [board_campanha.md](board_campanha.md)  
- [cena_ambientacao_ganchos.md](../sistema/cena_ambientacao_ganchos.md) · [motor_cena_1pager.md](../sistema/motor_cena_1pager.md) · [npc_agencia_cena.md](../sistema/npc_agencia_cena.md)  
- [sessao_resumo_023.md](../logs/sessao_resumo_023.md)  
- Soft longo prazo: [ideas_concepts/README.md](../ideas_concepts/README.md) (não boot)
