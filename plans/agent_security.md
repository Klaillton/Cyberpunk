# Projeto WIREGHOST — Arquitetura de Agents (OPSEC)

## Sistema de comunicação, defesa pessoal e deception em camadas

| Campo               | Valor                                                                                                                   |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Status**          | `active` — padrão operacional de Ryan                                                                                   |
| **Tipo**            | **In-fiction** — projeto Techie / OPSEC do personagem                                                                   |
| **Responsável**     | Ryan “Wireghost” Voss                                                                                                   |
| **Classificação**   | Privado / Restrito                                                                                                      |
| **SoT formalizado** | 2026-08-08                                                                                                              |
| **Canon temporal**  | Arquitetura já era padrão pós-Arasaka; especificação formalizada posteriormente. Sessões anteriores não são reescritas. |

**Não é** security de Agents de IA / repo / MCP.
**Não confundir:** **Arbiter** / **Watchdog** (política de Agents) ≠ **Warden** drone terrestre (**F03**).

**Objetivo:** comunicação resiliente por separação de funções, isolamento de risco, validação de trajetória, deception e coleta controlada de inteligência.

**Mecânica de mesa:** [08_techie](../sistema/regras_red/08_techie.md) · [10_netrunning](../sistema/regras_red/10_netrunning.md) · loadout [ryan_loadout.md](../fichas/ryan_loadout.md) · **F19** [fatos_duros](../sistema/fatos_duros.md).

---

# 1. Filosofia

> "Nem toda conexão precisa ser protegida. Algumas conexões simplesmente não devem existir."

Ryan é extremamente cauteloso com corporações, redes e qualquer sistema que possa comprometer sua autonomia.

A segurança não depende de uma única defesa.

O sistema parte da premissa de que:

- qualquer segredo pode eventualmente vazar;
- qualquer dispositivo pode eventualmente ser comprometido;
- qualquer chave pode eventualmente ser capturada;
- qualquer defesa pode eventualmente falhar;
- uma conexão comprometida nunca deve ser tratada como confiável apenas porque continua produzindo respostas criptograficamente válidas;
- a identidade física de um dispositivo não deve revelar sua função real.

O objetivo é:

- reduzir superfície de ataque;
- limitar blast radius se algo cair;
- detectar intrusão;
- diferenciar autenticação de confiança;
- validar não apenas **o que** foi apresentado, mas **como, quando e por qual caminho**;
- transformar ataques controlados em inteligência;
- manter dados críticos isolados;
- impedir que observadores externos saibam qual Agent Ryan realmente utiliza.

> **Segredo pode vazar. O protocolo não pode.**

A arquitetura utiliza três Agents com diferentes funções, níveis de exposição e tolerância a risco:

1. **Vault** — proteção absoluta;
2. **Profissional** — operação cotidiana;
3. **Honeypot** — identidade pública, deception e inteligência.

---

# 2. Arquitetura Geral

```text
                         ARBITER
              política / confiança / regras
                           |
        +------------------+------------------+
        |                  |                  |
      VAULT           PROFISSIONAL        HONEYPOT
   [implantado]       [subdermal]       [visível]
        |                  |                  |
        +------------------+------------------+
                           |
                    WATCHDOG / AUDITOR
                validação de trajetória
                e correlação de eventos
```

Os três Agents não precisam parecer relacionados.

### Aparência física

```text
VAULT
┌──────────────┐
│ pequeno chip │
│ metálico     │
└──────────────┘
     ↓
implantado no corpo/cabeça


PROFISSIONAL
┌──────────────────────┐
│ stick metálico       │
│ sem tela / controles │
└──────────────────────┘
          ↓
subdermal pocket


HONEYPOT
┌──────────────────────┐
│      AGENT comum     │
│ tela / interface     │
│ aparência convencional│
└──────────────────────┘
          ↓
dispositivo visível
```

A separação física faz parte da segurança.

Quem vê Ryan utilizando um Agent convencional pode concluir que aquele dispositivo é o sistema principal.

