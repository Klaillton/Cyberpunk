# Registro de Arquivos do Projeto - Cyberpunk RED

**Última atualização:** 01 de Julho de 2026

---

## Estrutura Geral do Projeto

```
cyberpunk/
├── base/                          ← PDFs de referência
│   ├── cyberpunk red.pdf
│   └── night city 2045 atlas full.pdf
│
├── board/                         ← Board oficial da campanha
│   └── board_campanha.md
│
├── consequencias/
│   └── consequencias_persistentes.md
│
├── fichas/                        ← Fichas dos personagens em Markdown
│   ├── fixer - kaz_the_broker_takahashi.md
│   ├── medtech - doc_stephania_voss.md
│   ├── netrunner - alex_specter_kane.md
│   ├── nomad - lena_valk_kane.md
│   ├── solo - jax_razor_kane.md
│   ├── solo - reina_bearclaw_morales.md
│   ├── techie - ryan_wireghost_voss.md
│   └── vehicle - the_mule.md
│
├── imagens/                       ← Imagens de referência
│   ├── fixer - kaz_the_broker_takahashi.jpg
│   ├── medtech - doc_stephania_voss.jpg
│   ├── netrunner - alex_specter_kane.jpg
│   ├── nomad - lena_valk_kane.jpg
│   ├── solo - jax_razor_kane.jpg
│   ├── solo - reina_bearclaw_morales.jpg
│   ├── techie - ryan_wireghost_voss.jpg
│   └── vehicle - the_mule.jpg
│
├── logs/
│   ├── downtime_ryan.md
│   ├── sessao_resumo_template.md
│   └── sessao_resumo_XXX.md          ← Padrão para resumos de sessão
│
├── relacionamentos/               ← Arquivos de relacionamentos
│   ├── alex_specter_kane_relacionamentos.md
│   ├── crew_relacionamentos.md
│   ├── faccao_relacionamentos.md
│   ├── lena_valk_kane_relacionamentos.md
│   ├── mapa_relacional_geral.md
│   ├── reina_bearclaw_relacionamentos.md
│   └── ryan_relacionamentos.md
│
├── facoes/                        ← Informações de facções
│   ├── faccao_template.md
│   ├── pack_badlands.md
│   └── facoes_geral.md
│
├── sistema/
│   ├── como_atualizar_arquivos.md
│   ├── dashboard_contexto.md      ← Dashboard rápido para consulta da IA
│   ├── diretrizes_narrador.md
│   └── registro_arquivos.md       ← Este arquivo
│
├── economia.md
├── event_queue.md
├── heat.md
├── reputacao.md
│
└── README.md
```

---

---

## Arquivos de Estado do Mundo

| Arquivo          | Status | Finalidade                        | Última atualização |
| ---------------- | ------ | --------------------------------- | ------------------ |
| `reputacao.md`   | Ativo  | Reputação por facção e NPC        | 30/06/2026         |
| `heat.md`        | Ativo  | Nível de exposição/perseguição    | 30/06/2026         |
| `event_queue.md` | Ativo  | Fila de eventos globais pendentes | 30/06/2026         |
| `economia.md`    | Ativo  | Estado financeiro e econômico     | 30/06/2026         |

---

## Arquivo Auxiliar para Consulta Rápida

| Arquivo                         | Status | Finalidade                                         | Última atualização |
| ------------------------------- | ------ | -------------------------------------------------- | ------------------ |
| `sistema/dashboard_contexto.md` | Ativo  | Resumo rápido das informações principais para a IA | 01/07/2026         |

---

## Observações Gerais

- O `registro_arquivos.md` é o **arquivo de referência central**.
- Os arquivos mais críticos para manter atualizados são:
  - `board_campanha.md`
  - `consequencias_persistentes.md`
  - `relacionamentos/` (principalmente `ryan_relacionamentos.md`)
  - `dashboard_contexto.md`
- **Resumos de Sessão**: Usar o padrão `sessao_resumo_XXX.md`. Antes de criar um novo resumo, verificar no repositório qual foi o último número utilizado.
- **Facções**: Informações de facções estão na pasta `facoes/`. O arquivo `facoes_geral.md` é usado para facções menores ou ainda não aprofundadas.
- O **Source of Truth** permanece nos arquivos locais do jogador.

**Última atualização deste registro:** 01 de Julho de 2026
