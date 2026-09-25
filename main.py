import numpy as np          #NumPy, biblioteca para criação de arrays
import sounddevice as sd    #Biblioteca responsavel por ler entrada na placa de audio (microfone)
import matplotlib.pyplot as plt #Biblioteca que serve apenas para vizualizar graficamente audio gravado

# 1. Parâmetros do sinal analógico
fs = 44100                      # Deve ser ajustado de acordo com microfone, define total de amostras
tempo_total = 10                # segundos de duração da gravação
sd.default.samplerate = fs      # Declara padrão para frequencia, que vai ser usado posteriormente 
sd.default.channels = 1         # Declara padrão para canais, que vai ser usado posteriormente


print("Microfone captando:")    #Marca o inicio da gravação para o usuario
gravacao=sd.rec(                #É a chamada da biblioteca que liga o microfone e capta de acordo com o tempo total dado. 
    int(tempo_total*fs)
)
sd.wait()                       #Pausa execução do codigo até o fim da gravação
print("Captura feita.")         #Marca termino da gravação


plt.plot(gravacao)              #Começa gráfico
plt.xlabel("amostra")           #Define eixo de amostra no gráfico
plt.ylabel("amplitude")         #Define eixo de amplitude no gráfico
plt.show()                      #Mostra o gráfico

threshold=0.7

sinal = (np.abs(gravacao) > threshold)              #Define o threshold criando novo array apenas com verdadeiro em batidas e falso em silencio
plt.plot(sinal)         
plt.xlabel("Amostras")
plt.ylabel("Verdadeiro/Falso")        
plt.show()                                          #Cria gráfico de sinais.


tquebra = fs * 0.05                                 #declara microsegundos convertidos para amostras
indice = np.where(sinal)[0]                         #Cria array onde apenas foi denotado true no array sinal 
quebra = np.where(np.diff(indice)>tquebra)[0]+1     #Identifica todas as quebras, separando de fato o silencio das batidas atraves da tquebra
batidas = np.split(indice, quebra)                  #Cria os grupos com indices declarando assim onde há inicio de uma batida e termino de cada uma

batida_inicio = []                                 
batida_fim = []

for i in batidas:   
    batida_inicio.append(i[0])                      #guarda no array o inicio de cada batida no array de inicio
    batida_fim.append(i[-1])                        #guarda no array o termino de cada batida

batida_inicio = np.array(batida_inicio)             
batida_fim = np.array(batida_fim)

silencio = batida_inicio[1:] - batida_fim[:-1]

intervalo = 20000                                   #threshold que decide se é batida dupla ou singular
resultado = []
diferente = np.where(silencio > intervalo)[0] + 1   #Encontra sempre que silencio ocorre
posicoes = np.arange(len(batidas))                  #Enumera todas as batidas
simbolos = np.split(posicoes, diferente)            #cria lista agrupando cada batida onde intervalo aponta para duas batidas
for i in simbolos:
    if len(i) == 1:
        resultado.append(0)                         #Nota que foi batida unica e adiciona 0 ao resultado
    elif len(i) == 2:
        resultado.append(1)                         #Nota que foi batida dupla e adiciona 1 ao resultado
    else:
        resultado.append(3)                         #Controle de erros... pode ser modificado
print(resultado)                                    