Essa conclusão está errada.

---

# 3. Vault

## 3.1 Função

Dispositivo / módulo principal de identidade e dados críticos.

É a extensão digital mais protegida de Ryan.

O Vault é implantado fisicamente no corpo de Ryan e sua aparência deve ser indistinguível, tanto quanto possível, de outros chips/cibernética implantados nele.

Não possui:

- tela;
- teclado;
- botões;
- alto-falante;
- interface física convencional;
- porta de comunicação exposta para uso cotidiano.

Fisicamente, ele se parece com:

> **mais um dos chips implantados em Ryan.**

A interação normal ocorre através do **Neural Link / Kiroshi**.

---

## 3.2 Princípio

> **"Se existe dúvida, a conexão não existe."**

O Vault não tenta ganhar uma invasão.

Ele não tenta descobrir primeiro o que o invasor quer.

Ele não tenta rastrear o atacante.

Ele não tenta manter uma operação importante funcionando.

### Qualquer anomalia é motivo suficiente para encerrar a conexão.

Não importa se:

- a anomalia parece pequena;
- a conexão continua funcional;
- o handshake continua válido;
- o ataque ainda não alcançou nenhum arquivo;
- Ryan está executando uma operação importante;
- a interrupção será inconveniente.

**Anomalia = perda de confiança = corte.**

---

# 3.3 Estado normal

O Vault permanece:

> **Offline / air-gapped.**

Não existe conexão permanente com redes externas.

O Vault não é um Agent de uso cotidiano.

Ele só abre uma conexão quando:

- Ryan necessita de um dado crítico;
- uma atualização previamente testada precisa ser instalada;
- uma sincronização específica foi autorizada.

Depois da operação:

```text
Conexão
   ↓
transferência
   ↓
validação
   ↓
sessão encerrada
   ↓
interface destruída
   ↓
Vault novamente isolado
```

---

# 3.4 Atualizações

O Vault nunca recebe diretamente software experimental.

O fluxo é:

```text
Desenvolvimento
      ↓
Sandbox externo
      ↓
Testes
      ↓
Agent Profissional
      ↓
Testes adicionais
      ↓
Validação
      ↓
Build aprovado
      ↓
Terceira interface
      ↓
Vault
      ↓
Conexão destruída
```

O Vault é o **último elemento da cadeia**.

Nenhuma atualização chega nele enquanto ainda estiver sendo desenvolvida ou testada.

---

# 3.5 Terceira Interface

A sincronização do Vault não utiliza diretamente:

- Honeypot;
- Agent Profissional;
- rede externa comum.

É utilizada uma terceira interface dedicada.

Ela pode ser fornecida pelo próprio **Neural Link / Kiroshi**, funcionando como uma ponte temporária e controlada.

Princípio:

> **uma interface de atualização não é uma interface permanente de comunicação.**

A conexão existe somente durante a transferência necessária.

Depois:

> **desconecta e destrói a sessão.**

---

# 3.6 Dados

Dados L3–L4:

- identidade profunda;
- contatos prioritários;
- chaves;
- dados médicos;
- projetos críticos;
- informações do Pack;
- backups;
- dados pessoais sensíveis;
- informações relacionadas à Arasaka;
- informações cuja exposição possa comprometer Ryan ou terceiros.

---

# 3.7 Segurança em camadas

### Camada 1 — Isolamento

Primeira e principal defesa.

```text
Conexão
   ↓
Monitoramento
   ↓
Anomalia detectada
   ↓
CORTE IMEDIATO
   ↓
ISOLAMENTO
```

Não existe período de observação.

Não existe "vamos ver o que ele consegue fazer".

Não existe tentativa de capturar inteligência.

---

### Camada 2 — Defesa ativa

Os programas de segurança continuam presentes:

- detecção;
- defesa;
- anti-intrusão;
- gray ICE;
- programas de contra-ataque;
- Black ICE, quando aplicável.

Eles existem como **segunda camada de proteção**.

A presença dessas defesas não muda a regra fundamental:

