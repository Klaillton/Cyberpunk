# Handoff atual — Continuidade para novo chat
**Gerado após:** sessão **020**  
**Próxima sessão:** **021** → `logs/sessao_resumo_021.md`  
**Data in-game ao fechar:** ~29 de Julho de 2026 · início da tarde  
**Branch canônica:** `feature/linha-estavel`  
**Última atualização deste handoff:** 18 de Agosto de 2026

> **Primeiro arquivo a ler:** `logs/context_pack_atual.md`  
> **Arco L1 + off-screen:** `board/arco_ativo.md`  
> **Ambiente / ganchos:** `sistema/cena_ambientacao_ganchos.md`  
> **Canon:** repo/RAW > handoff > memória de chat  

---

## Links rápidos

| Recurso | URL |
| ------- | --- |
| Context pack (RAW) | https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/context_pack_atual.md |
| Sessão 020 | logs/sessao_resumo_020.md |
| Handoff (RAW) | https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/handoff_atual.md |
| Arco ativo | https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/board/arco_ativo.md |
| Board | https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/board/board_campanha.md |
| Ambientação | https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/sistema/cena_ambientacao_ganchos.md |
| Procedimento novo chat | https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/sistema/novo_chat_procedimento.md |

---

## Boot (ordem de leitura)

1. `logs/context_pack_atual.md`  
2. `sistema/fatos_duros.md` (dúvida de fato)  
3. Este handoff  
4. `board/arco_ativo.md` se E015/canal/estagnação  
5. Board se divergir  

**Confirmação (1 linha):**
```
Boot OK · ~29/07/2026 tarde · Pack Badlands · prioridade: teste módulo + voo Condor 30/07 + possível 1º pacote ad · próximo resumo: 021 · Ruleset 1.3.0
```

---

## Estado atual (snapshot)

| Campo | Valor |
| ----- | ----- |
| Data | **~29/07/2026**, início da tarde |
| Local | Pack Badlands (oficina → refeitório) |
| Pessoas | Ryan + Valk (Pack); Lira + Sasha residual positivo |
| Drones | Vespas + Warden com Ryan; Condor/Corujas no Pack |
| Canais | **Lina Park (Sparrow):** residual sem ACK; **Marcus Rivera (Steel):** mudo; Kaz off-screen |
| Ryan × Valk | Acordo 019 em vigor + intimidade muito reforçada (020) |
| Módulo Condor | Hardware pronto (mochila sinal); 2 ajustes menores; falta Agent temp + teste integrado |
| Janela | Condor reservado 30/07 15h–17h (Tio Gringo) |
| Ad | Anônimo no ar; 1º pacote esperado em breve |
| Ruleset | **v1.3.0** |

### Cena de abertura
**Pack — tarde 29/07 / manhã 30/07.**  
Módulo na bancada. Ajustes menores + teste integrado pendentes. Voo amanhã 15h–17h.  
Gancho: o que Ryan faz até a janela / teste agora?

### AGENDA
1. Teste integrado + ajustes do módulo.  
2. Voo Condor 30/07 + possível 1º pacote ad.  
3. Residual Sparrow / Pack rotina.

---

## O que acabou de acontecer (020)

- Plano do módulo de sinal aceito por Valk (acordo 019 praticado).  
- Condor reservado com Tio Gringo (30/07 15–17h).  
- Construção completa do hardware (alumínio + couro + SDR adaptado + ventilação + placa reconstruída).  
- Dry-fit ok (2 notas menores).  
- Intimidade forte noite 28→29 + manhã 29.  
- Ideia bola-assistente Reyes registrada (futuro / tempo livre).

Detalhe: [sessao_resumo_020.md](sessao_resumo_020.md)

---

## Pendências quentes

| ID | Evento |
| -- | ------ |
| **E015** | Ad ativo; coleta via Condor preparada; residual Sparrow; Steel mudo |
| Módulo | Teste integrado + Agent temp + 2 ajustes |
| Ad | 1º pacote ~30/07 |
| E011 / E019 / E012 | Background |

---

## Regras duras (boot)

| ID | Regra |
| -- | ------ |
| F03 | Warden **não voa** |
| F04 | Stitch ≠ Doc Moreau |
| F15 | Valk **não** “herói” |
| F18 | Ruleset **1.3.0**; sem retcon 001–016 |
| F19 | Agents ≠ Warden |
| F20 | Sparrow = Lina Park (NPC); Steel = Marcus Rivera (NPC) |
| Motor | N1–N11: sem eco; delta ≥60%; AMBIENTE em local novo; SHOW relacional |

---

## Prompt de abertura (copiar no novo chat)

```markdown
# Cyberpunk RED — Continuidade (Sessão 021)

## Boot (tier-0)
- Repo: https://github.com/Klaillton/Cyberpunk · branch `feature/linha-estavel`
- Canon = arquivos do repo após sync / RAW
- Leia primeiro: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/context_pack_atual.md
- Resumo 020: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/sessao_resumo_020.md
- Handoff: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/logs/handoff_atual.md
- Arco L1: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/board/arco_ativo.md
- Ambientação: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/sistema/cena_ambientacao_ganchos.md
- Procedimento: https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/sistema/novo_chat_procedimento.md

## Mecânica
- Ruleset **1.3.0** (F18); loadout sob demanda; sem inventar mods

## Estado
- **~29/07/2026 tarde** · Pack Badlands
- Ryan + Valk (acordo 019 + intimidade 020 reforçada)
- Módulo sinal Condor: hardware pronto; falta teste integrado + Agent temp
- Janela Condor: **30/07 15h–17h** (Tio confirmou)
- Ad anônimo no ar; 1º pacote esperado em breve; residual **Lina Park** sem ACK; **Marcus Rivera** mudo
- Ideia bola-assistente Reyes = conceito futuro

## Cena
Pack. Preparação ops. **SHOW** residual se NPCs falarem. Gancho: teste do módulo / o que Ryan faz até a janela de amanhã?

## Narração
- N1–N11 · delta ≥60% · sem eco de mood/abraço
- Confirme boot em **1 linha** e aguarde o jogador.
```
