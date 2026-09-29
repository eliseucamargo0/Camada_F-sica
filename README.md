# Camada Física usando Som

## 1. Identificação da Equipe

## 2. Introdução

Este projeto tem como objetivo demonstrar o funcionamento da Camada Física do modelo ISO/OSI utilizando o som como meio de transmissão de informações.

O sistema utiliza um microfone para captar eventos sonoros e um software para processar o sinal recebido, identificar os padrões de batidas e convertê-los em bits.

O projeto possui dois métodos de transmissão. O Método 1 utiliza eventos sonoros por impacto, enquanto o Método 2 utilizará outra técnica de transmissão definida pela equipe.

---

# 3. Fundamentação Teórica

## 3.1 Modelo ISO/OSI

O modelo ISO/OSI organiza a comunicação em redes de computadores em sete camadas, cada uma responsável por uma função específica:

**Aplicação:** fornece serviços de rede diretamente aos programas utilizados pelo usuário.

**Apresentação:** trata do formato dos dados, como codificação, conversão e criptografia.

**Sessão:** controla o estabelecimento, manutenção e encerramento das sessões de comunicação.

**Transporte:** realiza a comunicação entre os dispositivos e pode fornecer mecanismos de controle e confiabilidade na transmissão.

**Rede:** realiza o endereçamento lógico e define o caminho que os dados devem seguir.

**Enlace:** organiza os dados em quadros e pode realizar detecção de erros na comunicação entre dispositivos diretamente conectados.

**Física:** transmite os bits por meio de sinais físicos, como sinais elétricos, luminosos, ondas de rádio ou, neste projeto, sinais sonoros.

## 3.2 Camada Física

A Camada Física é responsável pela transmissão dos bits através de um meio físico.

Neste projeto, o meio utilizado é o som. As informações são representadas por sinais sonoros, captados por um microfone e posteriormente processados pelo software para identificar os bits transmitidos.

O funcionamento pode ser representado de forma simplificada como:

**Informação → sinal sonoro → microfone → processamento → bits (0 e 1)**

## 3.3 Sinais Analógicos e Digitais

Um sinal analógico varia continuamente ao longo do tempo. O som captado pelo microfone é um exemplo de sinal analógico.

Já um sinal digital representa informações por valores discretos, normalmente utilizando 0 e 1.

No projeto, o som é captado pelo microfone e convertido em amostras digitais. O programa analisa essas amostras para identificar os eventos sonoros e transformá-los em bits.

## 3.4 Taxa de Amostragem

A taxa de amostragem determina quantas vezes o sinal sonoro é medido por segundo.

No projeto, foi utilizada:

```python
fs = 44100
```

Isso significa que o áudio é amostrado a 44.100 amostras por segundo (44,1 kHz).

Para uma gravação de 10 segundos, são obtidas aproximadamente:

**10 × 44.100 = 441.000 amostras.**

Quanto maior a taxa de amostragem, maior é a quantidade de informações obtidas sobre a variação do sinal ao longo do tempo.

## 3.5 Largura de Banda

A largura de banda representa a faixa de frequências disponível para a transmissão de um sinal.

No caso de sinais sonoros, a frequência é medida em Hertz (Hz). Diferentes frequências representam diferentes características do som.

A largura de banda disponível influencia a quantidade de informação que pode ser transmitida, mas a velocidade também depende da técnica de modulação, do ruído e das características do meio de transmissão.

## 3.6 Modulação

Modulação é o processo de alterar uma característica de um sinal para representar informações.

Em uma transmissão sonora, podem ser utilizadas características como:

- frequência;
- amplitude;
- duração.

Por exemplo, uma técnica pode utilizar uma frequência para representar o bit 0 e outra frequência para representar o bit 1.

Uma possibilidade para o segundo método do projeto é a FSK (Frequency Shift Keying), na qual diferentes frequências representam diferentes bits.

Exemplo:

```text
0 → frequência F0
1 → frequência F1
```

Os valores definitivos das frequências e demais parâmetros dependem da implementação escolhida pela equipe.

No Método 1, a representação dos bits não é feita por diferentes frequências. Os bits são representados pela quantidade de batidas consecutivas.

## 3.7 Ruído

Ruído é qualquer sinal indesejado que interfere na transmissão ou na recepção da informação.

Em uma comunicação utilizando som, podem existir ruídos causados por:

- conversas;
- televisão;
- ventiladores;
- trânsito;
- outras batidas;
- eco;
- sons do ambiente.

Por isso, o receptor precisa diferenciar o sinal desejado dos sons que não fazem parte da transmissão.

No Método 1, o programa utiliza um **threshold (limiar)** para ajudar nessa identificação:

```python
threshold = 0.03
```

As amostras cuja amplitude ultrapassa esse valor são consideradas possíveis eventos sonoros, enquanto amplitudes abaixo do limiar são interpretadas como silêncio.

Esse valor pode ser ajustado de acordo com as condições de gravação e com o nível de ruído do ambiente.

## 3.8 Detecção de Erros

