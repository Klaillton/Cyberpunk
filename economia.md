# Economia Persistente

**Última atualização:** 2026-08-02 in-game / 2026-08-31 real (pós-024 · sem delta cash)

> **Dinheiro / macro** = seções abaixo.  
> **Micro-recursos** = [Atores · Estoque · Ryan mínimo](#atores-produtores--consumidores).  
> Consulta: `[Estoque]` — [comandos_jogador.md](sistema/comandos_jogador.md) § K.  
> **Não** carregar ledger inteiro no tier-0.

## Situação Financeira - Ryan "Wireghost" Voss

| Item | Valor / Status | Observações |
| ---- | -------------- | ----------- |
| **Eddies (eb) em mãos** | **~1.200–3.700 eb** *(estimado após débito)* | Débito de **300 eb** (ad anônimo, 3 dias × 100) aplicado em 30/07 (sessão 021). Valor base ainda estimado. |
| Dívidas | Nenhuma registrada | — |
| Contratos pendentes | **Ad anônimo (E015)** — 100 ed/dia | Fixer 2º escalão; pacote de respostas a cada **3 dias**; renovável. 1º pacote coletado 30/07; **1º débito (300 eb) pago**. |
| Custos operacionais | Baixos no Pack | Hospedagem × trabalho técnico |
| Lifestyle atual | Pack (subsistência + oficina) | Em NC: ver [Lifestyle](#lifestyle-atalho-red) |

### Lifestyle (atalho RED)

| Nível | Custo mensal (ordem de grandeza) | Notas campanha |
| ----- | -------------------------------- | -------------- |
| Kibble / street | ~100–500 eb | Sobrevivência |
| Pack Badlands | ~0 eb cash (trabalho) | Estado atual de Ryan |
| Average NC | ~1.000–2.500 eb | Safehouse barato, comida |
| Comfortable | ~3.000–5.000+ eb | Exige job/Kaz |

Regras de compra/venda genéricas: DV Trading/Streetwise se risco; preço × disponibilidade.

## Economia do Pack de Badlands

| Item              | Status                           | Impacto de Ryan                 |
| ----------------- | -------------------------------- | ------------------------------- |
| Autonomia técnica | Em crescimento forte             | Linha de produção + ensino na oficina |
| Defesa            | Fortemente melhorada             | Perímetro + Mule + cerca **concluída** + **Condor/Corujas** |
| **Badlands Node** | Protótipo em progresso           | Biodigestor + filtragem; recrutas com autonomia |
| Destilaria        | Elias responsável autônomo       | Excedente + higiene/óleos (ver § Estoque) |
| Materiais         | Depósito reforçado               | Scavs 05/07 + 10/07; **chrome/componentes torre** 16–17/07 |
| **Casas modulares** | Protótipo externo OK; interno modelagem | E014: produção aprovada; revelação pública adiada (E012) |
| **Drones miméticos** | Condor + Corujas operacionais | Valor operacional (alerta 15–40 min); demo 20/07 |
| **Módulo de sinal Condor** | Operacional (021) | 1º pacote coletado; refrigerado; **no ar** 02/08 |

## Observações Econômicas Gerais

- Ryan está trocando **trabalho técnico** por hospedagem e proteção no Pack.
- **Ad anônimo:** 1º débito de 300 eb aplicado (30/07). Próximos débitos conforme renovação.
- O Pack está ganhando autonomia técnica; time de produção conhece o projeto de casas modulares (aguarda aprovação Reyes para revelação geral).

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

| ID | Item | Onde (região · local) | Guardião | Qtd | Origem | Notas |
| -- | ---- | --------------------- | -------- | --- | ------ | ----- |
| P001 | Sabonetes artesanais (destilaria) | Badlands · Pack (higiene comum) | A-PCK / A-ELI | alguns | ~004–005 | Produção local |
| P002 | Óleo aromático (laranja + alecrim) | Badlands · tenda Ryan & Valk | A-RYA | pouco | 005 (02/07) | Uso pessoal |
| P003 | Chrome / componentes eletrônicos (torre) | Badlands · Pack · depósito/oficina | A-RYA / A-OFC | bastante | 012 (16–17/07) | Material Condor/Corujas |
| P004 | Material estrutural scav (chapas/containers) | Badlands · Pack · depósito | A-OFC / A-PCK | bastante | 010–011 | Casas / cerca |
| P005 | Látex/polímero (teste enxame) | Badlands · destilaria (pedido) | A-ELI | nenhum ainda | 014 | Sob demanda |
| P006 | Resina/seiva (teste enxame) | Badlands · estufa (pedido) | A-MAR | nenhum ainda | 014 | Sob demanda |
| P007 | Módulo de sinal Condor | Badlands · oficina / Condor | A-RYA | 1 (protótipo) | 020–022 | Operacional e refrigerado; **no ar** 02/08 |

### Histórico / esgotado

| ID | Item | Notas |
| -- | ---- | ----- |
| — | *(vazio)* | Mover linhas esgotadas para cá em vez de apagar |

---

## Ryan — estoque mínimo e itens soltos

**Loadout tático / chrome / drones nomeados** → [ryan_loadout.md](fichas/ryan_loadout.md).

### Mínimo em corpo / marcha

| Item | Qtd | Notas |
| ---- | --- | ----- |
| Bolsa de ferramentas + kit de reparo | 1 | Ficha § Outros |
| Componentes básicos p/ drones | pouco | reparo de campo |
| Agent stack WIREGHOST | Honeypot · Profissional · Vault | F19 |
| Máscara tática meia-face | 1 | quase sempre |
| Vespas + Warden | loadout | F03 F12 |

### Oficina / depósito pessoal (Pack)

| Item | Qtd | Notas |
| ---- | --- | ----- |
| Sobras chrome/componentes | alguns | P003 |
| Enxame mini-drones | — | só ideia 014 |

### Compartilhado tenda / uso pessoal

| Item | Qtd | Notas |
| ---- | --- | ----- |
| P002 Óleo aromático | pouco | ver § Estoque |

---

## Referências

- [Board](board/board_campanha.md) · [Consequências](consequencias/consequencias_persistentes.md) · [Dashboard](sistema/dashboard_contexto.md)
- [Ficha Ryan](fichas/techie%20-%20ryan_wireghost_voss.md) · [Downtime](logs/downtime_ryan.md) · [Sessão 021](logs/sessao_resumo_021.md)
- Relacionados: [Reputação](reputacao.md) · [Heat](heat.md) · [Event Queue](event_queue.md)
- [Pack Badlands](facoes/pack_badlands.md) · Comando: [comandos_jogador.md](sistema/comandos_jogador.md) § K
