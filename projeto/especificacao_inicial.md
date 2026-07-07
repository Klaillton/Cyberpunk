# Especificação Inicial – Motor Narrativo Persistente para RPG (Raspberry Pi 4)

## Objetivo

Desenvolver um motor de narrativa persistente para campanhas de RPG, executando em um Raspberry Pi 4 (8 GB), onde o Raspberry seja responsável por toda a lógica da campanha e um LLM externo (ChatGPT, Grok ou outro) seja utilizado apenas para geração narrativa e decisões complexas.

O projeto deve ser modular, desacoplado e independente do provedor de IA.

---

# Filosofia do Projeto

O LLM **não é o Mestre do RPG**.

O LLM é apenas um escritor contratado.

Quem realmente conhece o mundo, seus personagens, suas regras e sua história é o **Motor Narrativo** executando localmente.

Todo o estado do universo deve existir localmente.

O modelo recebe apenas um recorte extremamente bem preparado daquele universo.

O objetivo do projeto é **eliminar a dependência da memória do LLM**.

---

# Princípios Fundamentais

## 1. Fonte Única da Verdade

Toda informação persistente deve existir localmente.

O LLM nunca deve ser considerado uma fonte de memória.

Toda decisão importante deve poder ser reconstruída apenas pelos dados armazenados.

---

## 2. Contexto Determinístico

O modelo nunca deve "adivinhar" como um NPC age.

O sistema deve fornecer contexto suficiente para que dois modelos diferentes produzam respostas coerentes com a campanha.

---

## 3. Independência do Modelo

Trocar ChatGPT por Grok, Claude, Gemini ou um modelo local deve exigir apenas alterar um adaptador de API.

Nenhuma regra da campanha pode depender de um modelo específico.

---

# Arquitetura Geral

```text
Jogador
     │
     ▼
FastAPI
     │
     ▼
Motor Narrativo
     │
 ┌───┼──────────────────────────┐
 │   │                          │
 ▼   ▼                          ▼
SQLite              Índice Vetorial (FAISS)
 │                           │
 ▼                           ▼
Markdown              Busca Semântica
 │                           │
 └──────────────┬────────────┘
                ▼
      Montador de Contexto
                ▼
         Cliente do LLM
                ▼
       ChatGPT / Grok / Outro
                ▼
      Resposta Narrativa
                ▼
 Parser de Atualização
                ▼
 Atualiza Banco + Markdown + Índice
```

---

# Responsabilidades do Raspberry

O Raspberry deve controlar:

- Estado do mundo
- NPCs
- Personagens
- Economia
- Clima
- Cronologia
- Inventários
- Eventos
- Reputações
- Consequências
- Memória da campanha
- Atualização automática dos arquivos
- Seleção inteligente do contexto
- Chamadas aos LLMs

---

# O LLM NÃO é responsável por

- Lembrar acontecimentos
- Controlar personalidade
- Atualizar estado do mundo
- Controlar inventários
- Controlar economia
- Decidir consequências permanentes
- Inventar relacionamentos

Ele apenas interpreta o contexto recebido e produz narrativa.

---

# Estrutura dos Dados

A campanha será organizada em Markdown.

Exemplo:

```text
campanha/
├── personagens/
├── npcs/
├── faccoes/
├── locais/
├── itens/
├── missoes/
├── eventos/
├── cronologia/
├── relacionamentos/
├── consequencias/
├── regras/
└── diretrizes/
```

Markdown é a fonte de verdade humana.

SQLite existe apenas para indexação e consultas rápidas.

---

# Banco SQLite

O banco armazenará entidades estruturadas.

## Tabelas previstas

- NPCs
- Personagens
- Facções
- Locais
- Eventos
- Inventários
- Missões
- Relacionamentos
- Cronologia
- Consequências
- Memória Episódica

---

# Índice Vetorial

Todos os Markdown devem ser indexados.

## Objetivo

Quando surgir uma ação do jogador:

> "Vou visitar Elias."

O sistema procura automaticamente apenas o contexto relevante.

Exemplo:

```text
elias.md
oficina.md
sessao_28.md
hydroponia.md
```

Nunca enviar toda a campanha para o modelo.

---

# Camadas de Contexto

O prompt deve ser montado em camadas.

```text
Regras do Sistema
        ↓
Contexto Global
        ↓
Estado do Mundo
        ↓
NPCs Envolvidos
        ↓
Relacionamentos
        ↓
Eventos Recentes
        ↓
Cena Atual
        ↓
Ação do Jogador
```

Cada camada pode ser atualizada independentemente.

---

# Contexto Global

Informações praticamente permanentes.

Exemplo:

- Cenário
- Regras da campanha
- Estilo narrativo
- Tecnologias
- Calendário
- Facções
- Leis do mundo

---

# Estado do Mundo

Informações variáveis.

Exemplo:

- Horário
- Clima
- Recursos
- Guerras
- Alertas
- Crises
- Eventos em andamento

---

# Sistema de NPCs

