# Context Pack — Template

> Copiar para `logs/context_pack_atual.md` e preencher. Alvo: **≤ ~120 linhas / ~4 KB**.  
> Procedimento: [sistema/comandos_jogador.md](../sistema/comandos_jogador.md) · Fatos: [sistema/fatos_duros.md](../sistema/fatos_duros.md)

**Gerado após sessão:** `NNN` · **Próxima:** `NNN+1` · **Branch:** `feature/linha-estavel`

---

## NOW (location-agnostic)

| Campo | Valor |
| ----- | ----- |
| Data in-game | |
| Período do dia | |
| Região | Badlands / Night City / Estrada / Outro |
| Local específico | |
| Facção / base local | |
| Cena / gancho | |
| Prioridade | E0XX ou livre |
| Segredos ativos | |

---

## Fatos duros em vigor

Citar IDs de `sistema/fatos_duros.md` (F01–F13 + L0x se aplicável):

- F03, F04, F11, …
- L0x: …

---

## Pendências quentes (event_queue)

| ID | Uma linha |
| -- | --------- |
| | |

---

## Carga de contexto

| Tier | Quando | Arquivos |
| ---- | ------ | -------- |
| **0** | Sempre / refresh | Este pack → `fatos_duros` → `board` se pack suspeito |
| **1** | Cena atual | *preencher conforme região* |
| **2** | Sob demanda | via `registro_arquivos.md` |

### Tier-1 sugerido para ESTE snapshot

- …

---

## RAW (se sandbox falhar)

Base: `https://raw.githubusercontent.com/Klaillton/Cyberpunk/feature/linha-estavel/`

- `logs/context_pack_atual.md`
- `board/board_campanha.md`
- `sistema/fatos_duros.md`
- `logs/handoff_atual.md`
- `event_queue.md`
- último `logs/sessao_resumo_XXX.md`

---

## Confirmação de boot (formato fixo)

```
Boot OK · [data] · [região/local] · prioridade: [E0XX] · próximo resumo: NNN
```

Hierarquia: **RAW/repo > sandbox > memória de chat**.
