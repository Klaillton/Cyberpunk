# Novo Chat — Procedimento Operacional

**Finalidade:** Abrir um chat novo sem perda de continuidade, com estado canônico no GitHub e um **handoff** colável.  
**Última atualização:** 13 de Julho de 2026  
**Playbook do comando:** [comandos_jogador.md](comandos_jogador.md) § D  
**Tier-0:** [logs/context_pack_atual.md](../logs/context_pack_atual.md)

---

## 1. Quando usar

| Gatilho | Ação |
| ------- | ---- |
| Chat longo / pesado (~80–100 msgs relevantes) | Finalizar sessão + gerar handoff + **novo chat** |
| Fim de sessão narrativo | `[Finalizar sessão e gerar resumo]` **e** atualizar handoff |
| Dessincronia entre dispositivos / instâncias Grok | Novo chat com handoff + sync da branch estável |
| Mudança de ferramenta (Grok web ↔ CLI ↔ outro) | Novo chat; **canon = arquivos**, não memória do chat antigo |
| Share Grok atualizado após sessão | Atualizar `sistema/grok_sources.json` + regenerar handoff se necessário |

**Regra absoluta:** memória de chat antigo **não é canon**. Canon = arquivos do repositório na branch `feature/linha-estavel` **após** sync.

---

## 2. Fluxo completo (fim de sessão → chat novo)

```text
[Finalizar sessão e gerar resumo]
        ↓
Atualizar arquivos de estado (board, consequencias, …)
        ↓
Commit + push em feature/linha-estavel
        ↓
Gerar / atualizar logs/handoff_atual.md  ← este procedimento
        ↓
Jogador abre chat NOVO e cola o prompt de abertura (§5)
        ↓
IA faz boot (§4) e confirma data/local/prioridade em 1 frase
        ↓
Continua a cena a partir do gancho do handoff
```

### Comandos do jogador

| Comando | Efeito |
| ------- | ------ |
| `[Finalizar sessão e gerar resumo]` | Resumo em `logs/sessao_resumo_XXX.md` + atualização de estado |
| `[Gerar handoff para novo chat]` / `[Preparar novo chat]` | Só handoff (sem necessariamente fechar a sessão) |
| `[Finalizar sessão e gerar resumo]` + pedido de handoff | Resumo + arquivos + **handoff atualizado** |

Após finalizar, a IA deve **sempre** oferecer/atualizar `logs/handoff_atual.md` se o jogador for abrir chat novo.

---

## 3. O que a IA gera no handoff

Arquivo canônico de continuidade:

| Arquivo | Papel |
| ------- | ----- |
| [`logs/context_pack_atual.md`](../logs/context_pack_atual.md) | **Tier-0** NOW + fatos em vigor (atualizar com handoff) |
| [`logs/handoff_atual.md`](../logs/handoff_atual.md) | **Único handoff vigente** — sobrescrever a cada fim de sessão |
| [`logs/handoff_template.md`](../logs/handoff_template.md) | Esqueleto estrutural (não editar com estado vivo) |
| `logs/sessao_resumo_XXX.md` | Histórico imutável da sessão que acabou |

### Conteúdo mínimo do handoff

1. **Links de boot** — repo, branch, RAW board, RAW última sessão, share Grok (se houver)
2. **Ordem de leitura** — arquivos obrigatórios
3. **Estado in-game** — data, local, período do dia, cena de abertura
4. **O que acabou de acontecer** — bullets da última sessão (sem recontar a campanha inteira)
5. **Prioridade / pendências** — `event_queue` + ganchos
6. **Projetos e NPCs quentes** — só o ativo agora
7. **Regras duras** — anti meta-game, Warden, datas canônicas, próximo `sessao_resumo_NNN`
8. **Prompt colável** — bloco pronto para o jogador colar no chat novo

**Não incluir:** spoilers de notas do narrador, segredos que NPCs não sabem expostos como “o pack já sabe”, inventário completo da campanha.

---

## 4. Boot no chat novo (IA)

Executar **nesta ordem** antes de narrar:

### 4.1 Sincronização / RAW-first

- Repo: <https://github.com/Klaillton/Cyberpunk> · Branch: `feature/linha-estavel`
- Git pull se possível; senão **RAW**  
  `https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/<caminho>`

### 4.2 Leitura obrigatória (tiers)

**Tier 0**

1. `logs/context_pack_atual.md`
2. `sistema/fatos_duros.md` (se necessário)
3. `logs/handoff_atual.md` (prompt / gancho)
4. `board/board_campanha.md` se pack e board divergirem

**Tier 1 (cena do NOW)** — poucos arquivos conforme região (Pack vs NC vs estrada); ver context pack.

**Não** carregar a biblioteca inteira no boot. Playbooks: [comandos_jogador.md](comandos_jogador.md).