Cada NPC possui duas partes.

## Núcleo Permanente

Nunca muda (ou muda muito raramente).

```text
Nome

Personalidade

Temperamento

Valores

Objetivos

Traumas

Hábitos

Modo de falar

Gestos

Virtudes

Defeitos

Medos

Sonhos
```

Esse bloco garante que o NPC nunca "mude de personalidade" apenas porque o modelo é diferente.

---

## Estado Atual

Muda constantemente.

```text
Humor

Ferimentos

Sono

Fome

Localização

Objetivo atual

Última atividade

Emoção dominante
```

---

# Sistema de Relacionamentos

Amizade é apenas um aspecto.

Cada relação possui múltiplos atributos.

Exemplo:

```text
Ryan → Elias

Confiança
Respeito
Admiração
Lealdade
Medo
Raiva
Ódio
Dependência
Romance
Dívida Moral
```

Cada atributo possui um valor numérico.

Exemplo:

```text
Confiança: 92

Respeito: 88

Admiração: 73

Lealdade: 95

Ódio: 0
```

---

# Histórico Compartilhado

Não enviar toda a campanha.

Enviar apenas um resumo relevante.

Exemplo:

```text
Ryan salvou Elias.

Construíram juntos a hidroponia.

Sobreviveram ao ataque do comboio.

Trabalham juntos há quatro meses.
```

Isso explica naturalmente por que existe intimidade.

---

# Memória Episódica

Além da memória permanente existe memória recente.

Exemplo:

Últimas 24 horas

```text
Ryan ensinou Tomas.

Mara observou.

Elias aprovou.

Valk discordou.
```

Essa memória influencia a cena atual.

---

# Seleção Automática de Contexto

O sistema deve descobrir automaticamente:

- Quais NPCs aparecem
- Quais locais aparecem
- Quais itens aparecem
- Quais eventos são relevantes
- Quais arquivos devem ser enviados

O usuário nunca monta contexto manualmente.

---

# Atualização Automática

Após receber a narrativa:

```text
Narrativa

↓

Parser

↓

Detecta alterações

↓

Atualiza SQLite

↓

Atualiza Markdown

↓

Atualiza Índice Vetorial

↓

Atualiza Estado do Mundo
```

---

# Modelo Local

Opcional.

Caso exista, terá as seguintes funções:

- Resumir documentos
- Classificar contexto
- Extrair entidades
- Detectar inconsistências
- Selecionar arquivos
- Comprimir contexto

Nunca será responsável pela narrativa principal.

---

# API

## Endpoints previstos

```text
POST /message

POST /scene

POST /context

POST /save

POST /search

GET /npc/{id}

GET /world

GET /timeline

POST /llm/chatgpt

POST /llm/grok
```

---

# Objetivo Principal

Criar um sistema onde qualquer modelo de linguagem possa ser substituído sem alterar o funcionamento do RPG.

O Raspberry deve conter toda a inteligência estrutural.

O LLM deve funcionar apenas como um narrador temporário, recebendo um contexto cuidadosamente preparado e retornando apenas texto narrativo.

A campanha jamais dependerá da memória do modelo.

---

# Funcionalidades Futuras (Roadmap)

O sistema deve ser projetado para suportar futuramente:

- Simulação de rotina diária dos NPCs (mesmo fora da presença do jogador).
- Economia persistente e oferta/demanda.
- Sistema de rumores propagados entre NPCs.
- Facções com objetivos próprios.
- Eventos globais independentes do jogador.
- Planejamento de longo prazo para NPCs.
- Memória individual de cada NPC (o que ele sabe, suspeita, esqueceu ou acredita).
- Sistema de reputação por facção, cidade e indivíduo.
- Compressão inteligente de contexto para caber em diferentes limites de tokens.
- Múltiplos jogadores compartilhando o mesmo mundo persistente.

---

# Fluxo de Execução

```text
Jogador envia ação
        │
        ▼
Motor identifica entidades
        │
        ▼
Busca documentos relevantes
        │
        ▼
Monta contexto em camadas
        │
        ▼
Envia ao LLM
        │
        ▼
Recebe narrativa
        │
        ▼
Extrai alterações
        │
        ▼
Valida regras
        │
        ▼
Atualiza mundo
        │
        ▼
Salva alterações
```

---

# Consideração Importante

A IA **não é a dona da narrativa**.

Ela é apenas um narrador.

O estado do universo pertence exclusivamente ao Motor Narrativo.

Fluxo ideal:

1. O Motor Narrativo prepara o contexto.
2. O LLM gera a narrativa.
3. O Motor interpreta a resposta.
4. O Motor extrai fatos relevantes.
5. O Motor valida as alterações.
6. O Motor atualiza o estado permanente.

Se o LLM esquecer um relacionamento, exagerar uma reação ou criar uma inconsistência, o Motor Narrativo deve detectar e corrigir antes que a alteração seja persistida.

Dessa forma, a campanha permanece consistente por meses ou anos, independentemente do modelo de linguagem utilizado.
