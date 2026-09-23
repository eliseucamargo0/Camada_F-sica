import numpy as np          #NumPy, biblioteca para criação de arrays
import sounddevice as sd    #Biblioteca responsavel por ler entrada na placa de audio (microfone)

# 1. Parâmetros do sinal analógico
fs = 44100                      # Deve ser ajustado de acordo com microfone, define total de amostras
tempo_total = 10                # segundos de duração da gravação
sd.default.samplerate = fs      # Declara padrão para frequencia, que vai ser usado posteriormente 
sd.default.channels = 2         # Declara padrão para canais, que vai ser usado posteriormente


print("Microfone captando:")    #Marca o inicio da gravação para o usuario
gravacao=sd.rec(                #É a chamada da biblioteca que liga o microfone e capta de acordo com o tempo total dado. 
    int(tempo_total*fs)
)
sd.wait()                       #Pausa de 2 segundos depois da gravação acabar
print("Captura feita.")         #Marca termino da gravação