> **A primeira resposta à anomalia é cortar a conexão.**

---

### Camada 3 — Circuit Breaker

Caso uma anomalia seja detectada:

```text
CIRCUIT BREAKER
      ↓
sessão encerrada
      ↓
interfaces externas bloqueadas
      ↓
Vault isolado
```

Se necessário:

- sessão destruída;
- interface de rede desabilitada;
- comunicação com outros Agents interrompida;
- Vault permanece isolado.

---

# 3.8 Recuperação do Vault

Após qualquer evento de anomalia, o Vault deve ser considerado:

> **potencialmente comprometido até inspeção física.**

A recuperação pode exigir:

- diagnóstico físico;
- validação do hardware;
- reinstalação;
- restauração;
- substituição de componentes;
- autenticação física;
- intervenção Techie;
- eventual cirurgia.

Ryan aceita esse custo.

> **É preferível passar por uma mesa de cirurgia para recuperar o Vault a manter uma conexão potencialmente comprometida.**

---

# 3.9 Protocolo de destruição

O Vault é projetado para não ser recuperável por terceiros.

Se Ryan for capturado e houver risco de:

- extração do implante;
- acesso físico;
- engenharia reversa;
- interrogatório técnico;
- comprometimento das camadas de segurança;

o Vault pode entrar em protocolo de destruição.

O princípio é semelhante ao protocolo de wipeout dos drones:

```text
ameaça física confirmada
        ↓
WIPEOUT
        ↓
apagamento seguro
        ↓
destruição física do hardware
```

O objetivo final não é preservar o dispositivo.

É preservar os dados.

> **Se o Vault tiver de ser perdido para impedir uma captura, o Vault será perdido.**

---

# 3.10 Neural Link / Kiroshi

O Neural Link fornece a interface primária entre Ryan e o Vault.

A interação pode ser completamente neural:

```text
Ryan
  ↓
Neural Link / Kiroshi
  ↓
Vault
  ↓
dados / processamento
  ↓
Neural Link
  ↓
Ryan
```

Não existe necessidade de:

- tela;
- teclado;
- áudio;
- comandos vocais;
- interface física.

O Vault é essencialmente um módulo computacional blindado.

---

# 4. Agent Profissional

## 4.1 Função

É o Agent utilizado por Ryan no cotidiano.

Responsável por:

- trabalho;
- pesquisa;
- comunicação;
- contatos;
- operações técnicas;
- tarefas do Pack;
- acesso a serviços;
- processamento;
- operações de rede.

É o Agent que efetivamente "trabalha".

---

# 4.2 Forma física

O Profissional é um **stick metálico compacto**, sem necessidade de tela ou controles.

Ele pode ser armazenado em um:

> **subdermal pocket**

Quando necessário, Ryan pode removê-lo ou substituí-lo.

Nunca precisa ficar exposto na mão durante o uso.

Sua interface principal é o Neural Link.

Isso permite que Ryan pareça estar usando:

> **o Agent comum que todos conhecem**

quando, na realidade, todo o processamento importante está acontecendo através do Profissional.

---

# 4.3 Redundância

O Profissional é deliberadamente descartável.

Ryan mantém redundância suficiente para aceitar:

> **perder um Agent é inconveniente, não catastrófico.**

Se houver suspeita de comprometimento:

```text
SUSPEITA
   ↓
DESCARTA AMBIENTE REAL
   ↓
DUMMY
```

Não vale a pena arriscar a segurança para salvar hardware.

---

# 4.4 Segurança

O Profissional possui:

- firewall;
- autenticação;
- criptografia;
- proteção de memória;
- detecção de intrusão;
- gray ICE;
- Black ICE;
- programas defensivos;
- circuit breaker;
- validação de handshake;
- validação de trajetória;
- deception.

---

# 4.5 Regra de suspeita

Diferentemente de um sistema comum:

> **Suspeita já é suficiente para abandonar o ambiente real.**

O Profissional não precisa esperar confirmação absoluta.

