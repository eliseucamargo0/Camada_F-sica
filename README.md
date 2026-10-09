# Video demonstração

https://youtube.com/shorts/BogOcquUeyQ?feature=share

# Camada Física usando Som

Projeto da disciplina de Redes de Computadores.

O objetivo é implementar uma comunicação na camada física utilizando o **som como meio de transmissão**. O projeto possui dois métodos:

- **Método 1:** transmissão utilizando impactos sonoros (batidas);
- **Método 2:** transmissão utilizando FSK (*Frequency Shift Keying*).

---

## 1. Objetivo

Desenvolver um sistema capaz de transmitir e receber informações utilizando sinais sonoros.

O computador emissor transforma os dados em sinais sonoros, reproduzidos pelo alto-falante. O computador receptor usa o microfone para capturar o som e processa o sinal recebido. Além da transmissão, são utilizadas técnicas de detecção de erros (paridade e CRC-8) para verificar se os dados recebidos estão corretos.

---

## 2. Funcionamento geral

```text
Emissor
   ↓
Conversão dos dados em bits
   ↓
Codificação dos bits
   ↓
Geração do sinal sonoro
   ↓
Alto-falante
   ↓
Meio acústico
   ↓
Microfone
   ↓
Processamento do áudio
   ↓
Decodificação
   ↓
Verificação dos dados
   ↓
Receptor
```

O processo utilizado depende do método escolhido.

---

## 3. Estrutura do projeto

| Arquivo | Função |
|---|---|
| `main.py` | Hub com o menu principal. Carrega cada módulo somente quando escolhido. |
| `estetica_oficial.py` | Visual do terminal (título, cores). |
| `metodo_um.py` | Método 1 — batidas, no terminal. |
| `grafico_oficial.py` | Método 1 — batidas com gráficos em tempo real. |
| `metodo_dois.py` | Método 2 — FSK (emissor e receptor). |
| `paridade_oficial.py` | Demonstração da paridade par. |

O `main.py` localiza os módulos ignorando acentos, maiúsculas/minúsculas e o prefixo `teste_` no nome do arquivo. Se algum arquivo estiver ausente, o menu informa quais `.py` existem na pasta, e um erro em um método não encerra o programa.

---

## 4. Instalação e execução

Requisitos: Python 3 e as bibliotecas abaixo.

```bash
pip install numpy sounddevice matplotlib
```

Para executar:

```bash
python main.py
```

### 4.1 Menu principal

```text
[1] Método 1 — Batidas (terminal)
[2] Método 1 — Batidas com gráficos
[3] Método 2 — FSK (frequências)
[4] Demonstração de paridade
[q] Sair
```

- **Ctrl+C** durante um método interrompe a execução e volta ao menu.
- Se uma dependência ou arquivo estiver faltando, o menu exibe a mensagem e sugere o comando `pip install`.

### 4.2 Opções do Método 2

O módulo do Método 2 oferece:

1. **Teste local:** codifica e decodifica a mensagem `Teste FSK` sem microfone, validando codificação, FSK, decodificação e CRC.
2. **Receber pelo microfone:** o usuário informa a duração da gravação; o sinal é processado e os bits são identificados.
3. **Transmitir mensagem:** o usuário digita a mensagem; o programa monta o quadro, calcula o CRC-8 e reproduz o sinal pelo alto-falante.

---

## 5. Fundamentação teórica

### 5.1 Camada Física

A camada física é responsável pela transmissão dos bits por meio de um meio físico. Neste projeto, o meio é o **som**: o computador transforma os bits em sinais sonoros, que viajam pelo ambiente até o computador receptor.

### 5.2 Comunicação acústica

As informações são representadas por características do som:

- No Método 1, a **quantidade de impactos** representa o bit.
- No Método 2, a **frequência** utilizada representa o bit.

### 5.3 Bits

Um bit pode assumir os valores `0` ou `1`. Cada método usa uma característica diferente do sinal sonoro para representá-los.

### 5.4 Frequência de amostragem

```text
FS = 44100 Hz
```

O áudio é representado por 44.100 amostras por segundo, nos dois métodos.

