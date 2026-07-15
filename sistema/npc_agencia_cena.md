# Agência de NPCs in-scene

**Finalidade:** Playbook para NPCs **falarem entre si**, **decidirem micro-ações** e **executarem tarefas delegadas** enquanto Ryan está na cena — sem controlar o protagonista e sem devolver o mesmo menu de opções ao jogador.

**Complementa:** [pulso_procedimento.md](pulso_procedimento.md) (off-screen, 1×/dia) · [diretrizes_narrador.md](diretrizes_narrador.md) §3

**Branch:** `feature/linha-estavel` · **Atualizado:** 15 de Julho de 2026

---

## 1. Princípios (hard rules)

| Regra | Detalhe |
| ----- | ------- |
| Ryan não é controlado | Narrador não escreve ações, falas nem decisões do protagonista. |
| F10 anti meta-game | NPC só sabe o que viu/ouviu na cena ou por canal plausível. |
| Sem inventar | Nomes e facções vêm de board, fichas, pulsos — não criar personagens genéricos (ex.: "Gus", "Marcus"). |
| Escala | Autonomia = **micro** (planejar caça, pedir peça, discordar, organizar rota). Missão do pack / segredos (F11, L03) → Ryan ou Reyes quando couber. |
| **Delegação executa** | Se Ryan **delegou** uma tarefa ("Valk, planeje X"), o NPC **entrega o plano** — não devolve o trabalho disfarçado de pergunta. |
| **Anti-loop** | Se a mesma pergunta/opções A/B/C já apareceu **2×** na sessão, o narrador **avança** com decisão do NPC na 3ª vez. |

---

## 2. Gatilhos

| Modo | Quando | Limite por turno |
| ---- | ------ | ---------------- |
| **Ambiental** | 2+ NPCs relevantes no NOW (context pack / board) | 0–1 troca curta (2–4 linhas) ou 1 micro-decisão observável |
| **Passivo** | `*observo em silêncio*`, `espero`, beat sem ação nova | 1–2 trocas NPC↔NPC ou 1 decisão pequena (consultar pulso) |
| **Explícito** | `[Agência NPC]`, `deixem eles decidirem`, `Valk, planeje…` | NPC **executa** o pedido; 1 bloco com resultado concreto |
| **Delegação** | Ryan pede a NPC competente fazer planejamento/logística | NPC devolve **plano fechado**; Ryan só veta ou ajusta se quiser |

---

## 3. Formato de escrita

```markdown
**NARRADOR:** … ambiente …

**Valk:** "…"
**Elias:** "…" *(gesto: aponta a válvula)*

**NARRADOR:** … consequência que Ryan percebe …
```

- Falas: nome em negrito + aspas (no motor solo futuro: `[NPC-F:Valk]`).
- Decisão autônoma: narrar **o que Ryan vê/ouve**, não monólogo interno do NPC.
- Terminar com **gancho** para Ryan reagir — não fechar a cena com "o que você faz?".

---

## 4. Fluxo do narrador

1. Ler **NOW** em [context_pack_atual.md](../logs/context_pack_atual.md) — quem está presente.
2. Abrir ficha + pulso dos NPCs na cena (ex.: Valk → [ficha](../fichas/nomad%20-%20lena_valk_kane.md) + [pulso](../pulso_do_mundo/crew/valk.md)).
3. Identificar gatilho (ambiental / passivo / explícito / delegação).
4. Resolver **1 gancho** do pulso adaptado à cena (não copiar literal).
5. Se mudou estado → candidato a update (board, relacionamentos) no fluxo normal de sessão.

---

## 5. Exemplo canônico — delegação (caça às aves / Valk)

### Problema observado (anti-padrão)

Ryan quer ir **caçar aves** nas Badlands. Ele pede a **Valk** que faça o **planejamento** (logística, horário, rota, equipamento). A narradora/IA **repete 3–4 vezes** o mesmo diálogo, pedindo de volta a Ryan que escolha rota, horário ou "como prefere planejar" — como se a delegação não tivesse ocorrido.

Isso viola:

- **Delegação executa** (§1)
- **Anti-loop** (§1)
- Competência de Valk (Tactics 4, organização de scav, nomad de estrada — ver ficha)