```text
NORMAL
  ↓
ANOMALIA
  ↓
SUSPEITA
  ↓
DUMMY
```

O custo é aceitável porque Ryan possui redundância.

---

# 4.6 Dummy Mode

Ao detectar uma anomalia, o Agent abandona a representação real do ambiente.

O invasor recebe uma continuação aparentemente válida:

```text
REAL
 ↓
COMPROMETIMENTO
 ↓
CAMINHO REAL ENCERRADO
 ↓
DUMMY
```

Para o invasor:

```text
AUTHENTICATION SUCCESSFUL
SESSION ESTABLISHED
ACCESS GRANTED
```

Para Ryan:

```text
REAL SESSION TERMINATED
ATTACKER CONTAINED IN DUMMY
```

---

# 4.7 Alimentação do Honeypot

O Profissional possui uma função adicional:

> **manter o Honeypot vivo e plausível.**

Periodicamente, informações falsas e atualizadas são propagadas para o Honeypot.

Exemplos:

- novos contatos falsos;
- trabalhos recentes;
- arquivos recentes;
- históricos de comunicação;
- alterações de agenda;
- pequenos projetos;
- registros temporais;
- informações operacionais falsas;
- mudanças de rotina.

O objetivo é evitar que o Honeypot pareça:

> **uma armadilha congelada no tempo.**

Ele deve parecer um Agent real, ativo e utilizado recentemente.

---

# 4.8 O Honeypot como cobertura

O objetivo principal do Honeypot não é simplesmente capturar hackers.

Ele também serve para:

> **ocultar a existência e a importância do Profissional.**

Um observador externo deve ser capaz de concluir:

> "Esse é o Agent que Ryan usa."

E essa conclusão deve ser falsa.

O Agent visível existe justamente para tornar essa conclusão natural.

---

# 5. Honeypot

## 5.1 Função

O Honeypot é a identidade digital descartável e visível de Ryan.

Objetivos:

1. fornecer cobertura para o Profissional;
2. parecer um Agent comum;
3. servir como alvo plausível;
4. receber informações falsas recentes;
5. detectar e estudar invasores;
6. rastrear comportamento;
7. transformar intrusão em inteligência.

---

# 5.2 Forma física

Ao contrário do Vault e do Profissional, o Honeypot:

> **parece exatamente o tipo de Agent que uma pessoa esperaria encontrar.**

Pode possuir:

- tela;
- interface convencional;
- comandos;
- aparência comercial;
- identificadores;
- histórico;
- arquivos;
- contatos;
- dados simulados.

Pode ser utilizado na frente de outras pessoas.

Ryan pode segurá-lo, consultar a tela e interagir normalmente.

Isso reforça a falsa associação:

> **Honeypot = Agent de Ryan.**

---

# 5.3 Trabalho real através do Neural Link

Enquanto Ryan utiliza o Honeypot de maneira visível:

```text
OUTSIDERS
     ↓
Ryan usando Honeypot
     ↓
"Esse é o Agent dele."
```

a operação real ocorre:

```text
Ryan
 ↓
Neural Link
 ↓
Profissional
 ↓
rede / trabalho real
```

O Honeypot pode até estar exibindo informações plausíveis enquanto o trabalho verdadeiro ocorre de maneira independente.

---

# 5.4 Segurança

O Honeypot continua protegido.

Possui:

- firewall;
- detecção;
- autenticação;
- criptografia;
- gray ICE;
- Black ICE;
- programas defensivos;
- monitoramento;
- auditoria;
- rastreamento;
- deception.

A diferença é:

> **o Honeypot aceita um nível de risco que o Vault e o Profissional não aceitam.**

---

# 5.5 Dados falsos

O Honeypot contém somente dados descartáveis.

Pode conter:

- contatos falsos;
- documentos falsos;
- projetos falsos;
- históricos falsos;
- credenciais falsas;
- arquivos simulados;
- identidades descartáveis;
- canary data.

Nunca contém:

