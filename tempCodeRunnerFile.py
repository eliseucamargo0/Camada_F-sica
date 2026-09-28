import numpy as np          #NumPy, biblioteca para criação de arrays
import sounddevice as sd    #Biblioteca responsavel por ler entrada na placa de audio (microfone)
import matplotlib.pyplot as plt #Biblioteca que serve apenas para vizualizar graficamente audio gravado

fs = 44100
sd.default.samplerate = fs
sd.default.channels = 1

def callback(indata, frames, time, status):
    if status:
        print(status)          # avisa se algo deu errado 
    print(indata.shape)


stream = sd.InputStream(
    blocksize=1024,       # quantas amostras vêm em CADA chamada do callback
    callback=callback
)

with sd.InputStream(samplerate=fs, channels=1, blocksize=1024, callback=callback):
    sd.sleep(5000)  # mantém o programa "vivo" por 5 segundos enquanto o callback dispara sozinho