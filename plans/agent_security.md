# Projeto WIREGHOST — Arquitetura de Agents (OPSEC)

## Sistema de comunicação e defesa pessoal em camadas

| Campo | Valor |
| ----- | ----- |
| **Status** | `active` (padrão operacional de Ryan) |
| **Tipo** | **In-fiction** — projeto Techie / OPSEC do personagem |
| **Responsável** | Ryan “Wireghost” Voss |
| **Classificação** | Privado / Restrito |
| **SoT formalizado** | 2026-08-07 |
| **Canon temporal** | Arquitetura **já era padrão** pós-Arasaka; spec escrita agora. Sessões **≤016** não são reescritas. **≥017** usa este doc explicitamente. |

**Não é** security de agents de IA / repo / MCP.  
**Não confundir:** **Arbiter** (política de Agents) ≠ **Warden** drone terrestre (**F03**).

**Objetivo:** comunicação resiliente por separação de funções, isolamento de risco e coleta controlada de inteligência.

**Mecânica de mesa:** [08_techie](../sistema/regras_red/08_techie.md) · [10_netrunning](../sistema/regras_red/10_netrunning.md) · loadout [ryan_loadout.md](../fichas/ryan_loadout.md) · **F19** [fatos_duros](../sistema/fatos_duros.md).

---

# 1. Filosofia

> "Nem toda conexão precisa ser protegida. Algumas conexões simplesmente não devem existir."

Ryan é paranóico com corps e extremamente criativo como Maker. O Vault é desenhado para o **máximo de segurança que o Cyberpunk RED permitir**, com **desconexão de rede como requisito não negociável** em estado normal.

Objetivos:

- reduzir superfície de ataque;
- limitar blast radius se algo cair;
- detectar intrusão;
- transformar ataque em **inteligência**;
- manter críticos **isolados**.

Risco residual (falha crítica, corpo capturado, black ICE hostil) **existe** — o design minimiza dano, não invoca imunidade narrativa.

Nenhum dispositivo tem o mesmo nível de confiança.

---

# 2. Arquitetura

```text
                    ARBITER
         (política / validação de confiança)
                       |
        +--------------+--------------+
        |              |              |
     VAULT       PROFISSIONAL      HONEYPOT
    (seguro)     (operacional)   (inteligência)
```

| Unidade | Função | Risco aceito | Resposta típica |
| ------- | ------ | ------------ | --------------- |
| **Vault** | Segredos, identidade, Pack, médico, chaves | Mínimo (air-gap) | Isolar / matar sessão |
| **Profissional** | Trabalho, contatos, pesquisa, ops | Moderado | Defesa + isolamento |
| **Honeypot** | Isca + auditoria de atacantes | Controlado | Observar + log + canary |
| **Arbiter** | Regras de quem fala com quem | — | Drop de links proibidos |

---

# 3. Vault

## Função

Dispositivo / módulo principal de identidade e dados críticos. Extensão digital do Ryan — **não** fica online “por costume”.

## Princípio

> "Se existe dúvida, a conexão não existe."

O Vault não tenta “ganhar” uma invasão prolongada: **evita continuidade**.

## Estado normal

- **Offline** / air-gap.  
- Sem conexão permanente com redes externas.  
- Acesso só: solicitado + autorizado + função específica.  
- Após uso: sessão encerrada, estado de isolamento.

## Dados (níveis L3–L4 — ver §8)

- Identidade profunda; contatos prioritários; chaves; médico; projetos críticos; **info do Pack**; backups; sensíveis.

## Camadas de segurança