Durante uma transmissão, os dados podem sofrer alterações devido ao ruído ou a outros problemas do meio de comunicação.

Por exemplo:

```text
Enviado:  10110010
Recebido: 10100010
```

Nesse caso, um dos bits foi alterado.

Por isso, os métodos de transmissão precisam utilizar mecanismos de detecção de erros, capazes de indicar quando os dados recebidos podem estar diferentes dos dados enviados.

### 3.8.1 Paridade Par

No Método 1, deve ser utilizado um quadro de **9 bits**, formado por:

- 8 bits de dados;
- 1 bit de paridade.

A paridade utilizada é a **paridade par**. O objetivo é fazer com que a quantidade total de bits 1 no quadro seja par.

Se os 8 bits de dados já possuem uma quantidade par de 1, o bit de paridade será 0.

Exemplo:

```text
Dados:     10110010
Número de 1: 4
Paridade:  0
Quadro:    101100100
```

Se os 8 bits possuem uma quantidade ímpar de 1, o bit de paridade será 1.

Exemplo:

```text
Dados:     10110011
Número de 1: 5
Paridade:  1
Quadro:    101100111
```

No receptor, os primeiros 8 bits são analisados e o bit de paridade esperado é calculado. Esse valor é comparado com o 9º bit recebido.

Se os valores forem iguais, o quadro passa na verificação de paridade. Se forem diferentes, o receptor indica que houve um possível erro na transmissão.

A paridade é um mecanismo de detecção de erros, não de correção. Ela permite identificar determinados erros, mas não recuperar automaticamente o bit que foi alterado.

## 3.9 Taxa de Transmissão

A taxa de transmissão representa a quantidade de bits transmitidos por segundo e é medida em bits por segundo (bps).

Por exemplo:

```text
10 bits em 1 segundo = 10 bps
```

No projeto, será necessário avaliar tanto a taxa teórica quanto a taxa prática de transmissão.

A taxa teórica representa a velocidade esperada em condições ideais. Já a taxa prática considera fatores como ruído, capacidade de processamento, sincronização e limitações do equipamento utilizado.

Uma velocidade maior pode aumentar a quantidade de dados transmitidos, mas também pode dificultar a identificação correta dos sinais. Por isso, o objetivo é encontrar uma velocidade que mantenha uma transmissão confiável.

---

# 4. Engenharia e Arquitetura das Soluções

## 4.1 Visão Geral do Sistema

O sistema é composto por um software responsável pela transmissão e recepção de informações utilizando sinais sonoros.

No Método 1, o receptor utiliza o microfone para captar as batidas. O áudio captado é convertido em amostras digitais e processado para identificar as batidas e os intervalos de silêncio.

O funcionamento pode ser representado como:

```text
Batidas sonoras
      ↓
Microfone
      ↓
Gravação do áudio
      ↓
Processamento das amostras
      ↓
Detecção das batidas
      ↓
Identificação dos bits
      ↓
Quadro de 9 bits
      ↓
Verificação de paridade
```

## 4.2 Método 1 — Transmissão por Batidas

O Método 1 utiliza eventos sonoros produzidos por impacto, como:

- batidas de caneta em uma mesa, superfície ou quadro;
- batidas de palma da mão;
- estalar de dedos.

O padrão de representação dos bits é:

```text
Bit 0 = silêncio + 1 batida + silêncio

Bit 1 = silêncio + 2 batidas consecutivas + silêncio
```

Assim, uma única batida representa o bit **0**, enquanto duas batidas consecutivas representam o bit **1**.

A transmissão deve seguir a cadência, o ritmo e o padrão estabelecidos no vídeo de referência fornecido na atividade.

O receptor identifica as batidas a partir do áudio captado pelo microfone e utiliza os intervalos de silêncio para separar os símbolos transmitidos.

No processamento do sinal, o programa utiliza um threshold para diferenciar possíveis eventos sonoros do silêncio.

Após a detecção, os símbolos são classificados de acordo com a quantidade de batidas:

```text
1 batida → 0
2 batidas → 1
```

Caso sejam identificadas quantidades diferentes de batidas dentro de um símbolo, o evento é considerado inválido.

## 4.3 Estrutura do Quadro de 9 Bits

O Método 1 utiliza um quadro composto por **9 bits**:

```text
8 bits de dados + 1 bit de paridade
```

Os primeiros 8 bits representam a informação transmitida.

O 9º bit é utilizado para verificar a paridade do quadro.

Exemplo:

```text
Dados:
10110010

Paridade:
0

Quadro:
101100100
```

O receptor precisa receber exatamente 9 bits para realizar a verificação completa do quadro.

## 4.4 Detecção de Erros do Método 1

A detecção de erros do Método 1 utiliza **paridade par**.

O programa calcula a quantidade de bits 1 presentes nos primeiros 8 bits recebidos.

Se a quantidade de bits 1 for par, o bit de paridade esperado será:

```text
0
```

Se a quantidade de bits 1 for ímpar, o bit de paridade esperado será:

```text
1
```

O bit esperado é comparado com o 9º bit recebido.

Se forem iguais:

