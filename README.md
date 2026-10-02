# Camada Física usando Som
Projeto da disciplina de Redes de Computadores.
O objetivo deste projeto é implementar uma comunicação na camada física utilizando o **som como meio de transmissão**. O projeto possui dois métodos de transmissão:
- **Método 1:** transmissão utilizando impactos sonoros.
- **Método 2:** transmissão utilizando FSK (*Frequency Shift Keying*).
---
## 1. Objetivo
Desenvolver um sistema capaz de transmitir e receber informações utilizando sinais sonoros.
O computador emissor transforma os dados em sinais sonoros, que são reproduzidos pelo alto-falante. O computador receptor utiliza o microfone para capturar o som e posteriormente processar o sinal recebido.
O projeto apresenta duas formas de transmissão:
1. transmissão utilizando impactos sonoros;
2. transmissão utilizando diferentes frequências sonoras.
Além da transmissão, são utilizadas técnicas de detecção de erros para verificar se os dados recebidos estão corretos.
---
## 2. Funcionamento geral
O funcionamento básico do projeto pode ser representado da seguinte forma:
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
# 3. Fundamentação teórica
## 3.1 Camada Física
A camada física é responsável pela transmissão dos bits por meio de um meio físico.
Neste projeto, o meio utilizado é o **som**.
O computador transforma os bits em sinais sonoros, que são transmitidos pelo ambiente até o computador receptor.
---
## 3.2 Comunicação acústica
Na comunicação acústica, as informações são representadas por características do som.
Neste projeto são utilizadas duas formas diferentes:
- impactos sonoros;
- frequências diferentes.
No Método 1, a quantidade de impactos representa o bit.
No Método 2, a frequência utilizada representa o bit.
---
## 3.3 Bits
Um bit pode assumir dois valores:
```text
0
1
```
Os métodos desenvolvidos no projeto utilizam diferentes características do sinal sonoro para representar esses valores.
---
## 3.4 Frequência de amostragem
Os sinais de áudio são processados utilizando uma frequência de amostragem de:
```text
FS = 44100 Hz
```
Isso significa que o áudio é representado por 44.100 amostras por segundo.
Essa frequência é utilizada nos dois métodos.
---
## 3.5 Método 1 — Impactos sonoros
O primeiro método utiliza **impactos sonoros** para representar os bits.
Podem ser utilizados sons produzidos por:
- batidas com uma caneta;
- batidas na mesa;
- batidas em uma superfície;
- palmas;
- estalos.
O receptor utiliza o microfone para capturar o áudio e identifica os impactos presentes no sinal.
---
## 3.6 Representação dos bits
No Método 1:
```text
0 → 1 batida
1 → 2 batidas consecutivas
```
Existe um período de silêncio antes e depois dos símbolos.
O programa analisa a quantidade de batidas encontradas dentro de cada símbolo.
A identificação ocorre da seguinte maneira:
```text
1 batida → 0
2 batidas → 1
outras quantidades → símbolo inválido
```
O ritmo e o padrão das batidas seguem a referência utilizada para a atividade.
---
## 3.7 Detecção das batidas
Para identificar as batidas, o programa utiliza um limite de amplitude chamado **threshold**.
No código atual:
```python
threshold = 0.75
```
O programa verifica quais amostras do áudio possuem amplitude absoluta maior que esse valor.
Essas amostras são consideradas parte de um evento sonoro.
As amostras abaixo do limite são consideradas silêncio.
O programa também utiliza:
```python
tquebra = fs * 0.05
```
Esse valor é utilizado para separar grupos de amostras que pertencem a eventos sonoros diferentes.
---
## 3.8 Quadro do Método 1
O Método 1 utiliza um quadro formado por:
```text
8 bits de dados + 1 bit de paridade
```
O objetivo da paridade é permitir uma verificação simples dos dados.
### 3.8.1 Paridade
É utilizada **paridade par**.
O programa conta a quantidade de bits `1` presentes nos oito bits de dados.
Se a quantidade de bits `1` for par:
```text
paridade = 0
```
Se a quantidade de bits `1` for ímpar:
```text
paridade = 1
```
Assim, o quadro final possui nove bits:
```text
[bit][bit][bit][bit][bit][bit][bit][bit][paridade]
```
Na implementação atual, os oito bits de dados são obtidos a partir das batidas detectadas no áudio.
Depois disso, o programa calcula a paridade localmente e monta o quadro de nove bits.
O nono bit ainda não é obtido de uma transmissão acústica separada; o código utiliza o valor calculado como simulação do recebimento correto da paridade.
---
# 4. Métodos de transmissão
## 4.1 Fluxo do Método 1
O funcionamento do Método 1 pode ser representado por:
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
O programa utiliza uma captura de áudio em tempo real através do `SoundDevice`.
Também é apresentada uma visualização do sinal durante a captura.
A gravação é encerrada quando a janela de visualização é fechada.
---
## 4.2 Fluxo do Método 2
O funcionamento do Método 2 pode ser representado por:
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
## 4.2 Método 1 — Impactos sonoros
O primeiro método utiliza impactos sonoros como forma de representar os bits.
A transmissão segue o seguinte padrão:
```text
Bit 0 → silêncio + 1 batida + silêncio
Bit 1 → silêncio + 2 batidas consecutivas + silêncio
```
O receptor identifica as batidas através do microfone.
O programa utiliza o threshold para diferenciar eventos sonoros de silêncio.
Depois da detecção, as batidas são agrupadas e utilizadas para determinar os símbolos.
A interpretação é:
```text
1 batida → 0
2 batidas → 1
outras quantidades → 3 (símbolo inválido)
```
---
## 4.3 Estrutura do quadro do Método 1
A implementação atual trabalha com oito bits de dados.
Quando exatamente oito bits são identificados, o programa calcula o bit de paridade e monta um quadro de nove bits:
```text
8 bits de dados + 1 bit de paridade
```
Exemplo:
```text
Dados:
1 0 1 0 0 1 0 1
Paridade:
0
Quadro:
1 0 1 0 0 1 0 1 0
```
A paridade é calculada pelo próprio programa a partir dos oito bits identificados.
Atualmente, o nono bit não é transmitido como uma nona sequência acústica. Ele é utilizado no código para representar a paridade calculada.
---
## 4.4 Verificação de paridade
A função `calcular_paridade()` conta a quantidade de bits `1` presentes nos dados.
A função `verificar_paridade()` compara:
```text
Paridade esperada
        ↓
Paridade recebida
```
Na implementação atual, a paridade recebida é simulada utilizando a própria paridade calculada:
```python
paridade_recebida = paridade
```
Quando os valores são iguais, o programa apresenta:
```text
SUCESSO
```
Caso sejam diferentes, apresenta:
```text
FALHA DE TRANSMISSÃO
```
Essa estrutura permite testar a lógica da verificação de paridade, embora o nono bit ainda não esteja sendo transmitido acusticamente.
---
## 4.5 Método 2 — FSK
O segundo método utiliza **FSK (Frequency Shift Keying)**.
Nesse método, cada bit é representado por uma frequência diferente.
A implementação utiliza:
```text
Bit 0 → 440 Hz
Bit 1 → 880 Hz
```
Cada bit possui duração de:
```text
0,12 segundos
```
Portanto, a taxa teórica de transmissão é:
```text
1 / 0,12 ≈ 8,33 bits por segundo
```
O sinal utilizado é uma onda senoidal.
---
## 4.5.1 Estrutura do quadro do Método 2
O quadro utilizado pelo Método 2 possui:
```text
PREÂMBULO + TAMANHO + DADOS + CRC-8
```
O preâmbulo utilizado é:
```text
10101010
```
O campo de tamanho possui um byte e informa a quantidade de bytes da mensagem.
Os dados da mensagem são convertidos para UTF-8.
O último byte contém o CRC-8 utilizado para verificar a integridade dos dados.
Assim:
```text
+------------+---------+---------------+--------+
| Preâmbulo  | Tamanho |     Dados     | CRC-8  |
+------------+---------+---------------+--------+
| 8 bits     | 8 bits  | variável      | 8 bits |
+------------+---------+---------------+--------+
```
---
## 4.5.2 Transmissão do Método 2
O emissor recebe uma mensagem de texto.
Primeiro, a mensagem é convertida para UTF-8.
Depois:
1. é obtido o tamanho da mensagem;
2. é calculado o CRC-8;
3. é formado o quadro;
4. o quadro é convertido para bits;
5. o preâmbulo é adicionado;
6. cada bit é convertido em uma frequência;
7. o sinal sonoro é gerado;
8. o sinal é reproduzido pelo alto-falante.
A conversão utilizada é:
```text
0 → 440 Hz
1 → 880 Hz
```
---
## 4.5.3 Recepção do Método 2
O receptor utiliza o microfone para capturar o áudio.
O áudio é dividido em janelas correspondentes à duração de cada bit:
```text
0,12 segundos
```
Para cada janela, o programa:
1. aplica uma janela de Hanning;
2. calcula a FFT;
3. identifica a magnitude próxima de 440 Hz;
4. identifica a magnitude próxima de 880 Hz;
5. compara as duas magnitudes;
6. determina o bit recebido.
A lógica utilizada é:
```text
440 Hz maior → 0
880 Hz maior → 1
```
Depois da identificação dos bits, o programa procura o preâmbulo:
```text
10101010
```
Após encontrar o preâmbulo, o programa identifica o tamanho da mensagem, recupera os dados e verifica o CRC-8.
---
## 4.6 CRC-8
O Método 2 utiliza **CRC-8** para verificar a integridade da mensagem recebida.
O CRC é calculado a partir do tamanho da mensagem e dos dados.
No receptor são obtidos dois valores:
```text
CRC recebido
CRC calculado
```
Os valores são comparados.
Se forem iguais:
```text
SUCESSO
Dados íntegros.
```
Se forem diferentes:
```text
FALHA DE TRANSMISSÃO
Os dados foram corrompidos.
```
Além da comparação do CRC, o programa também verifica se os dados recebidos podem ser convertidos corretamente para UTF-8.
---
## 4.7 Taxa de transmissão
No Método 2, cada bit possui duração de:
```text
0,12 segundos
```
Portanto:
```text
Taxa = 1 / 0,12
Taxa ≈ 8,33 bps
```
Essa é a taxa teórica de transmissão dos bits.
A taxa efetiva de transmissão de mensagens é menor devido aos dados adicionais do quadro, como:
- preâmbulo;
- campo de tamanho;
- CRC-8.
O valor de 0,12 segundo foi utilizado como uma configuração inicial para permitir a detecção das frequências durante os testes.
---
# 5. Implementação
## 5.1 Emissor
No Método 2, o emissor recebe uma mensagem digitada pelo usuário.
Exemplo:
```text
Mensagem: Teste FSK
```
A mensagem é transformada em bytes, recebe o CRC-8 e é convertida em bits.
Os bits são então transformados em sinais sonoros utilizando as frequências de 440 Hz e 880 Hz.
O sinal é reproduzido pelo alto-falante utilizando a biblioteca `SoundDevice`.
---
## 5.2 Receptor
O receptor utiliza o microfone para capturar o sinal acústico.
No Método 1, o áudio é analisado para identificar as batidas.
No Método 2, o áudio é dividido em janelas de 0,12 segundo e cada janela é analisada utilizando FFT.
Depois da detecção dos bits, o programa realiza as verificações correspondentes a cada método.
No Método 1:
```text
8 bits → cálculo da paridade → quadro de 9 bits
```
No Método 2:
```text
Preâmbulo → tamanho → dados → CRC-8 → mensagem
```
---
## 5.3 Bibliotecas utilizadas
O projeto utiliza principalmente:
### NumPy
Utilizada para:
- manipulação de arrays;
- processamento dos sinais;
- geração das ondas senoidais;
- cálculo da FFT;
- operações matemáticas.
### SoundDevice
Utilizada para:
- gravação pelo microfone;
- reprodução dos sinais pelo alto-falante;
- captura de áudio.
### Matplotlib
Utilizada no Método 1 para:
- visualizar o sinal de áudio;
- acompanhar a captura em tempo real;
- visualizar o resultado do threshold.
A biblioteca padrão `time` também aparece importada no Método 2, embora a implementação atual não dependa de funções dessa biblioteca para realizar a transmissão.
---
## 5.4 Menu do programa
O programa possui um menu principal:
```text
1 - Teste local
2 - Receber pelo microfone
3 - Transmitir mensagem
0 - Sair
```
### Opção 1 — Teste local
Realiza um teste do Método 2 sem utilizar o microfone.
A mensagem:
```text
Teste FSK
```
é transformada em sinal e posteriormente decodificada diretamente pelo programa.
Essa opção permite verificar o funcionamento da codificação, FSK, decodificação e CRC.
### Opção 2 — Receber pelo microfone
Permite capturar um sinal utilizando o microfone.
O usuário informa a duração da gravação e o programa realiza a captura do áudio.
Depois, o sinal é processado e os bits são identificados.
### Opção 3 — Transmitir mensagem
Permite digitar uma mensagem.
O programa cria o quadro, calcula o CRC-8, converte os bits para frequências e reproduz o sinal pelo alto-falante.
### Opção 0 — Sair
Encerra o programa.
---
# 6. Equipe
- Bruno Scarabel
- Desirée Wolff
- Eliseu Camargo
- Giovana Campos
---
# 7. Testes
Foram realizados testes para verificar o funcionamento dos métodos de transmissão.
No Método 1 foram realizados testes de:
- detecção de batidas;
- identificação dos bits;
- formação do quadro de 9 bits;
- cálculo da paridade;
- verificação de paridade.
No Método 2 foram realizados testes de:
- geração do sinal FSK;
- transmissão local;
- identificação das frequências;
- detecção do preâmbulo;
- leitura do tamanho da mensagem;
- recuperação dos dados;
- cálculo e verificação do CRC-8;
- transmissão utilizando microfone e alto-falante.
---
# 8. Vídeo
Será apresentado um vídeo demonstrando o funcionamento dos métodos desenvolvidos.
O vídeo deverá apresentar:
- funcionamento do Método 1;
- funcionamento do Método 2;
- transmissão dos sinais;
- recepção;
- identificação dos dados;
- verificação de erros.
---
# 9. Utilização de Inteligência Artificial
As ferramentas de Inteligência Artificial foram utilizadas como apoio durante o desenvolvimento do projeto.
A utilização ocorreu principalmente para:
- esclarecer conceitos;
- auxiliar na compreensão de erros;
- revisar trechos de código;
- auxiliar na documentação;
- compreender conceitos relacionados à transmissão de dados e processamento de sinais.
As decisões sobre a implementação e os testes foram realizadas pelo grupo.
---
# 10. Conclusão
O projeto apresenta uma implementação de comunicação na camada física utilizando o som como meio de transmissão.
O **Método 1** utiliza impactos sonoros para representar os bits e possui uma verificação de paridade para os dados identificados.
O **Método 2** utiliza FSK, com 440 Hz representando o bit `0` e 880 Hz representando o bit `1`. Cada bit possui duração de 0,12 segundo, resultando em uma taxa teórica de aproximadamente 8,33 bps.
O Método 2 também utiliza:
- preâmbulo;
- campo de tamanho;
- dados em UTF-8;
- CRC-8;
- FFT para identificação das frequências.
Os testes permitem verificar a geração, transmissão, recepção e validação dos dados.
O projeto poderá receber novos ajustes e otimizações durante o desenvolvimento, principalmente relacionados à transmissão acústica e à melhoria da detecção dos sinais.
---
# 11. Licença
A definir.