1. **Isolamento** — anomalia → cortar / bloquear (prioridade #1).  
2. **Defesa ativa** — gray ICE / detecção / anti-intrusão (segunda linha).  
3. **Desconexão total** — comprometimento confirmado → fim de sessão, sem negociar.

> Nenhuma informação no Vault vale manter um link comprometido.

### Black ICE (realista na campanha)

- **Não** carrega black ICE ofensivo permanente como gadget de rua (Heat / Netwatch).  
- Programas **gray** fortes + kill-session.  
- Opcional: black ICE de **último recurso** só com Vault jacked, **1 uso**, custo alto (ruído, trace, HL) — Maker consciente.

### Neural Link (mitigação)

O **Neural Link não substitui** um Agent completo (comms de rua, apps, UI). Ele é o **barramento**:

| Peça | Papel |
| ---- | ----- |
| Neural Link | Auth, UI de sessão, token de unlock (**só sob autorização**) |
| Vault (hardware/store isolado) | Dados L3–L4; bolso blindado / baú físico; **sem rádio** |
| Híbrido leve | Chaves/token no neural; blob cifrado no Vault |

Se o neural for comprometido: **desliga** sessão Vault; Vault permanece air-gapped se não reabriu.  
**Evitar** “Vault só dentro da cabeça” como default (um jack hostil leva o cofre).

---

# 4. Profissional (operacional)

## Função

Agent de **trabalho diário**: contatos, pesquisa, serviços, ops técnicas, comunicação externa.

## Princípio

> "O risco é aceitável quando necessário, mas sempre controlado."

## Conectividade

Conectado com frequência; monitora, valida, registra suspeita, isola se preciso.

## Resposta a ataques

```text
Suspeita → Análise → Contra-medidas → Comprometido? → Isolamento
```

Quando defesa pesada é necessária, o link **deixa de ser confiável**.

### Defesa realista

Firewall, detect, isolate, anti-malware; logs para o **Arbiter**. Sem black ICE de bolso como default.

## Integração com Vault (patch pipeline)

```text
Ameaça / update no Profissional
    → análise e teste
    → correção validada
    → sync one-shot para Vault (cabo / NFC / contato — ver §7)
```

O Vault **nunca** recebe alteração não testada no Profissional.

---

# 5. Honeypot (inteligência)

## Função

Sistema feito para ser **alvo**. Objetivo: invasão **controlada** → inteligência.

## Aparência (“banco shadow”)

Deve parecer o dispositivo “certo”, **sem clonar o Vault real**.

| Aspecto | Honeypot | Vault / real |
| ------- | -------- | ------------ |
| Skin / apps | Wireghost de rua, crível, um pouco mais “barulhento” | Minimal, offline |
| **Estrutura** de dados | Taxonomia **estilo rede bancária** (contas, KYC fake, ledgers, logs de “transação”) | Estrutura real diferente e mais pobre publicamente |
| **Conteúdo** | L0–L1 **synthetic** + **canaries** | L3–L4 reais |
| Defesa na UI | “Black ICE” aparente | Gray + disconnect real |
| ID digital | Identidade **descartável** | Mínima |

Conteúdo mock: **indistinguível em estrutura** do que um cofre “valioso” teria; **nunca** Pack real, chaves reais, médico real, L3/L4.

## Segurança real

Contenção, monitoramento, gray ICE, rastreamento; black real só se investido e aceito o risco legal.

## Auditoria

Registrar: origem, método, tools, tempo, arquivos tocados, tentativas, comportamento.

## Resposta

```text
Intrusão → ambiente controlado → registro → rastreio → análise
Isolar se: sem intel útil / risco de pivot / tentativa de sair do sandbox
```

**Proibido:** rota honeypot → Vault (Arbiter drop).

---

# 6. Arbiter

Camada de **política** (software + regras nos Agents):

- valida se um link é permitido;  
- bloqueia Profissional↔Honeypot em rotina;  
- bloqueia Vault↔rede;  
- autoriza janelas curtas Vault↔Profissional / Vault↔Neural;  
- em correlação honeypot↔profissional: **incidente** → isola Profissional.

**Não** é o drone Warden. **Não** precisa ser um 4º rádio na rua — roda no Profissional + regras locais no Vault.

---

# 7. Conexões (meio × proteção)

| De → Para | Meio | Nota |
| --------- | ---- | ---- |
| Profissional ↔ rede NC | Wireless / Agent net | Monitorado |
| Honeypot ↔ rede | Wireless “sujo” | Quer ser achado |
| Vault ↔ rede | **Proibido** (normal) | Air-gap |
| Vault ↔ Profissional | **Cabo / contato / NFC one-shot** auth | Patch / sync; sessão curta |
| Vault ↔ Neural | Link **só sob auth** | UI + unlock; sem keep-alive |
| Profissional ↔ Honeypot | **Proibido** em ops normal | Só lab one-way Maker |
| Neural sozinho | Não carrega L3/L4 | Só token/UI |

Tipo de conexão **depende** da necessidade de proteção: honeypot pode viver “aberto”; Vault **só** air-gap + aberturas conscientes.

---

# 8. Matriz de vazamento (L0–L4)

Inspirado em classificação de dados / banking — **não** é o Heat Echo N0–N4, mas convive com ele.

| Nível | Nome | Onde pode existir | Se vazar |
| ----- | ---- | ----------------- | -------- |
| **L0** | Public bait | Honeypot (mock) | Boato inútil; **canary** identifica o canal |
| **L1** | Operational | Profissional | Jobs mid, rotina, contatos — dor moderada |
| **L2** | Sensitive | Profissional cifrado; raro em Vault open | Handles, rotas, chaves de job |
| **L3** | Critical | **Só Vault** offline | Pack, médico, projetos, identidade profunda |
| **L4** | Crown | Vault + handoff **físico** only | Verdade Arasaka / mapa de vida — quase nunca digital |

---

# 9. Threat model (resumo)

| Ameaça | O que quer | Resposta de design |
| ------ | ---------- | ------------------ |
| Corps (Arasaka, BT) | ID, pack, chrome | Vault offline; honeypot engaja |
| Netrunners | Jack, dados | Gray + isolate; honeypot grava método |
| Echo / media | Headline | Nunca L3 no ar; Void List separado |
| Pack curiosity | Fofoca | Profissional “limpo”; Vault não social |
| Roubo físico | Device | Wipe/auth; honeypot é o que “acham” primeiro |
| Traição / torture | Tudo | Doubt = disconnect; neural sem keep-alive no Vault |

---

# 10. Mesa RED (017+)

| Cena | Resolução |
| ---- | --------- |
| Abrir Vault | Auth + tempo; falha → sem “duelo no vault”, disconnect |
| Invasão Profissional | [10_netrunning] se jack; senão Electronics/Cybertech vs DV |
| Invasão Honeypot | Atacante obtém L0 synthetic; Ryan testa log/canary (Cybertech / com Alex) |
| Sync Vault←Profissional | Ação segura / downtime; teste se sob fogo |
| Drones | F03/F12/F16 — **separados** dos três Agents |

**Histórico ≤016:** não re-rolar. Se Agent aparecer no passado: “o profissional / o de trabalho”.

---

# 11. Princípio final

O objetivo não é um sistema impossível de invadir.

É um sistema onde:

- invasões são detectadas;  
- danos são limitados;  
- críticos ficam protegidos;  
- atacantes revelam técnicas.

> "Um sistema seguro não é o que nunca é atacado. É aquele onde um ataque nunca acontece sem consequência."

---

## Referências

- Loadout: [ryan_loadout.md](../fichas/ryan_loadout.md)  
- Maker: [08_techie.md](../sistema/regras_red/08_techie.md)  
- NET: [10_netrunning.md](../sistema/regras_red/10_netrunning.md)  
- Fatos: [fatos_duros.md](../sistema/fatos_duros.md) **F19** · drone Warden **F03**  
- Echo: [echo_exposicao.md](../sistema/echo_exposicao.md)