```text
SUCESSO
```

Se forem diferentes:

```text
FALHA DE TRANSMISSÃO
```

Essa verificação permite detectar determinados erros ocorridos durante a transmissão.

## 4.5 Método 2 — [nome do método escolhido]

A definir pela equipe.

## 4.6 Detecção de Erros do Método 2

A definir de acordo com o método escolhido para o Método 2.

## 4.7 Taxa de Transmissão

A taxa de transmissão será avaliada considerando o tempo necessário para transmitir os bits e a capacidade do sistema de identificar corretamente os eventos sonoros.

No Método 1, a quantidade de batidas e os intervalos de silêncio influenciam diretamente o tempo necessário para transmitir cada bit.

A taxa prática também pode ser afetada pelo ruído do ambiente, pelo microfone, pelo processamento do áudio e pela sincronização entre transmissor e receptor.

---

# 5. Funcionamento do Software

## 5.1 Emissor

O emissor é responsável por produzir a sequência de eventos sonoros que representa os bits da informação.

No Método 1, cada bit é representado de acordo com o padrão estabelecido:

```text
0 → 1 batida
1 → 2 batidas consecutivas
```

A sequência transmitida possui 8 bits de dados e 1 bit de paridade.

## 5.2 Receptor

O receptor utiliza o microfone para capturar o sinal sonoro.

O processamento realizado pelo programa segue as seguintes etapas:

1. Configuração da taxa de amostragem.
2. Gravação do áudio pelo microfone.
3. Conversão do áudio em amostras digitais.
4. Aplicação do threshold para identificar possíveis eventos sonoros.
5. Separação das batidas.
6. Identificação dos intervalos de silêncio.
7. Agrupamento das batidas em símbolos.
8. Classificação dos símbolos:
   - 1 batida → bit 0;
   - 2 batidas → bit 1.
9. Verificação da quantidade de bits recebidos.
10. Separação dos 8 bits de dados e do bit de paridade.
11. Cálculo da paridade esperada.
12. Comparação com a paridade recebida.
13. Exibição do resultado da transmissão.

De forma simplificada:

```text
Microfone
    ↓
Áudio
    ↓
Threshold
    ↓
Batidas detectadas
    ↓
Agrupamento dos eventos
    ↓
1 batida = 0
2 batidas = 1
    ↓
9 bits
    ↓
8 bits + paridade
    ↓
Verificação
    ↓
SUCESSO / FALHA DE TRANSMISSÃO
```

## 5.3 Bibliotecas Utilizadas

O Método 1 utiliza as seguintes bibliotecas Python:

### NumPy

Utilizada para realizar operações com os dados do áudio, incluindo criação e manipulação de arrays e identificação das amostras que ultrapassam o threshold.

```python
import numpy as np
```

### SoundDevice

Utilizada para acessar o dispositivo de áudio e realizar a gravação pelo microfone.

```python
import sounddevice as sd
```

### Matplotlib

Utilizada para visualizar graficamente o sinal de áudio e auxiliar na análise dos eventos sonoros.

```python
import matplotlib.pyplot as plt
```

## 5.4 Interface/Terminal

A interação com o usuário é realizada principalmente pelo terminal.

Durante a execução, o programa apresenta informações relacionadas à captura e ao processamento do sinal, como:

```text
Microfone captando:
Captura feita.
Quantidade de batidas válidas:
Tamanho das batidas válidas:
Intervalos entre batidas:
Símbolos detectados:
Quantidade de símbolos:
```

Ao final, o programa apresenta o resultado da transmissão e da verificação de paridade.

---

# 6. Divisão de Tarefas da Equipe

A definir pela equipe.

---

# 7. Desafios, Problemas e Soluções

Durante o desenvolvimento do projeto, foram encontrados desafios relacionados à captura e ao processamento do áudio.

Entre eles estão:

- identificação das batidas no sinal captado;
- diferenciação entre batidas e ruídos;
- definição de um threshold adequado;
- separação das batidas consecutivas;
- identificação dos intervalos de silêncio;
- sincronização entre os eventos sonoros;
- necessidade de receber exatamente 9 bits para realizar a verificação de paridade.

Os parâmetros do programa podem precisar de ajustes de acordo com o ambiente de gravação e com o equipamento utilizado.

---

# 8. Demonstração em Vídeo

A definir .

---

# 9. Uso de Inteligência Artificial

A definir 
---

# 10. Conclusão

O projeto apresenta uma implementação prática do funcionamento da Camada Física utilizando o som como meio de transmissão.

No Método 1, eventos sonoros produzidos por batidas são utilizados para representar bits. O microfone captura o sinal, que é processado pelo software para identificar as batidas e convertê-las em uma sequência de bits.

O uso de um quadro de 9 bits, composto por 8 bits de dados e 1 bit de paridade, permite realizar uma verificação de possíveis erros ocorridos durante a transmissão.

Dessa forma, o projeto demonstra conceitos relacionados à transmissão de sinais, amostragem, processamento de áudio, representação digital, ruído e detecção de erros.

---

# 11. Licença

A definir 