- dados reais do Pack;
- chaves reais;
- dados médicos reais;
- L3;
- L4;
- credenciais capazes de alcançar o Vault;
- credenciais capazes de comprometer o Profissional.

---

# 5.6 Dados temporalmente coerentes

O Honeypot deve parecer vivo.

Os dados falsos precisam apresentar:

- datas recentes;
- alterações recentes;
- arquivos recém-criados;
- comunicações recentes;
- pequenas inconsistências naturais;
- evolução temporal.

O objetivo é que uma invasão em agosto encontre informações que parecem ter sido produzidas em agosto.

---

# 5.7 Inteligência

O Honeypot pode permitir que um invasor continue acreditando que venceu.

Depois da detecção:

```text
INTRUSION
   ↓
PATH DEVIATION
   ↓
DUMMY BRANCH
   ↓
AUDIT
   ↓
TRACE
```

Registrar:

- origem;
- método;
- ferramentas;
- tempo de permanência;
- nós acessados;
- arquivos consultados;
- credenciais procuradas;
- tentativas de escalada;
- caminhos percorridos;
- comportamento;
- interesses demonstrados;
- tentativas de saída.

---

# 5.8 Objetivo de inteligência

A pergunta não é somente:

> **"Quem entrou?"**

Também:

> **"O que ele estava procurando?"**

E:

> **"O que ele fez quando pensou que encontrou?"**

A reação do invasor fornece informação sobre:

- objetivo;
- prioridade;
- conhecimento prévio;
- ferramentas;
- nível técnico;
- origem provável;
- interesse específico em Ryan.

---

# 6. Handshake e Árvore de Confiança

## 6.1 Princípio

Autenticação não é suficiente para determinar confiança.

O sistema também verifica:

- sequência;
- origem;
- momento;
- contexto;
- estado;
- caminho percorrido;
- próximo estado esperado.

> **Uma chave válida utilizada no lugar errado continua sendo um evento de segurança.**

---

# 6.2 Árvore de Handshakes

```text
                         ROOT
                           |
             +-------------+-------------+
             |                           |
            A1                           A2
          /    \                       /    \
        A1.1  A1.2                   A2.1  A2.2
         |      |                     |      |
        B1     B2                    B3     B4
```

Cada nó pode possuir:

- chave pública;
- chave privada correspondente;
- nonce;
- identificador do estado;
- próximo estado esperado;
- janela temporal;
- permissões;
- nível de confiança.

O sistema não valida apenas:

> "A chave é válida?"

Também valida:

> "Essa chave deveria aparecer agora, a partir deste estado, neste dispositivo e nesta sessão?"

---

# 6.3 Validação de trajetória

Uma sessão normal pode percorrer:

```text
ROOT → A1 → A1.2 → B2 → SESSION
```

Se o atacante provocar:

```text
ROOT → A1 → A1.2 → X7
```

quando `X7` não é esperado:

> **PATH DEVIATION**

---

# 6.4 Resposta por Agent

### Vault

```text
PATH DEVIATION
      ↓
COMPROMETIMENTO
      ↓
CORTE IMEDIATO
```

### Profissional

```text
PATH DEVIATION
      ↓
SUSPEITA
      ↓
DUMMY
      ↓
MONITORAMENTO
```

### Honeypot

```text
PATH DEVIATION
      ↓
COMPROMETIMENTO ASSUMIDO
      ↓
DUMMY
      ↓
AUDITORIA
      ↓
RASTREAMENTO
```

---

# 7. Protocol Deception Layer

## 7.1 Princípio

> **O atacante pode descobrir que uma chave é válida. Ele não deve descobrir facilmente qual é o protocolo correto de utilização dessa chave.**

O sistema pode continuar fornecendo handshakes criptograficamente válidos depois que a trajetória real já foi abandonada.

---

# 7.2 Dummy Branch

```text
CAMINHO REAL

ROOT
 ↓
A1
 ↓
A1.2
 ↓
SESSION REAL


CAMINHO COMPROMETIDO

ROOT
 ↓
A1
 ↓
A1.2
 ↓
DUMMY-01
 ↓
DUMMY-04
 ↓
DUMMY-09
 ↓
SIMULATED SESSION
```

