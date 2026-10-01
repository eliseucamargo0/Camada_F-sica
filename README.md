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

#### 4.5 Método 2 — Transmissão por FSK

Para o segundo método de transmissão foi escolhida a técnica **FSK (Frequency Shift Keying)**, na qual cada bit é representado por uma frequência diferente.

Neste método foram utilizadas duas frequências:

* **Bit 0 → 440 Hz**
* **Bit 1 → 880 Hz**

A duração utilizada para cada bit é de **0,12 segundos**, resultando em uma taxa teórica de aproximadamente:

**Taxa = 1 / 0,12 ≈ 8,33 bps**

O sinal utilizado é uma onda senoidal, gerada matematicamente pelo programa. Durante a transmissão, cada bit é convertido em seu respectivo tom e enviado pelo alto-falante.

O receptor utiliza o microfone para capturar o áudio. Em seguida, o programa analisa o sinal utilizando a **Transformada Rápida de Fourier (FFT)** para identificar qual das duas frequências está presente e, consequentemente, determinar se o bit recebido é 0 ou 1.

#### 4.5.1 Estrutura da transmissão

O Método 2 utiliza um quadro formado por:

**PREÂMBULO + TAMANHO + DADOS + CRC-8**

O preâmbulo utilizado é:

`10101010`

Sua função é permitir que o receptor identifique onde começa o quadro da mensagem.

O campo **TAMANHO** possui 1 byte e informa quantos bytes existem na mensagem.

O campo **DADOS** contém a mensagem propriamente dita, convertida para bytes utilizando UTF-8.

Por fim, é acrescentado um byte contendo o resultado do **CRC-8**, utilizado para verificar se os dados foram alterados durante a transmissão.

#### 4.5.2 Funcionamento do emissor

O emissor recebe uma mensagem digitada pelo usuário e realiza as seguintes etapas:

1. Converte a mensagem para UTF-8.
2. Verifica o tamanho da mensagem.
3. Calcula o CRC-8.
4. Monta o quadro.
5. Converte os bytes do quadro para bits.
6. Adiciona o preâmbulo.
7. Converte cada bit em uma frequência:

   * 0 → 440 Hz
   * 1 → 880 Hz
8. Reproduz o sinal pelo alto-falante.

O programa também apresenta no terminal a quantidade de bits transmitidos e a taxa teórica de transmissão.

#### 4.5.3 Funcionamento do receptor

O receptor utiliza o microfone para gravar o sinal acústico recebido.

Depois da gravação, o programa divide o áudio em janelas correspondentes à duração de cada bit. Para cada janela é realizada uma análise utilizando FFT.

O programa verifica diretamente as magnitudes das frequências de 440 Hz e 880 Hz:

* Se a magnitude de 440 Hz for maior, o bit é interpretado como **0**.
* Se a magnitude de 880 Hz for maior, o bit é interpretado como **1**.

Depois que os bits são identificados, o receptor procura o preâmbulo `10101010`. Quando encontrado, os bits seguintes são interpretados como o quadro da mensagem.

O primeiro byte informa o tamanho da mensagem. Com essa informação, o receptor consegue identificar quais bytes correspondem aos dados e qual byte corresponde ao CRC.

### 4.6 Detecção de Erros do Método 2 — CRC-8

Para detectar possíveis erros durante a transmissão do Método 2 foi utilizado o **CRC-8 (Cyclic Redundancy Check)**.

O CRC é calculado antes da transmissão utilizando o campo de tamanho da mensagem junto com os dados.

O valor calculado é acrescentado ao final do quadro:

**PREÂMBULO + TAMANHO + DADOS + CRC**

No receptor, o CRC é calculado novamente utilizando os dados recebidos.

São então comparados:

**CRC recebido × CRC calculado**

Se os dois valores forem iguais, o programa considera que os dados recebidos estão íntegros e apresenta:

`SUCESSO`

Caso os valores sejam diferentes, o programa identifica que houve alteração nos dados e apresenta:

`FALHA DE TRANSMISSÃO`

Dessa forma, o CRC-8 permite identificar alterações ocorridas durante a transmissão acústica.

Além da comparação do CRC, o programa também verifica situações como:

* preâmbulo não encontrado;
* quadro incompleto;
* dados inválidos;
* mensagem que não pode ser decodificada em UTF-8.

Nessas situações também é apresentada a indicação de:

`FALHA DE TRANSMISSÃO`

### 4.7 Taxa de Transmissão do Método 2

A duração utilizada atualmente para cada bit é de **0,12 segundos**.

Assim, a taxa teórica é calculada por:

**Taxa = 1 / duração do bit**

**Taxa = 1 / 0,12**

**Taxa ≈ 8,33 bps**

Essa é a taxa teórica do protocolo considerando a duração definida para cada bit. A taxa efetiva de transmissão de uma mensagem também depende da quantidade de bits adicionais utilizados pelo preâmbulo, pelo campo de tamanho e pelo CRC-8.

O valor de 0,12 segundos foi escolhido como parâmetro inicial para buscar um equilíbrio entre velocidade e confiabilidade da comunicação acústica.

