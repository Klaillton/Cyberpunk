# Escudo Energético — Estágio 2

> **Status:** folded em 2026-10-30. SoT (ainda não canônico): [projeto de armadura](../fichas/reina_armour_project.md) § Escudo Energético. O projeto continua **IDEIA FUTURA**. Não é boot. Não altera a ficha da Reina. Este arquivo é a fonte longa.

**Aplicação:** Exclusivamente no Estágio 2 da armadura da Reina. Ainda não testado em jogo.

## 1. Conceito

O escudo energético é uma camada de proteção que envolve o corpo inteiro da Reina, funcionando como um único campo de energia.

Não existem escudos independentes por região corporal. O campo protege a personagem como um todo, independentemente de onde o ataque a atinja.

Sua finalidade é permitir que Reina avance em combate, atraia a atenção dos adversários e sustente fogo inimigo enquanto atua na linha de frente.

## 2. Características

| Propriedade                  |    Valor |
| ---------------------------- | -------: |
| SP do escudo                 |       15 |
| HP por cartucho              |       60 |
| Cartuchos dedicados          |        5 |
| Capacidade total distribuída |   300 HP |
| Tempo mínimo de substituição | 2 turnos |

O escudo possui dois parâmetros distintos:

- **SP 15:** redução fixa de dano por ataque enquanto o campo estiver ativo.
- **HP 60:** integridade energética disponível em cada cartucho.

O SP não sofre ablação. Permanece em 15 até que o campo seja desativado.

## 3. Resolução de dano

Todo ataque é processado nesta ordem:

1. Determina-se o dano total do ataque.
2. O SP 15 do escudo reduz o dano recebido.
3. O dano restante é subtraído do HP do cartucho atual.
4. Caso o dano ultrapasse o HP restante, o excedente atravessa o escudo e é encaminhado à armadura física.
5. Quando o HP chega a zero, o campo energético é desativado.

A armadura física aplica seu próprio SP normalmente ao dano que atravessar o escudo.

### Exemplo A — Ataque absorvido

- Dano recebido: 30.
- Redução do escudo: 15.
- Dano restante: 15.
- HP inicial: 60.
- HP restante: 45.

Nenhum dano chega à armadura física.

### Exemplo B — Ataque que esgota o escudo

- Dano recebido: 40.
- Redução do escudo: 15.
- Dano restante: 25.
- HP restante antes do ataque: 20.
- HP consumido: 20.
- Excedente: 5.

O campo é desativado e os 5 pontos excedentes são encaminhados à armadura física, que aplica seu próprio SP.

**Importante:** o excedente não é descartado. O escudo não pode absorver mais dano do que sua integridade restante permite.

## 4. Cartuchos

O sistema utiliza cinco cartuchos dedicados exclusivamente ao escudo energético.

Cada cartucho fornece uma carga independente de 60 HP.

- Um cartucho esgotado não pode ser recarregado durante o combate.
- A substituição exige pelo menos dois turnos.
- A instalação de um cartucho novo restaura o escudo para 60 HP.
- O SP permanece em 15.
- Os cartuchos do escudo não compartilham energia com os sistemas de propulsão, mobilidade ou outros equipamentos da armadura.

A capacidade total de 300 HP representa cinco cargas de 60 HP, e não uma reserva contínua de 300 HP.

## 5. Comportamento em combate

O escudo foi dimensionado para favorecer a permanência de Reina na linha de frente.

Seu comportamento esperado:

- Contra ataques convencionais, tende a preservar boa parte da carga.
- Contra armas pesadas, consome HP mais rapidamente.
- Contra explosões, pode absorver uma parcela significativa do dano, mas ataques suficientemente fortes podem ultrapassar a integridade restante.
- Quando esgotado, deixa Reina dependente da proteção física até que um novo cartucho seja instalado.

## 6. Limitações

O escudo não torna Reina invulnerável.

A proteção está sujeita à integridade da carga atual. Quando ela se esgota, o campo deixa de oferecer SP.

Interferências eletrônicas, falhas de alimentação e efeitos que não sejam resolvidos como dano convencional ainda precisam ter suas interações definidas separadamente.

## 7. Configuração consolidada

**Escudo Energético — Estágio 2**

- Campo de proteção único, de cobertura corporal integral.
- SP fixo: 15.
- HP por cartucho: 60.
- Cinco cartuchos dedicados.
- Capacidade total: 300 HP distribuídos em cinco cargas.
- Sem ablação de SP.
- Dano excedente atravessa o escudo e segue para a armadura física.
- Esgotamento de uma carga desativa o campo.
- Substituição de cartucho: mínimo de dois turnos.