O invasor recebe:

```text
AUTHENTICATION SUCCESSFUL
ACCESS GRANTED
SESSION ESTABLISHED
```

O sistema registra:

```text
REAL PATH TERMINATED
DUMMY ENVIRONMENT ACTIVE
```

---

# 7.3 Erro deve ser caro

O sistema não permite tentativa e erro ilimitada sem consequências.

Cada tentativa pode:

- consumir recursos;
- gerar eventos;
- alterar o caminho;
- ativar defesa;
- revelar ferramentas;
- aumentar o rastreamento;
- provocar ICE;
- provocar isolamento.

O atacante precisa decidir:

> **continuar arriscando ou abandonar a invasão.**

---

# 8. Protocolo de Comprometimento

O sistema pode trabalhar com:

```text
NORMAL
   ↓
ANOMALIA
   ↓
SUSPEITA
   ↓
COMPROMETIMENTO PROVÁVEL
   ↓
COMPROMETIMENTO CONFIRMADO
```

Mas a interpretação depende do Agent.

### Vault

```text
NORMAL
  ↓
QUALQUER ANOMALIA
  ↓
ISOLAMENTO
```

### Profissional

```text
NORMAL
  ↓
ANOMALIA
  ↓
SUSPEITA
  ↓
DUMMY
```

Não é necessário confirmar o comprometimento antes de abandonar o ambiente real.

### Honeypot

```text
NORMAL
  ↓
ANOMALIA
  ↓
COMPROMETIMENTO ASSUMIDO
  ↓
DUMMY
  ↓
AUDITORIA
```

---

# 9. Watchdog / Auditor

O Watchdog acompanha metadados das sessões.

Registra:

- dispositivo;
- sessão;
- horário;
- origem;
- caminho;
- nós acessados;
- sequência;
- alterações;
- tentativas;
- respostas;
- tempo entre eventos.

Exemplo:

```text
DEVICE: AGENT-03

11:42:07 — ROOT
11:42:08 — A1
11:42:09 — A1.2
11:42:11 — B7
11:42:11 — B7.3
11:42:14 — B7.3.2
```

Se o esperado fosse:

```text
ROOT → A1 → A1.2 → C3
```

o sistema detecta:

```text
EXPECTED: C3
ACTUAL:   B7

PATH DEVIATION
```

---

# 10. Arbiter

Camada de política e confiança.

Responsabilidades:

- validar se um link é permitido;
- bloquear Vault ↔ rede;
- limitar Vault ↔ Profissional;
- impedir Vault ↔ Honeypot;
- autorizar janelas curtas de sincronização;
- bloquear tentativas de pivot;
- receber eventos do Watchdog;
- elevar incidentes.

O Arbiter não é o Warden.

Pode ser implementado como política distribuída nos Agents.

---

# 11. Conexões

| De → Para                  | Meio                              | Política                    |
| -------------------------- | --------------------------------- | --------------------------- |
| Profissional ↔ rede        | Wireless / Agent net              | Permitido e monitorado      |
| Honeypot ↔ rede            | Wireless                          | Permitido                   |
| Vault ↔ rede               | **Proibido normalmente**          | Air-gap                     |
| Vault ↔ Profissional       | **Não direto**                    | Sincronização controlada    |
| Vault ↔ terceira interface | Neural Link / Kiroshi             | One-shot                    |
| Profissional ↔ Honeypot    | Canal controlado                  | Alimentação de dados falsos |
| Honeypot → Vault           | **Nunca permitido**               | Arbiter drop                |
| Honeypot → Profissional    | **Nunca permitido para controle** | Isolado                     |
| Neural Link → Vault        | Sessão autorizada                 | Sem keep-alive              |

---

# 12. Pipeline de Atualização

