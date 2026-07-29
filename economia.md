# Economia Persistente

**Última atualização:** 29 de Julho de 2026 (ledger estoque §1–§3)

> **Dinheiro / macro** = seções abaixo.  
> **Micro-recursos (genérico, multi-local)** = [Atores · Estoque · Ryan mínimo](#atores-produtores--consumidores).  
> Consulta jogador: `[Estoque]` / `[Recursos]` / `[O que tem: …]` — [comandos_jogador.md](sistema/comandos_jogador.md) § K.  
> **Não** carregar este ledger inteiro no tier-0 / context pack.

## Situação Financeira - Ryan "Wireghost" Voss

| Item                | Valor / Status     | Observações                                      |
| ------------------- | ------------------ | ------------------------------------------------ |
| Dinheiro em mãos    | Moderado           | Ryan não está rico, mas também não está quebrado |
| Dívidas             | Nenhuma registrada | -                                                |
| Contratos pendentes | Nenhum             | -                                                |
| Custos operacionais | Baixos             | Está hospedado no Pack (em troca de trabalho)    |

## Economia do Pack de Badlands

| Item              | Status                           | Impacto de Ryan                 |
| ----------------- | -------------------------------- | ------------------------------- |
| Autonomia técnica | Em crescimento forte             | Linha de produção + ensino na oficina |
| Defesa            | Fortemente melhorada             | Perímetro + Mule + cerca **concluída** + **Condor/Corujas** |
| **Badlands Node** | Protótipo em progresso           | Biodigestor + filtragem; recrutas com autonomia |
| Destilaria        | Elias responsável autônomo       | Excedente + higiene/óleos (ver § Estoque) |
| Materiais         | Depósito reforçado               | Scavs 05/07 + 10/07; **chrome/componentes torre** 16–17/07 |
| **Casas modulares** | Protótipo externo OK; interno modelagem | E014 implícita; escala/revelação parcial — [sessao_resumo_012](logs/sessao_resumo_012.md) |
| **Drones miméticos** | Condor + Corujas operacionais | Valor operacional (alerta 15–40 min); demo 20/07 |

## Observações Econômicas Gerais

- Ryan está trocando **trabalho técnico** por hospedagem e proteção no Pack.
- A atualização do Mule foi feita sem custo direto para Valk (presente).
- O Pack está ganhando autonomia técnica; time de produção conhece o projeto de casas modulares (aguarda aprovação Reyes para revelação geral).
- **Badlands Node** e destilaria podem reduzir dependência externa e gerar excedente.
- Não há dívidas ou contratos pendentes registrados no momento.

**Possíveis Futuros Impactos Econômicos:**

- Protótipo de casas modulares pode reduzir custo de habitação e atrair famílias.
- Jobs futuros trazidos por Kaz podem trazer dinheiro.
- Se a Biotechnica descobrir a crew, pode gerar custos de segurança ou fuga.

---

## Atores (produtores / consumidores)

**Finalidade:** quem **pode** produzir ou consumir (capacidade). Qty de lotes → § Estoque.  
**Genérico:** qualquer região — acrescentar linhas (ex. stash NC) sem mudar o schema.

| ID | Ator | Tipo | Local padrão | Produz (capacidade) | Consome / usa | Notas |
| -- | ---- | ---- | ------------ | ------------------- | ------------- | ----- |
| A-ELI | Elias | NPC · destilaria | Badlands · Pack · destilaria | refino/processamento; **sabões**; **óleos** (c/ insumos) | matéria vegetal, scav químico | autonomia Node; [ficha](fichas/npc/elias_recruit.md) |
| A-MAR | Mara | NPC · estufa | Badlands · Pack · estufa | seiva/resina/ciclo bio-água (insumos) | água, nutrientes, tempo de cultivo | Node; [ficha](fichas/npc/mara_recruit.md) |
| A-TOM | Tomas | NPC · mecânica | Badlands · Pack · oficina/Node | protótipos mecânicos, apoio peças | sucata, tempo | sob monitoramento; [ficha](fichas/npc/tomas_recruit.md) |
| A-OFC | Oficina Pack (Tio Gringo + alunos) | facility | Badlands · Pack · oficina | metalurgia, peças, linha casas modulares | chapas, perfis, sucata | [Tio Gringo](fichas/npc/tio_gringo.md) |
| A-NOD | Badlands Node | sistema | Badlands · Pack | água tratada / biodigestão (outputs do Node) | residual orgânico, manutenção | E007 |
| A-PCK | Pack (comum) | facção | Badlands · acampamento | — (consome coletivo) | higiene, comida, peças, combustível | “o pack tem…” |
| A-RYA | Ryan | PC | móvel · oficina Pack | drones, protótipos, reparos, custom chrome | componentes, chrome scav, tempo | **≠** loadout da ficha |
| A-VAL | Valk / Mule | crew | Mule · tenda | — | munição, combustível, kit campo | equipe Valk+Mule |
| A-NC | *(placeholder NC)* | — | Night City | preencher em jobs/safehouse | — | ativar ao operar em NC |

**Qtd (faixas):** `nenhum` · `pouco` · `alguns` · `bastante` · `lote` · `esgotado` (número só se o jogo exigir).

---

## Estoque (itens / lotes)

> Atualizar no **Finalizar** se criou, consumiu, scavou ou transferiu.  
> `Onde` = região · local (genérico). Item viajou → atualizar linha.  
> Esgotado/irrelevante antigo → mover para [Histórico](#histórico--esgotado).

| ID | Item | Onde (região · local) | Guardião | Qtd | Origem | Notas |
| -- | ---- | --------------------- | -------- | --- | ------ | ----- |
| P001 | Sabonetes artesanais (destilaria) | Badlands · Pack (higiene comum) | A-PCK / A-ELI | alguns | ~004–005 / consolidação destilaria | Produção local; ausente dos resumos 004–005 — backfill jogador 29/07 |
| P002 | Óleo aromático (laranja + alecrim) | Badlands · tenda Ryan & Valk | A-RYA | pouco (uso pessoal / sobra) | 005 (02/07) | Usado intimidade 02/07 — [consequencias](consequencias/consequencias_persistentes.md); origem destilaria/insumos |
| P003 | Chrome / componentes eletrônicos (torre) | Badlands · Pack · depósito/oficina | A-RYA / A-OFC | bastante (lote scav) | 012 (16–17/07) | Material Condor/Corujas; sobras possíveis |
| P004 | Material estrutural scav (chapas/containers) | Badlands · Pack · depósito | A-OFC / A-PCK | bastante | 010–011 (05–10/07) | Casas modulares / cerca |
| P005 | Látex/polímero (teste enxame) | Badlands · destilaria (pedido) | A-ELI | nenhum ainda (combinado) | 014 | Tomas: gramas de teste sob demanda; sem pressa |
| P006 | Resina/seiva (teste enxame) | Badlands · estufa (pedido) | A-MAR | nenhum ainda (combinado) | 014 | Mara: corte controlado c/ 1 dia aviso |

### Histórico / esgotado

| ID | Item | Notas |
| -- | ---- | ----- |
| — | *(vazio)* | Mover linhas esgotadas para cá em vez de apagar |

---

## Ryan — estoque mínimo e itens soltos

**Loadout tático / chrome / drones nomeados** → [ficha Ryan](fichas/techie%20-%20ryan_wireghost_voss.md) (não duplicar aqui).  
**Aqui:** consumíveis, sobras, o que “sempre tem” ou está na oficina pessoal.

### Mínimo em corpo / marcha (sempre que sair equipado, salvo ditado contrário)

| Item | Qtd | Notas |
| ---- | --- | ----- |
| Bolsa de ferramentas + kit de reparo | 1 | Ficha § Outros |
| Componentes básicos p/ drones | pouco | reparo de campo |
| Agent | 1 | comunicação |
| Máscara tática meia-face | 1 | quase sempre |
| Vespas (Hornet, Vesper, Barbed) + Warden | loadout | ver ficha / F03 F12 |

### Oficina / depósito pessoal (Pack)

| Item | Qtd | Notas |
| ---- | --- | ----- |
| Sobras chrome/componentes (pós-torre / drones) | alguns | ligado a P003 |
| Ideia enxame mini-drones (sem lotes físicos ainda) | — | só sondagem 014; sem P-item de protótipo |

### Compartilhado tenda / uso pessoal

| Item | Qtd | Notas |
| ---- | --- | ----- |
| P002 Óleo aromático | pouco | ver § Estoque |

---

## Referências

- [Board](board/board_campanha.md) · [Consequências](consequencias/consequencias_persistentes.md) · [Dashboard](sistema/dashboard_contexto.md)
- [Ficha Ryan](fichas/techie%20-%20ryan_wireghost_voss.md) · [Downtime](logs/downtime_ryan.md) · [Sessão 012](logs/sessao_resumo_012.md)
- Relacionados: [Reputação](reputacao.md) · [Heat](heat.md) · [Event Queue](event_queue.md)
- [Pack Badlands](facoes/pack_badlands.md) · Comando: [comandos_jogador.md](sistema/comandos_jogador.md) § K
