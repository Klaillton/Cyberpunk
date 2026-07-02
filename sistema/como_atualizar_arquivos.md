# Como Atualizar os Arquivos da Campanha

Este arquivo serve como referência rápida para manter os arquivos da campanha atualizados de forma organizada, especialmente quando a campanha está espalhada em vários chats.

---

## Fluxo Recomendado

### Regra Principal

Sempre seja o mais específico possível sobre **qual arquivo** você quer atualizar.

Quanto mais específico você for, menor o risco de inconsistências.

### Ordem de Prioridade

1. **Chats atuais / recentes** → Use comandos específicos (nome do arquivo).
2. **Chats antigos ou longos** → Peça primeiro um **resumo das atualizações** antes de aplicar.
3. **Sempre que possível** → Peça para eu mostrar as mudanças propostas antes de confirmar.

---

## Comandos Recomendados

### Comando Genérico (bom para chats antigos)

"Analise este chat e atualize os arquivos da campanha conforme o que aconteceu.
Atualize Board, Consequências Persistentes, Relacionamentos relevantes e Downtime se aplicável.
Se tiver dúvidas ou precisar de mais contexto antes de aplicar as mudanças, me pergunte primeiro."

### Templates Prontos (mais seguros)

| Finalidade                               | Comando                                                                                                                                                                                  |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Atualização geral de sessão**          | `Com base neste chat, atualize o Board e as Consequências Persistentes com o que aconteceu. Depois me mostre um resumo das mudanças propostas.`                                          |
| **Foco em Relacionamentos**              | `Analise este chat e atualize os arquivos de relacionamentos (ryan_relacionamentos.md, crew_relacionamentos.md, faccao_relacionamentos.md) com as interações e mudanças que ocorreram.`  |
| **Foco em Downtime**                     | `Atualize o downtime_ryan.md com as atividades que Ryan realizou nesse período.`                                                                                                         |
| **Atualização completa (com segurança)** | `Faça uma análise completa deste chat e proponha atualizações para Board, Consequências, Relacionamentos, Downtime, sugira outros arquivos a serem atualizados/criados. Só aplique depois que eu confirmar.`                                |
| **Chats muito antigos / confusos**       | `Leia este chat antigo e extraia os eventos importantes que ainda não estão registrados nos arquivos da campanha. Me mostre um resumo primeiro.`                                         |
| **Resumo rápido**                        | `[Faça um resumo do que precisa ser atualizado nos arquivos após essa sessão, liste tbm em quais arquivos ocorrerão essas atualizações; Me mostre o resumo antes de qualquer alteração]` |

---

## Boas Práticas

### 1. Sempre mencione o nome do arquivo quando possível

Exemplos bons:

- `Atualize o board_campanha.md com...`
- `Adicione no ryan_relacionamentos.md o seguinte...`
- `Atualize o consequencias_persistentes.md com o evento...`

### 2. Peça resumo antes de aplicar (especialmente em chats antigos)

Comando recomendado:

> “Faça um resumo do que precisa ser atualizado nos arquivos e depois aplique as mudanças.”

### 3. Para chats muito longos ou antigos

Use este fluxo:

1. Peça um resumo primeiro.
2. Revise o resumo.
3. Confirme para eu aplicar as mudanças.

### 4. Atualização em lote

Você pode pedir para atualizar vários arquivos de uma vez:

> “Atualize o Board, as Consequências e os Relacionamentos com base no que rolou nessa sessão.”

### 5. Quando estiver em dúvida

Peça:

> “Me ajude a identificar o que precisa ser atualizado nos arquivos depois dessa sessão.”

---

## Estrutura de Pastas (Referência Rápida)

cyberpunk/
├── base/                          ← PDFs de referência
│   ├── cyberpunk red.pdf
│   └── night city 2045 atlas full.pdf
├── board/                         ← Board oficial da campanha
│   └── board_campanha.md
├── consequencias/
│   └── consequencias_persistentes.md
├── fichas/                        ← Fichas dos personagens em Markdown
│   ├── fixer - kaz_the_broker_takahashi.md
│   ├── medtech - doc_stephania_voss.md
│   ├── netrunner - alex_specter_kane.md
│   ├── nomad - lena_valk_kane.md
│   ├── solo - jax_razor_kane.md
│   ├── solo - reina_bearclaw_morales.md
│   ├── techie - ryan_wireghost_voss.md
│   └── vehicle - the_mule.md
├── imagens/                       ← Imagens de referência
│   ├── fixer - kaz_the_broker_takahashi.jpg
│   ├── medtech - doc_stephania_voss.jpg
│   ├── netrunner - alex_specter_kane.jpg
│   ├── nomad - lena_valk_kane.jpg
│   ├── solo - jax_razor_kane.jpg
│   ├── solo - reina_bearclaw_morales.jpg
│   ├── techie - ryan_wireghost_voss.jpg
│   └── vehicle - the_mule.jpg
├── logs/
│   ├── downtime_ryan.md
│   ├── sessao_resumo_template.md
│   └── sessao_resumo_XXX.md          ← Padrão para resumos de sessão
├── relacionamentos/               ← Arquivos de relacionamentos
│   ├── alex_specter_kane_relacionamentos.md
│   ├── crew_relacionamentos.md
│   ├── faccao_relacionamentos.md
│   ├── lena_valk_kane_relacionamentos.md
│   ├── mapa_relacional_geral.md
│   ├── reina_bearclaw_relacionamentos.md
│   └── ryan_relacionamentos.md
├── facoes/                        ← Informações de facções
│   ├── faccao_template.md
│   ├── pack_badlands.md
│   └── facoes_geral.md
├── sistema/
│   ├── como_atualizar_arquivos.md
│   ├── dashboard_contexto.md      ← Dashboard rápido para consulta da IA
│   ├── diretrizes_narrador.md
│   └── registro_arquivos.md       ← Este arquivo
├── economia.md
├── event_queue.md
├── heat.md
├── reputacao.md
└── README.md

---

## Dica Final

- **Chats atuais**: Seja específico.
- **Chats antigos**: Peça resumo primeiro.
- **Sempre**: Eu mostro as mudanças propostas antes de você confirmar a aplicação final nos seus arquivos locais.

Manter esse hábito evita bagunça e inconsistências conforme a campanha cresce.