```text
Alteração
   ↓
Sandbox externo
   ↓
Testes
   ↓
Agent Profissional
   ↓
Testes de integração
   ↓
Testes de segurança
   ↓
Validação final
   ↓
Build aprovado
   ↓
Terceira interface
   ↓
Vault
   ↓
Sessão encerrada
   ↓
Interface destruída
```

O Vault nunca recebe diretamente uma alteração experimental.

---

# 13. Matriz de Vazamento

| Nível  | Nome        | Onde pode existir       | Se vazar                   |
| ------ | ----------- | ----------------------- | -------------------------- |
| **L0** | Public bait | Honeypot                | Informação inútil / canary |
| **L1** | Operational | Profissional / Honeypot | Dor moderada               |
| **L2** | Sensitive   | Profissional cifrado    | Incidente relevante        |
| **L3** | Critical    | **Somente Vault**       | Comprometimento grave      |
| **L4** | Crown       | Vault + handoff físico  | Comprometimento extremo    |

---

# 14. Modelo de Confiança

O sistema não considera suficiente:

```text
CHAVE VÁLIDA
```

A confiança considera:

```text
CHAVE
 +
ORIGEM
 +
TEMPO
 +
ESTADO
 +
SEQUÊNCIA
 +
CAMINHO
 +
CONTEXTO
 =
CONFIANÇA
```

Uma chave roubada pode continuar sendo válida.

Uma sessão sequestrada pode continuar parecendo válida.

Um handshake pode continuar sendo criptograficamente válido.

Mas uma **trajetória inválida** denuncia o comprometimento.

---

# 15. Princípio de Deception

O sistema assume que um invasor tende a reduzir sua cautela quando acredita ter conseguido acesso.

Portanto:

> **Não revelar imediatamente que a invasão foi detectada pode ser mais valioso do que bloquear imediatamente a invasão.**

Essa regra aplica-se somente aos sistemas com tolerância de risco.

### Vault

Nunca.

### Profissional

Suspeita → abandonar ambiente real → dummy.

### Honeypot

Suspeita → manter interação → auditar → rastrear.

---

# 16. Black ICE e Defesa Convencional

A arquitetura de deception não substitui os programas de segurança.

A defesa continua existindo antes, durante e depois da detecção.

Camadas conceituais:

```text
1. Isolamento
2. Autenticação
3. Handshake
4. Validação de trajetória
5. Firewall / detecção
6. Gray ICE
7. Black ICE
8. Deception
9. Auditoria
10. Isolamento final
```

A posição e intensidade de cada camada dependem do Agent.

No Vault, entretanto:

> **a defesa ativa é secundária à decisão de cortar a conexão.**

---

# 17. Identidade Física e OPSEC

A existência dos três Agents não deve ser óbvia.

## Vault

Parece:

> **um simples chip/cibernética implantado em Ryan.**

Não parece um Agent.

Não possui tela.

Não possui interface externa.

Não é reconhecível como dispositivo de comunicação.

---

## Profissional

Parece:

> **um pequeno stick metálico.**

Pode ficar escondido em um subdermal pocket.

Não precisa ser manipulado para ser utilizado.

A interação ocorre através do Neural Link.

Se comprometido:

> **descarta e substitui.**

---

## Honeypot

Parece:

> **o Agent de Ryan.**

Pode ser mostrado.

Pode ser utilizado publicamente.

Possui aparência convencional.

Pode ficar sobre a mesa.

Pode ser visto por aliados.

Pode ser visto por inimigos.

Essa exposição é deliberada.

---

# 18. Cenário de Uso

Ryan está diante de outras pessoas.

Ele segura o Honeypot.

Na percepção externa:

```text
Ryan
 ↓
Agent visível
 ↓
trabalho
```

Na realidade:

```text
Ryan
 ↓
Neural Link
 ↓
PROFISSIONAL
 ↓
trabalho real
```

O Honeypot pode:

- mostrar informações plausíveis;
- receber comandos;
- responder;
- manter histórico;
- executar tarefas falsas;
- simular atividade.

Se alguém roubar o dispositivo:

> **não encontrou necessariamente o Agent que estava trabalhando.**

