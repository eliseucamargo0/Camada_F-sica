# Camada Física usando Som

## 1. Identificação da Equipe

## 2. Introdução



3. Fundamentação Teórica

3.1 Modelo ISO/OSI

O modelo ISO/OSI organiza a comunicação em redes de computadores em sete camadas, cada uma responsável por uma função específica:

Aplicação: fornece serviços de rede diretamente aos programas utilizados pelo usuário.

Apresentação: trata do formato dos dados, como codificação, conversão e criptografia.

Sessão: controla o estabelecimento, manutenção e encerramento das sessões de comunicação.

Transporte: realiza a comunicação entre os dispositivos e pode fornecer mecanismos de controle e confiabilidade na transmissão.

Rede: realiza o endereçamento lógico e define o caminho que os dados devem seguir.

Enlace: organiza os dados em quadros e pode realizar detecção de erros na comunicação entre dispositivos diretamente conectados.

Física: transmite os bits por meio de sinais físicos, como sinais elétricos, luminosos, ondas de rádio ou, neste projeto, sinais sonoros.

3.2 Camada Física

A Camada Física é responsável pela transmissão dos bits através de um meio físico.

Neste projeto, o meio utilizado é o som. As informações são representadas por sinais sonoros, captados por um microfone e posteriormente processados pelo software para identificar os bits transmitidos.

O funcionamento pode ser representado de forma simplificada como:

Informação → sinal sonoro → microfone → processamento → bits (0 e 1)

3.3 Sinais Analógicos e Digitais

Um sinal analógico varia continuamente ao longo do tempo. O som captado pelo microfone é um exemplo de sinal analógico.

Já um sinal digital representa informações por valores discretos, normalmente utilizando 0 e 1.

No projeto, o som é captado pelo microfone e convertido em amostras digitais. O programa analisa essas amostras para identificar os eventos sonoros e transformá-los em bits.

3.4 Taxa de Amostragem

A taxa de amostragem determina quantas vezes o sinal sonoro é medido por segundo.

No projeto, foi utilizada:

fs = 44100

Isso significa que o áudio é amostrado a 44.100 amostras por segundo (44,1 kHz).

Para uma gravação de 10 segundos, são obtidas aproximadamente:

10 × 44.100 = 441.000 amostras.

Quanto maior a taxa de amostragem, maior é a quantidade de informações obtidas sobre a variação do sinal ao longo do tempo.

3.5 Largura de Banda

A largura de banda representa a faixa de frequências disponível para a transmissão de um sinal.

No caso de sinais sonoros, a frequência é medida em Hertz (Hz). Diferentes frequências representam diferentes características do som.

A largura de banda disponível influencia a quantidade de informação que pode ser transmitida, mas a velocidade também depende da técnica de modulação, do ruído e das características do meio de transmissão.

3.6 Modulação

Modulação é o processo de alterar uma característica de um sinal para representar informações.

Em uma transmissão sonora, podem ser utilizadas características como:

frequência;

amplitude;

duração.

Por exemplo, uma técnica pode utilizar uma frequência para representar o bit 0 e outra frequência para representar o bit 1.

Uma possibilidade para o segundo método do projeto é a FSK (Frequency Shift Keying), na qual diferentes frequências representam diferentes bits.

Exemplo:

0 → frequência F0
1 → frequência F1

Os valores definitivos das frequências e demais parâmetros dependem da implementação escolhida pela equipe.

3.7 Ruído

Ruído é qualquer sinal indesejado que interfere na transmissão ou na recepção da informação.

Em uma comunicação utilizando som, podem existir ruídos causados por:

conversas;

televisão;

ventiladores;

trânsito;

outras batidas;

eco;

sons do ambiente.

Por isso, o receptor precisa diferenciar o sinal desejado dos sons que não fazem parte da transmissão.

No Método 1, o programa utiliza um threshold (limiar) para ajudar nessa identificação:

threshold = 0.2

As amostras cuja amplitude ultrapassa esse valor são consideradas possíveis eventos sonoros, enquanto amplitudes abaixo do limiar são interpretadas como silêncio.

3.8 Detecção de Erros

Durante uma transmissão, os dados podem sofrer alterações devido ao ruído ou a outros problemas do meio de comunicação.

Por exemplo:

Enviado:   10110010
Recebido:  10100010

Nesse caso, um dos bits foi alterado.

Por isso, os métodos de transmissão precisam utilizar mecanismos de detecção de erros, capazes de indicar quando os dados recebidos podem estar diferentes dos dados enviados.

3.8.1 Paridade Par

No Método 1, deve ser utilizado um quadro de 9 bits, formado por:

8 bits de dados;

1 bit de paridade.

A paridade utilizada é a paridade par. O objetivo é fazer com que a quantidade total de bits 1 no quadro seja par.

Se os 8 bits de dados já possuem uma quantidade par de 1, o bit de paridade será 0.

Exemplo:

Dados:    10110010
Número de 1: 4
Paridade:  0
Quadro:   101100100

Se os 8 bits possuem uma quantidade ímpar de 1, o bit de paridade será 1.

Exemplo:

Dados:    10110011
Número de 1: 5
Paridade:  1
Quadro:   101100111

No receptor, os primeiros 8 bits são analisados e o bit de paridade esperado é calculado. Esse valor é comparado com o 9º bit recebido.

Se os valores forem iguais, o quadro passa na verificação de paridade. Se forem diferentes, o receptor indica que houve um possível erro na transmissão.

A paridade é um mecanismo de detecção de erros, não de correção. Ela permite identificar determinados erros, mas não recuperar automaticamente o bit que foi alterado.

3.9 Taxa de Transmissão

A taxa de transmissão representa a quantidade de bits transmitidos por segundo e é medida em bits por segundo (bps).

Por exemplo:

10 bits em 1 segundo = 10 bps

No projeto, será necessário avaliar tanto a taxa teórica quanto a taxa prática de transmissão.

A taxa teórica representa a velocidade esperada em condições ideais. Já a taxa prática considera fatores como ruído, capacidade de processamento, sincronização e limitações do equipamento utilizado.

Uma velocidade maior pode aumentar a quantidade de dados transmitidos, mas também pode dificultar a identificação correta dos sinais. Por isso, o objetivo é encontrar uma velocidade que mantenha uma transmissão confiável.


## 4. Engenharia e Arquitetura das Soluções
### 4.1 Visão Geral do Sistema
### 4.2 Método 1 — Transmissão por Batidas
### 4.3 Estrutura do Quadro de 9 Bits
### 4.4 Detecção de Erros do Método 1
### 4.5 Método 2 — [nome do método escolhido]
### 4.6 Detecção de Erros do Método 2
### 4.7 Taxa de Transmissão

## 5. Funcionamento do Software
### 5.1 Emissor
### 5.2 Receptor
### 5.3 Bibliotecas Utilizadas
### 5.4 Interface/Terminal

## 6. Divisão de Tarefas da Equipe

## 7. Desafios, Problemas e Soluções

## 8. Demonstração em Vídeo

## 9. Uso de Inteligência Artificial

## 10. Conclusão

## 11. Licença