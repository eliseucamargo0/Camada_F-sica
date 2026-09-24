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

threshold=0.2

sinal = (np.abs(gravacao) > threshold)#Define o threshold criando novo array apenas com verdadeiro em batidas e falso em silencio
plt.plot(sinal)         
plt.xlabel("Amostras")
plt.ylabel("Verdadeiro/Falso")        
plt.show()                            #Cria gráfico de sinais.