---

## 6. Método 1 — Impactos sonoros

Os bits são representados por sons como batidas de caneta, batidas na mesa ou em outra superfície, palmas e estalos. O receptor captura o áudio pelo microfone e identifica os impactos no sinal.

### 6.1 Representação dos bits

```text
Bit 0 → silêncio + 1 batida + silêncio
Bit 1 → silêncio + 2 batidas consecutivas + silêncio
```

Na recepção, a quantidade de batidas em cada símbolo é interpretada assim:

```text
1 batida  → 0
2 batidas → 1
outras quantidades → símbolo inválido
```

O ritmo e o padrão das batidas seguem a referência utilizada para a atividade.

### 6.2 Detecção das batidas

O programa usa um limite de amplitude (**threshold**):

```python
threshold = 0.75
```

Amostras com amplitude absoluta maior que esse valor são consideradas parte de um evento sonoro; as demais são consideradas silêncio.

Também é utilizado:

```python
tquebra = fs * 0.05
```

Esse valor separa grupos de amostras que pertencem a eventos sonoros diferentes (50 ms).

### 6.3 Quadro e paridade

O quadro do Método 1 é formado por:

```text
8 bits de dados + 1 bit de paridade
```

É utilizada **paridade par**: o programa conta os bits `1` nos oito bits de dados.

```text
quantidade de 1s par   → paridade = 0
quantidade de 1s ímpar → paridade = 1
```

Exemplo:

```text
Dados:    1 0 1 0 0 1 0 1
Paridade: 0
Quadro:   1 0 1 0 0 1 0 1 0
```

As funções `calcular_paridade()` e `verificar_paridade()` calculam e comparam a paridade esperada com a recebida. Quando são iguais, o programa exibe `SUCESSO`; caso contrário, `FALHA DE TRANSMISSÃO`.

> **Limitação atual:** os oito bits de dados são obtidos das batidas detectadas, mas o nono bit **ainda não é transmitido acusticamente**. O código usa a paridade calculada localmente como simulação do recebimento correto (`paridade_recebida = paridade`). Essa estrutura permite testar a lógica da verificação, mas ainda não detecta erros reais de transmissão da paridade.

### 6.4 Fluxo do Método 1

```text
Batidas
   ↓
Microfone
   ↓
Gravação do áudio
   ↓
Processamento do sinal
   ↓
Detecção das batidas
   ↓
Identificação dos símbolos
   ↓
8 bits
   ↓
Cálculo da paridade
   ↓
Quadro de 9 bits
```

A captura é feita em tempo real com o `SoundDevice`, e o sinal é visualizado durante a gravação. A gravação termina quando a janela de visualização é fechada.

---

## 7. Método 2 — FSK

Cada bit é representado por uma frequência diferente:

```text
Bit 0 → 440 Hz
Bit 1 → 880 Hz
```

O sinal é uma onda senoidal e cada bit dura **0,12 s**. A taxa teórica é:

```text
Taxa = 1 / 0,12 ≈ 8,33 bps
```

A taxa efetiva de mensagens é menor, devido aos dados adicionais do quadro (preâmbulo, tamanho e CRC-8). O valor de 0,12 s foi usado como configuração inicial para permitir a detecção das frequências durante os testes.

### 7.1 Estrutura do quadro

```text
+------------+---------+---------------+--------+
| Preâmbulo  | Tamanho |     Dados     | CRC-8  |
+------------+---------+---------------+--------+
| 8 bits     | 8 bits  | variável      | 8 bits |
+------------+---------+---------------+--------+
```

- **Preâmbulo:** `10101010`.
- **Tamanho:** um byte com a quantidade de bytes da mensagem.
- **Dados:** mensagem em UTF-8.
- **CRC-8:** verifica a integridade dos dados. É calculado a partir do tamanho e dos dados.

### 7.2 Transmissão

1. A mensagem de texto é convertida para UTF-8;
2. é obtido o tamanho da mensagem;
3. é calculado o CRC-8;
4. é formado o quadro;
5. o quadro é convertido para bits;
6. o preâmbulo é adicionado;
7. cada bit é convertido em uma frequência (`0 → 440 Hz`, `1 → 880 Hz`);
8. o sinal sonoro é gerado e reproduzido pelo alto-falante (`SoundDevice`).

