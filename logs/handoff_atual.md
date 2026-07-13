# Handoff atual — Continuidade para novo chat

**Gerado após:** sessão **010**  
**Próxima sessão:** **011** → `logs/sessao_resumo_011.md`  
**Data in-game ao fechar:** 09 de Julho de 2026 · final da tarde  
**Branch canônica:** `feature/linha-estavel`  
**Procedimento:** [sistema/novo_chat_procedimento.md](../sistema/novo_chat_procedimento.md)  
**Playbook:** [comandos_jogador.md](../sistema/comandos_jogador.md) § D  
**Tier-0:** [context_pack_atual.md](context_pack_atual.md) · [fatos_duros.md](../sistema/fatos_duros.md)  
**Última atualização deste handoff:** 13 de Julho de 2026

> **Como usar:** abra um chat novo e cole o bloco **Prompt de abertura** (§ abaixo).  
> **Canon:** arquivos no GitHub na branch estável. **Primeiro arquivo a ler:** `context_pack_atual.md`. Este handoff é ponte, não source of truth.

---

## Links rápidos

| Recurso | URL / caminho |
| ------- | ------------- |
| Repo | https://github.com/Klaillton/Cyberpunk |
| **Context pack (RAW)** | https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/context_pack_atual.md |
| Board (RAW) | https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/board/board_campanha.md |
| Fatos duros (RAW) | https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/sistema/fatos_duros.md |
| Comandos (RAW) | https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/sistema/comandos_jogador.md |
| Sessão 010 (RAW) | https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/sessao_resumo_010.md |
| Este handoff (RAW) | https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/handoff_atual.md |
| Share part3 (auxiliar) | https://grok.com/share/c2hhcmQtMw_07808d03-3ca1-4816-8ca8-187dadfeaba9 |

---

## Estado atual (snapshot)

| Campo | Valor |
| ----- | ----- |
| Data | **09/07/2026**, final da tarde → próximo marco **10/07 manhã** |
| Local | Pack Nômade de Badlands — oficina / tenda Ryan & Valk |
| Protagonista | Ryan "Wireghost" Voss |
| Parceira | Lena "Valk" Kane (relação consolidada) |
| Prioridade | **E010 — Scav de containers** (estrutura do protótipo de casas modulares) |
| Segredo ativo | Casas modulares dobráveis — **ainda secreto** no pack |

### Cena de abertura sugerida

**Manhã de 10/07/2026 — área de saída do Pack.**  
Valk organizou o time (2–3 veículos) para a scav de **containers**. Ryan decide como partir (recon, formação, ordens).

Alternativa: fechar a noite de 09/07 na tenda se o jogador quiser roleplay antes da partida.

---

## O que acabou de acontecer (sessão 010)

- Scav de **materiais** (05/07): Valk, Rusty, Jax + 2; dois veículos; recon solo + Vespas (Hornet, Vesper, Barbed); área limpa.
- Material: chapas, perfis, tubulações, vigas, isolamento, peças mecânicas. Containers inteiros **ficaram** para 2ª viagem.
- Oficina (~05–09/07): linha de produção de peças do protótipo com alunos do Tio Gringo; propósito **não revelado**; “só Ryan”.
- Badlands Node: biodigestor + filtragem de água avançando; destilaria (Elias) / estufa (Mara) andando.
- Valk × Ryan: vínculo forte; conversa sobre eventual partida + visita à **Doc Moreau** (Elisa; Valk quer ir junto — não é Stitch).
- Fim: peças quase prontas; scav de containers marcada para **amanhã**.

Detalhes: [sessao_resumo_010.md](sessao_resumo_010.md)

---

## Pendências (event_queue)

| ID | Evento | Prioridade |
| -- | ------ | ---------- |
| **E010** | Scav de containers | Imediata (10/07) |
| E012 | Montagem protótipo + revelação controlada | Após E010 |
| E007 | Badlands Node (Água + Biodigestor) | Alta / contínuo |
| E008 | Vigilância residual Raffen (pós-torre 04/07) | Média |
| E011 | Visita à Doc Moreau (Elisa); Valk junto — não é Stitch | Médio prazo |
| E001/E006 | Biotechnica (investigação / retaliação latente) | Médio |
| E004 | Interesse de Alex em Valk | Contínuo / baixo agora |

---

## Projetos ativos

| Projeto | Status |
| ------- | ------ |
| Casas modulares dobráveis (~30→90 m²) | Peças ~prontas; falta container; **SEGREDO** |
| Badlands Node | Biodigestor + água em progresso |
| Destilaria (Elias) | Autônoma |
| Estufa (Mara) | Em progresso |
| Cerca em estrela | Pessoal mais autônomo |

---

## NPCs quentes