Como o objetivo do Método 2 é obter uma transmissão com maior taxa de dados mantendo a confiabilidade diante de ruídos, esse parâmetro pode ser ajustado posteriormente a partir dos testes realizados com o microfone e com diferentes condições de ruído.


# 5. Funcionamento do Software

## 5.1 Emissor

O emissor transforma uma sequência de bits em sinais sonoros.

O processo pode ser representado da seguinte forma:

```text
Sequência de bits
        ↓
Escolha da frequência
        ↓
Geração do tom
        ↓
Inclusão do silêncio
        ↓
Sinal de áudio
        ↓
Reprodução
```

A representação utilizada é:

```text
0 → 440 Hz
1 → 880 Hz
```

---

## 5.2 Receptor

O receptor recebe o sinal de áudio e analisa a frequência predominante de cada intervalo.

O processamento ocorre nas seguintes etapas:

1. Define a duração de cada bit.
2. Divide o sinal em janelas.
3. Aplica a janela de Hanning.
4. Calcula a FFT.
5. Identifica a frequência dominante.
6. Compara a frequência com 660 Hz.
7. Classifica o trecho como 0 ou 1.
8. Avança para o próximo intervalo.
9. Repete o processo para os demais bits.
10. Compara os bits detectados com os bits enviados.

De forma simplificada:

```text
Sinal de áudio
      ↓
Divisão em janelas
      ↓
Janela de Hanning
      ↓
FFT
      ↓
Frequência dominante
      ↓
Comparação com 660 Hz
      ↓
Bit 0 ou Bit 1
      ↓
Sequência recebida
      ↓
Comparação com sequência enviada
```

---

## 5.3 Bibliotecas Utilizadas

### NumPy

A biblioteca NumPy é utilizada para operações matemáticas, criação dos sinais e processamento dos dados.

Também é utilizada para realizar a FFT.

```python
import numpy as np
```

### SoundDevice

A biblioteca SoundDevice é utilizada para reproduzir o sinal sonoro.

```python
import sounddevice as sd
```

### Matplotlib

A biblioteca Matplotlib é utilizada para visualizar graficamente os sinais gerados e os sinais com ruído.

```python
import matplotlib.pyplot as plt
```

---

## 5.4 Interface/Terminal

A interação com o usuário ocorre principalmente pelo terminal.

Durante a execução, o programa apresenta informações como:

```text
Bits enviados: [1, 0, 1, 1, 0, 0, 1, 0]

Tocando o som...

Fim da reprodução.

Teste sem ruído

Bits detectados: [...]

Correto? True
```

No teste com ruído, são apresentados os bits identificados pelo receptor e o resultado da comparação.

---

# 6. Divisão de Tarefas da Equipe

A definir pela equipe.

---

# 7. Desafios, Problemas e Soluções

Durante o desenvolvimento do Método 2, foram considerados alguns desafios relacionados à transmissão e recepção dos sinais sonoros.

Entre eles estão:

* escolha das frequências utilizadas para representar os bits;
* diferenciação entre as frequências F0 e F1;
* definição da duração de cada bit;
* definição do intervalo de silêncio;
* identificação da frequência dominante;
* utilização da FFT;
* sincronização das janelas de análise;
* influência do ruído na transmissão;
* necessidade de manter uma comunicação confiável;
* busca por uma taxa de transmissão maior.

As frequências escolhidas foram:

```text
F0 = 440 Hz
F1 = 880 Hz
```

A diferença entre as frequências permite utilizar um valor intermediário de 660 Hz para classificar os sinais.

O teste com ruído foi incluído para analisar o comportamento do método quando o sinal sofre interferências.

A duração de 0,3 segundo por bit também poderá ser alterada durante os testes para verificar se é possível aumentar a velocidade de transmissão mantendo a confiabilidade.

---

# 8. Demonstração em Vídeo

A definir.

---

# 9. Uso de Inteligência Artificial

A definir de acordo com o desenvolvimento realizado pela equipe.

---

# 10. Conclusão

O Método 2 utiliza a técnica FSK (Frequency Shift Keying) para realizar uma transmissão acústica de informações binárias.

Nesse método, o bit 0 é representado por um tom de 440 Hz e o bit 1 por um tom de 880 Hz.

O emissor gera os sinais sonoros a partir de uma sequência de bits. O receptor analisa o áudio utilizando a FFT para identificar a frequência dominante de cada intervalo e determinar qual bit foi transmitido.

O sistema também possui testes sem ruído e com ruído, permitindo analisar o funcionamento do método em diferentes condições.

A duração atual de cada bit é de 0,3 segundo, com 0,05 segundo de silêncio entre os bits, resultando em uma taxa aproximada de 2,86 bps.

A taxa ainda poderá ser otimizada durante os testes, buscando aumentar a velocidade sem comprometer a identificação correta dos bits em condições de ruído.

A técnica de detecção de erros do Método 2 será acrescentada posteriormente, conforme a escolha da equipe.

---

# 11. Licença

A definir.