### Entrada do jogador (exemplo)

> "Valk, quero caçar algumas aves amanhã cedo. Planeja isso para mim — rota, horário, o que levar e quem fica no acampamento."

### Resposta correta (modelo)

**NARRADOR:** Valk para de alinhar o mapa no chão da tenda. Ela não pergunta de volta o que você já delegou — só confere uma última vez o vento na abertura da lona e começa a falar como quem já rodou dezenas de operações assim.

**Valk:** "Amanhã: saída **05h20**, antes do calor. Leva o **Mule** só até o cânion seco — depois a pé, duas horas máximo. Rotas: entramos pelo **leste do acampamento**, contorno da linha de postes queimados; evitamos o trecho aberto depois do meio-dia — Raffen passou ali na semana passada, segundo Rusty."

**Valk:** "Equipamento: rifle leve ou arco — o que você preferir levar, eu cubro munição e kit de campo. **Jax** (sentinela do pack) fica de overwatch no alto do cânion se ele topar; senão, **Rusty** no rádio do acampamento. **Reyes** não precisa saber ainda — é caça, não incursão."

**Valk:** "Eu fico no volante e no perímetro. Você caça; eu não entro na linha de tiro. Volta prevista **10h30**. Se quiser mudar só uma coisa — horário ou quem fica no acampamento — diz agora; senão, amanhã é isso."

**NARRADOR:** Ela dobra o mapa e guarda no coldre lateral do cinto, esperando tua confirmação ou um ajuste pontual — não um segundo planejamento do zero.

### O que o narrador NÃO deve fazer

- Repetir "qual rota você prefere: A, B ou C?" depois que Ryan já pediu o plano.
- Pedir a Ryan que "detalhe o planejamento" quando Valk foi nomeada responsável.
- Fazer Valk indecisa em logística que está no perfil dela (organizou scav de containers, recon, formação de veículos).
- Substituir Valk por NPC inventado na resposta.

### Quando Ryan ainda decide

- **Veto ou ajuste** explícito: "sem Jax (pack)", "saímos mais cedo", "quero arco, não rifle".
- **Risco novo** não previsto no plano (sinal de Raffen, clima, ferimento).
- **Segredo de campanha** que Valk não conhece (ex.: não revelar casas modulares — F11).

---

## 6. Exemplo secundário — NPCs entre si (oficina)

Ryan pergunta a Elias; **Elias e Tio Gringo** resolvem a peça entre si enquanto Ryan observa.

**Jogador:** `*observo em silêncio enquanto eles falham da válvula*`

**NARRADOR:** Elias segura o diagrama da destilaria. Tio Gringo já tem a peça na mão antes de você abrir a boca.

**Elias:** "Essa válvula aguenta a pressão do novo condensador?"

**Tio Gringo:** "Aguenta se você não forçar o fluxo na hora do meio-dia. Deixa eu ajustar o flange — meia hora."

**NARRADOR:** Elias assente e anota no canto do quadro. Ryan só precisa decidir se intervém ou deixa o trabalho seguir.

---

## 7. Anti-padrões

| Anti-padrão | Correção |
| ----------- | -------- |
| Ping-pong de planejamento (NPC devolve tarefa ao jogador) | NPC entrega plano; jogador só veta/ajusta |
| Mesmo diálogo 3–4× na sessão | Anti-loop: avançar estado na 2ª repetição |
| Pergunta a Elias, responde outro NPC | Quem foi nomeado responde; outros só se intercalarem de forma natural |
| Troca longa estilo novela sem input | Limitar a 1–2 falas NPC↔NPC por turno (salvo `[Agência NPC]` explícito) |
| Decisão que contradiz board / F11 / L03 | Consultar [board](../board/board_campanha.md) e [fatos_duros.md](fatos_duros.md) |

---

## 8. Referências

- [comandos_jogador.md](comandos_jogador.md) — § H `[Agência NPC]`
- [diretrizes_narrador.md](diretrizes_narrador.md) — §3 e §3.1
- [pulso_do_mundo/](../pulso_do_mundo/) — ganchos in-scene por NPC
- [fatos_duros.md](fatos_duros.md) — F10