### 7.3 Recepção

O áudio é dividido em janelas de 0,12 s. Para cada janela, o programa:

1. aplica uma janela de Hanning;
2. calcula a FFT;
3. identifica a magnitude próxima de 440 Hz;
4. identifica a magnitude próxima de 880 Hz;
5. compara as duas magnitudes (`440 Hz maior → 0`, `880 Hz maior → 1`).

Depois, o programa procura o preâmbulo `10101010`, lê o tamanho, recupera os dados e verifica o CRC-8.

### 7.4 CRC-8

No receptor são obtidos o **CRC recebido** e o **CRC calculado**:

```text
Iguais     → SUCESSO — Dados íntegros.
Diferentes → FALHA DE TRANSMISSÃO — Os dados foram corrompidos.
```

O programa também verifica se os dados recebidos podem ser convertidos corretamente para UTF-8.

### 7.5 Fluxo do Método 2

```text
Mensagem
   ↓
Conversão para bytes
   ↓
CRC-8
   ↓
Formação do quadro
   ↓
Conversão para bits
   ↓
FSK
   ↓
Alto-falante
   ↓
Meio acústico
   ↓
Microfone
   ↓
FFT
   ↓
Detecção das frequências
   ↓
Bits
   ↓
CRC-8
   ↓
Mensagem
```

---

## 8. Bibliotecas utilizadas

- **NumPy:** manipulação de arrays, processamento dos sinais, geração das ondas senoidais, FFT e operações matemáticas.
- **SoundDevice:** gravação pelo microfone e reprodução pelo alto-falante.
- **Matplotlib:** visualização do sinal, acompanhamento da captura em tempo real e do resultado do threshold (Método 1 com gráficos).

Também são usadas bibliotecas padrão do Python (`os`, `sys`, `importlib`, `runpy`, `unicodedata`) no menu principal.

---

## 9. Testes

**Método 1:** detecção de batidas; identificação dos bits; formação do quadro de 9 bits; cálculo e verificação da paridade.

**Método 2:** geração do sinal FSK; transmissão local; identificação das frequências; detecção do preâmbulo; leitura do tamanho; recuperação dos dados; cálculo e verificação do CRC-8; transmissão com microfone e alto-falante.

---

## 10. Vídeo

Será apresentado um vídeo demonstrando o funcionamento dos métodos, mostrando o Método 1, o Método 2, a transmissão dos sinais, a recepção, a identificação dos dados e a verificação de erros.

---

## 11. Equipe

- Bruno Scarabel — 2707209
- Desirée Wolff — 2811642
- Eliseu Camargo — 2429292
- Giovana Campos — 2811715

---

## 12. Utilização de Inteligência Artificial

Ferramentas de IA foram utilizadas como apoio durante o desenvolvimento, principalmente para esclarecer conceitos, auxiliar na compreensão de erros, revisar trechos de código, auxiliar na documentação e compreender conceitos de transmissão de dados e processamento de sinais. As decisões sobre a implementação e os testes foram realizadas pelo grupo.

---

## 13. Conclusão

O projeto implementa uma comunicação na camada física utilizando o som como meio.

O **Método 1** usa impactos sonoros para representar os bits e possui verificação de paridade para os dados identificados (com o nono bit ainda simulado). O **Método 2** usa FSK, com 440 Hz para o bit `0` e 880 Hz para o bit `1`, 0,12 s por bit (≈ 8,33 bps teóricos), além de preâmbulo, campo de tamanho, dados em UTF-8, CRC-8 e FFT para identificação das frequências.

Como próximos passos, o projeto poderá receber ajustes e otimizações, principalmente na transmissão acústica (incluindo a transmissão real do bit de paridade) e na melhoria da detecção dos sinais.

---

## 14. Licença

Este projeto é distribuído sob a **Licença MIT**. Consulte o arquivo [`LICENSE`](LICENSE) para o texto completo.