| NPC | Nota |
| --- | ---- |
| **Valk** | Organiza scav; cumplicidade total no projeto secreto |
| **Rusty** | Veículos / Mule |
| **Jax** | Cobertura operacional (scav anterior) |
| **Tio Gringo** | Oficina/alunos — **ainda sem saber** das casas |
| **Mara / Elias / Tomas** | Node + destilaria/estufa |
| **Reyes** | Líder; confia em Ryan |

---

## Regras duras

- Canon = arquivos `feature/linha-estavel` > handoff > share > memória de chat
- Datas: calendário do **board** (julho/2026)
- **Warden** = drone **terrestre** scorpion-like (não voador)
- Sem meta-game em NPCs
- Casas modulares: secreto até protótipo / revelação consciente do jogador
- Próximo resumo: `logs/sessao_resumo_011.md`
- Não commit/push sem confirmação explícita do jogador

---

## Prompt de abertura (copiar e colar no chat novo)

```markdown
# Cyberpunk RED — Continuidade (Sessão 011)

## Boot obrigatório (tiers — não carregue a campanha inteira)
- Repo: https://github.com/Klaillton/Cyberpunk · Branch: `feature/linha-estavel`
- Hierarquia: **RAW/repo > sandbox > memória de chat**
- **Tier-0 (sempre):** context pack → fatos duros → board se divergir
  - https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/context_pack_atual.md
  - https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/sistema/fatos_duros.md
  - https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/sistema/comandos_jogador.md
- Handoff: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/handoff_atual.md
- Board: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/board/board_campanha.md
- Sessão 010: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/sessao_resumo_010.md
- Share (auxiliar, não canon): https://grok.com/share/c2hhcmQtMw_07808d03-3ca1-4816-8ca8-187dadfeaba9

Leia nesta ordem:
1. `logs/context_pack_atual.md` + `sistema/fatos_duros.md`
2. `logs/handoff_atual.md` (este prompt / gancho)
3. `board/board_campanha.md` se necessário
4. Tier-1 da cena (Badlands agora): `event_queue.md`, `relacionamentos/ryan_relacionamentos.md` (+ Valk se em cena)
5. Comandos: seguir `sistema/comandos_jogador.md` à risca

---

## Quem somos
- **Protagonista (jogador):** Ryan "Wireghost" Voss — Techie/operador
- **Parceira:** Lena "Valk" Kane — amor mútuo, relação consolidada
- **Tom:** Cyberpunk RED, Badlands, pack nômade. Alterna Techie carinhoso ↔ operador frio
- **Warden:** drone terrestre scorpion-like (**não** voador)
- **Anti meta-game:** NPCs só sabem o que estavam presentes ou o que lhes foi dito

---

## Estado atual (in-game)
- **Data:** 09/07/2026 final da tarde → **abrir em 10/07/2026 manhã** (scav)
- **Local:** Pack Nômade de Badlands
- **Prioridade:** E010 — scav de **containers** para protótipo de casas modulares (ainda **SEGREDO** no pack)
- Peças usinadas do protótipo quase prontas; material estrutural da scav 05/07 no depósito; containers inteiros pendentes

---

## O que acabou de acontecer (sessão 010 — resumo)
- Scav de materiais limpa (Valk, Rusty, Jax + 2; recon solo + drones)
- Linha de produção na oficina (alunos / Tio Gringo sem saber o propósito final)
- Node + destilaria/estufa avançando
- Valk × Ryan: forte; visita à Doc Moreau (Elisa) prometida (Valk quer ir junto)
- Combinaram scav de containers para o dia seguinte

---

## Pendências principais
1. Scav de containers (10/07) — Valk organiza 2–3 veículos
2. Montagem do 1º protótipo de casa modular
3. Revelar plano a Tio Gringo / equipe quando ~98% + containers
4. Visita à Doc Moreau (Elisa); vigilância residual Raffen; Node contínuo

---

## Comece a narrar
Confirme boot (1 frase: data, local, prioridade, próximo resumo `011`) e continue a partir de:

**Manhã de 10/07/2026 — área de saída do Pack. Valk preparou o time para a scav de containers. Ryan decide como partir.**

Aguarde a ação do jogador.
```

---

## Prompt mínimo (emergência)

```text
Campanha Cyberpunk RED solo — Ryan "Wireghost" Voss.
Repo: https://github.com/Klaillton/Cyberpunk · branch feature/linha-estavel
Canon = arquivos do repo. Leia logs/handoff_atual.md + board + sessao_resumo_010.
Data alvo: 10/07/2026 manhã · scav de containers (E010) · casas ainda SEGREDO.
Warden = drone terrestre scorpion. Sem meta-game.
Confirme boot em 1 frase e continue.
```

---

## Referências

- [Novo chat — procedimento](../sistema/novo_chat_procedimento.md) · [Template](handoff_template.md)
- [Sessão 010](sessao_resumo_010.md) · [Board](../board/board_campanha.md) · [Dashboard](../sistema/dashboard_contexto.md)
- [Event queue](../event_queue.md) · [Como atualizar](../sistema/como_atualizar_arquivos.md)