### 4.3 Confirmação (1 frase)

> Boot OK · **[data]** · **[região/local]** · prioridade: **[E0XX]** · próximo resumo: `NNN`

Só então narra o gancho de abertura.

### 4.4 Share Grok (opcional)

- Shares listados em `sistema/grok_sources.json`
- Share = memória narrativa auxiliar; **em conflito, o arquivo do repo vence**

---

## 5. Prompt de abertura (padrão)

O jogador cola no chat novo o bloco **“Prompt de abertura”** de [`logs/handoff_atual.md`](../logs/handoff_atual.md).

Se o handoff estiver desatualizado, a IA deve:

1. Ler `board` + último `sessao_resumo_*` + `event_queue`
2. Regenerar `logs/handoff_atual.md` com este procedimento
3. Pedir confirmação antes de commit (salvo o jogador já ter autorizado)

### Prompt mínimo de emergência (sem handoff)

```text
Campanha Cyberpunk RED solo — Ryan "Wireghost" Voss.
Repo: https://github.com/Klaillton/Cyberpunk · branch feature/linha-estavel
Canon = arquivos do repo após sync. Leia logs/handoff_atual.md; se faltar, board + último sessao_resumo_*.
Confirme data/local/prioridade em 1 frase e continue a cena.
Sem meta-game. Warden = drone terrestre scorpion-like.
```

---

## 6. Como gerar/atualizar o handoff (checklist da IA)

Após sessão (ou sob comando `[Gerar handoff para novo chat]`):

- [ ] Confirmar número da **última** sessão (`sessao_resumo_XXX`) e da **próxima**
- [ ] Copiar data/local/prioridade de `board/board_campanha.md`
- [ ] Resumir eventos da última sessão (5–12 bullets)
- [ ] Listar pendências de `event_queue.md` (IDs ativos)
- [ ] Projetos em andamento (tabela curta)
- [ ] NPCs quentes + 1 linha cada
- [ ] Regras duras (Warden, segredos, datas)
- [ ] Cena de abertura explícita (“continuar em…”)
- [ ] Links RAW + share atual (`grok_sources.json` part mais recente)
- [ ] Escrever **Prompt de abertura** colável completo
- [ ] Sobrescrever `logs/handoff_atual.md` (não criar `handoff_011.md` em série — o vigente é sempre `_atual`)
- [ ] Atualizar `sistema/registro_arquivos.md` se for a primeira vez do procedimento
- [ ] Commit/push **somente** com confirmação do jogador (exceto se já pediu explicitamente)

---

## 7. Regras duras de continuidade

| Tema | Regra |
| ---- | ----- |
| Canon | Arquivos na branch estável > handoff > share > memória de chat |
| Datas | Usar calendário do **board** (ex.: julho/2026); corrigir datas erradas do chat Grok |
| Warden | Drone **terrestre** scorpion-like (não voador) |
| Meta-game | NPCs só sabem o que viram/ouviram in-fiction |
| Segredos | Ex.: casas modulares — só quem o jogador revelou |
| Resumos | `logs/sessao_resumo_XXX.md`; próximo número em `registro_arquivos.md` |
| GitHub | Não commit/push sem confirmação explícita (salvo pedido explícito no turno) |

---

## 8. Relação com outros procedimentos

| Momento | Procedimento |
| ------- | ------------ |
| Atualizar estado pós-sessão | [como_atualizar_arquivos.md](como_atualizar_arquivos.md) |
| Resumo estruturado | [diretrizes_ia.md](diretrizes_ia.md) § Resumo de Sessão + `logs/sessao_resumo_template.md` |
| Passou 1+ dia in-game | [pulso_procedimento.md](pulso_procedimento.md) |
| **Abrir chat novo** | **Este arquivo** + [handoff_atual.md](../logs/handoff_atual.md) |
| Boot geral da IA | [instrucoes_projeto.md](instrucoes_projeto.md) |

---

## 9. Manutenção deste procedimento

- Revisar quando mudar branch canônica, URL do repo ou estrutura de pastas.
- Ao criar o handoff, **não** duplicar o board inteiro — handoff é ponte, não source of truth.
- Se o chat novo “alucinar” estado antigo: mandar re-ler RAW do board + `handoff_atual.md`.

---

## Referências

- [Handoff atual](../logs/handoff_atual.md) · [Template handoff](../logs/handoff_template.md)
- [Instruções do Projeto](instrucoes_projeto.md) · [Diretrizes IA](diretrizes_ia.md) · [Como Atualizar](como_atualizar_arquivos.md)
- [Board](../board/board_campanha.md) · [Dashboard](dashboard_contexto.md) · [Registro](registro_arquivos.md)
- [Grok sources](grok_sources.json) · [Última sessão](../logs/sessao_resumo_010.md)