Se alguém comprometer o dispositivo:

> **pode ter acabado de entrar voluntariamente na armadilha.**

---

# 19. Filosofia dos Três Agents

### Vault

> **"Qualquer anomalia vale a perda da conexão."**

Se for necessário:

- cirurgia;
- desmontagem do implante;
- restauração;
- substituição;
- destruição física;

isso ainda é preferível ao vazamento de seus dados críticos.

---

### Profissional

> **"Suspeita já é suficiente para abandonar o ambiente real."**

O Agent pode ser sacrificado.

A sessão pode ser perdida.

O hardware pode ser substituído.

Ryan é redundante.

O objetivo é:

> **não arriscar segurança para salvar um dispositivo.**

---

### Honeypot

> **"Se você entrou, quero saber como."**

O invasor pode acreditar que venceu.

Pode receber handshakes válidos.

Pode atravessar nós.

Pode encontrar arquivos.

Pode acreditar que chegou ao coração do sistema.

Enquanto isso:

```text
INTRUSION
   ↓
PATH DEVIATION
   ↓
DUMMY BRANCH
   ↓
AUDIT
   ↓
TRACE
   ↓
INTELLIGENCE
```

---

# 20. Princípio Final

O objetivo não é criar um sistema impossível de invadir.

É criar um sistema onde:

- o Vault não permanece exposto;
- qualquer anomalia no Vault encerra a conexão;
- o Vault só recebe atualizações após validação completa;
- a atualização do Vault ocorre por uma terceira interface;
- a sessão do Vault é destruída imediatamente após o uso;
- o Vault pode ser fisicamente destruído se houver risco de captura;
- o Profissional é descartável;
- suspeita no Profissional já provoca migração para dummy;
- o Honeypot funciona como cobertura para o Profissional;
- o Honeypot parece um Agent real e ativo;
- o Profissional alimenta o Honeypot com informação falsa e recente;
- uma chave roubada não equivale a uma sessão confiável;
- uma sessão sequestrada não equivale a um caminho válido;
- um invasor pode ser enganado sem perceber que foi detectado;
- cada tentativa pode fornecer inteligência;
- erro e tentativa e erro têm custo;
- dados críticos nunca dependem da boa-fé da rede;
- a identidade física de um Agent não revela necessariamente sua função.

> **"Um sistema seguro não é aquele que nunca é atacado. É aquele onde um ataque nunca acontece sem consequência."**

E, para o Vault:

> **"Se eu tiver que escolher entre perder o Vault e deixar alguém entrar nele, eu perco o Vault."**

---

## Referências

- Loadout: [ryan_loadout.md](../fichas/ryan_loadout.md)
- Techie: [08_techie.md](../sistema/regras_red/08_techie.md)
- Netrunning: [10_netrunning.md](../sistema/regras_red/10_netrunning.md)
- Fatos: [fatos_duros.md](../sistema/fatos_duros.md) — **F19**
- Warden: **F03**
- Echo: [echo_exposicao.md](../sistema/echo_exposicao.md)

---

# 21. Mesa RED (017+)

| Cena | Resolução |
| ---- | --------- |
| Abrir Vault | Auth + tempo; **anomalia = corte** (sem duelo NET no cofre) |
| Dummy Profissional | Atacante em L1 falso; detecção Cybertech/Electronics |
| Honeypot invadido | L0 + canary; audit; [10_netrunning](../sistema/regras_red/10_netrunning.md) se jack |
| Path deviation | Resposta por Agent (Vault cut / Prof dummy / Honeypot audit) |
| Sync → Vault | 3ª interface Neural one-shot pós-validação; downtime se sob pressão |
| Wipeout Vault | Decisão de cena; Surgery se físico (Stitch/Doc) |
| Drones | F03/F12/F16 — **separados** dos Agents |

**Histórico ≤016:** não re-rolar. Agent no passado = "o profissional / o de trabalho / o da mão".

House: [regras_campanha.md](../sistema/house_rules/regras_campanha.md) §9.
