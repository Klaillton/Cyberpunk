# Pulso do Mundo — Procedimento Operacional

**Finalidade:** Simular o que acontece off-screen enquanto Ryan não está presente (ou está dormindo / focado em outra coisa).  
**Última atualização:** 03 de Julho de 2026

---

## 1. Quando rodar

| Gatilho | Ação |
| ------- | ---- |
| **Passou 1 dia in-game** | Rodar **1 ciclo diário completo** (obrigatório) |
| Ryan dorme a noite toda | Considerar 1 dia; rodar ao narrar o despertar |
| Viagem / downtime longo (vários dias) | 1 ciclo **por dia** narrado (não pular dias sem simular) |
| **Evento catalisador** (ver §4) | Ciclo diário **+** rolagens extras nas categorias elegíveis |
| Início de sessão (manhã) | Ler `Eventos Off-Screen Recentes` nos pulsos ativos; narrar 0–2 em cena |

**Escopo geográfico:**

| Pasta | Acionar quando Ryan está em… |
| ----- | ---------------------------- |
| `pulso_do_mundo/pack_badlands/` | Badlands / acampamento do pack |
| `pulso_do_mundo/crew/` | Night City, crew reunida, ou **mensagem/rumor** chega ao pack |

Não acionar pulsos de crew como cena local nas Badlands sem canal plausível (comlink, Kaz, etc.).

---

## 2. Ciclo diário (1× por dia in-game)

### Passo 1 — Rolagem da tabela geral

Abrir [pulso_do_mundo/pack_badlands/pulso_geral.md](../pulso_do_mundo/pack_badlands/pulso_geral.md).

Para **cada linha** da tabela de eventos, rolar **1d100** uma vez naquele dia.

| Resultado | Efeito |
| --------- | ------ |
| ≤ limiar da linha | Evento **tenta** ocorrer (resolver no Passo 2) |
| > limiar | Não ocorre neste dia |

**Regra de frequência vs impacto (inversa):**

- **Impacto baixo** (fofoca, olhares, rotina) → limiar **alto** → pode passar **várias vezes por semana**; com catalisador, até **2 ocorrências no mesmo dia** (2ª rolagem extra).
- **Impacto alto** (ameaça externa, confronto físico, incursão) → limiar **baixo** → raro mesmo com rolagem diária; **máx. 1× por semana in-game** mesmo se passar em dias seguidos (cooldown de 7 dias por linha).

### Passo 2 — Resolver com pulso NPC

1. Identificar **categoria** do evento que passou.
2. Abrir o **pulso** do NPC/grupo indicado na coluna *Pulso* da tabela (ou o mais relevante).
3. Responder **1–3 perguntas** da seção *Perguntas de Pulso* com base no estado dos arquivos (`board`, `relacionamentos`, `consequencias`).
4. Escolher **no máximo 1 gancho** da seção *Ganchos* (adaptar, não copiar literal).
5. Registrar em *Eventos Off-Screen Recentes* do pulso afetado (data in-game + 1 linha).

### Passo 3 — Limites do dia

| Regra | Valor |
| ----- | ----- |
| Eventos **resolvidos** por dia | **máx. 4** |
| Eventos **sociais / micro** (impacto 1–2) | **máx. 2** por dia |
| Eventos **ameaça / combate** (impacto 4–5) | **máx. 1** por semana |
| Mesma linha da tabela 2× no mesmo dia | Só com **catalisador** e impacto ≤ 2 |

Se o limite do dia estiver cheio, eventos que passaram na rolagem ficam como **rumor leve** (sem mudança de estado) ou empurram para o dia seguinte.

### Passo 4 — Persistência

| Tipo de resultado | Onde registrar |
| ----------------- | -------------- |
| Cena off-screen menor | *Eventos Off-Screen Recentes* no pulso |
| Mudança de relacionamento / reputação | `relacionamentos/`, `reputacao.md` |
| Impacto permanente | `consequencias/consequencias_persistentes.md` |
| Ameaça futura | `event_queue.md` |
| Exposição | `heat.md` |
| Log auditável (opcional) | `logs/pulso_YYYYMMDD.md` ([template](../logs/pulso_log_template.md)) |

**Arquivar:** quando *Eventos Off-Screen Recentes* tiver **> 5 entradas**, mover as mais antigas para `logs/pulso_*.md` ou resumir em `consequencias_persistentes.md`.

---

## 3. Limiares d100 (rolagem diária)

Conversão da coluna **Frequência** da tabela:

| Frequência (tabela) | Limiar d100 (≤ passa) | Impacto | Máx. vezes / dia | Cooldown se alto impacto |
| ------------------- | ---------------------- | ------- | ---------------- | ------------------------ |
| Muito Alta / Diário | 75 | 1 — Micro | 2 (com catalisador) | — |
| Alta / Quase todo dia | 60 | 2 — Baixo | 1 (+1 extra se catalisador) | — |
| Média | 40 | 3 — Médio | 1 | — |
| Baixa | 18 | 4 — Alto | 1 | 7 dias |
| Raro | 8 | 5 — Crítico | 1 | 14 dias |

**Exemplos alinhados ao pack atual:**

- Fofoca Ryan/Valk → impacto 1, limiar 75, pode ocorrer **mais de uma vez** no mesmo dia se houver catalisador social.
- Alguém sai do acampamento (caça/comércio) → impacto 2, limiar 60, rotineiro.
- Raffen / Biotechnica → impacto 5, limiar 8, **difícil** repetir; scavenge/incursão hostil fora do comum segue cooldown semanal.

---

## 4. Eventos catalisadores

Disparam **1 rolagem extra** nas linhas elegíveis (impacto ≤ 3 da mesma categoria ou Social).

| Catalisador | Categorias elegíveis |
| ----------- | -------------------- |
| Ryan voltou de incursão / combate visível | Social, Combate/incursões, Oficina |
| Confronto público no acampamento | Social, Vida diária |
| Novo recruta / visitante | Social, Vida diária, Eventos especiais |
| Ferimento ou acidente | Eventos especiais, Oficina |
| Performance / celebração do pack | Social, Eventos especiais |
| Ryan isolado na oficina **> 1 dia** | Social (Valk/Reina futuro), Oficina (Tio Gringo) |
| Rumor de ameaça externa confirmado | Ameaças externas (+ ignora cooldown 1×) |

Registrar catalisador ativo no topo de `pulso_geral.md` (seção *Catalisadores ativos*, remover quando resolvido).

---

## 5. Ordem de prioridade na resolução

1. Linha com **maior impacto** que passou (resolver ameaças antes de fofoca).
2. Se empate → categoria **Ameaças** > **Eventos especiais** > **Combate** > **Social** > **Rotina**.
3. Pulso NPC com **motivação** mais urgente (`Motivações Atuais`).
4. Ganchos que **Ryan descobriria** ao acordar ou ao entrar na cena têm prioridade narrativa.

---

## 6. Integração com a IA / Narrador

**Narrador** ([diretrizes_narrador.md](diretrizes_narrador.md)):

- Ao narrar passagem de tempo (“no dia seguinte…”), declarar que o pulso diário rodou.
- Mostrar ao jogador **1–2 resquícios** do off-screen (rumor, cena breve, NPC abordando Ryan).
- Não expor todas as rolagens — só o que Ryan perceberia.

**IA gestora** ([diretrizes_ia.md](diretrizes_ia.md)):

- Atualizar arquivos de estado após o pulso.
- Não inventar fora dos pulsos + arquivos existentes.
- Se pulso contradiz `board` → ajustar pulso ou atualizar board (board prevalece).

---

## 7. Índice de pulsos

| Arquivo | Escopo |
| ------- | ------ |
| [pulso_geral.md](../pulso_do_mundo/pack_badlands/pulso_geral.md) | Tabela + clima do pack |
| [reyes.md](../pulso_do_mundo/pack_badlands/reyes.md) | Líder |
| [tio_gringo.md](../pulso_do_mundo/pack_badlands/tio_gringo.md) | Forja |
| [sasha_e_lira.md](../pulso_do_mundo/pack_badlands/sasha_e_lira.md) | Jovens do pack |
| [criancas.md](../pulso_do_mundo/pack_badlands/criancas.md) | Crianças |
| [recrutas.md](../pulso_do_mundo/pack_badlands/recrutas.md) | Mara, Elias, Tomas |
| [valk.md](../pulso_do_mundo/crew/valk.md) | Valk (Badlands) |
| [kaz.md](../pulso_do_mundo/crew/kaz.md) | NC / remoto |
| [alex.md](../pulso_do_mundo/crew/alex.md) | NC / futuro |
| [reina.md](../pulso_do_mundo/crew/reina.md) | NC / futuro |
| [stephania_stitch.md](../pulso_do_mundo/crew/stephania_stitch.md) | NC / remoto |
| [jax.md](../pulso_do_mundo/crew/jax.md) | NC / remoto |

**Template:** [template_pulso_npc.md](../pulso_do_mundo/template_pulso_npc.md)

---

## Referências

- [Como Atualizar Arquivos](como_atualizar_arquivos.md) · [Registro de Arquivos](registro_arquivos.md)
- [Board](../board/board_campanha.md) · [Consequências](../consequencias/consequencias_persistentes.md)
- [Pack Badlands](../facoes/pack_badlands.md)