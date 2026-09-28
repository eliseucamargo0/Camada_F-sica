import numpy as np          #NumPy, biblioteca para criação de arrays
import sounddevice as sd    #Biblioteca responsavel por ler entrada na placa de audio (microfone)
import matplotlib.pyplot as plt #Biblioteca que serve apenas para vizualizar graficamente audio gravado
from matplotlib.animation import FuncAnimation

fs = 44100
sd.default.samplerate = fs
sd.default.channels = 1

buffer = np.zeros(fs)   # janela de 1 segundo, começa "em silêncio"

def callback(indata, frames, time, status):
    global buffer
    if status:
        print(status)
    buffer = np.roll(buffer, -frames)   # empurra tudo pra esquerda
    buffer[-frames:] = indata[:, 0]     # coloca o pedaço novo no final

fig, ax = plt.subplots()
linha, = ax.plot(buffer)
ax.set_ylim(-1, 1)          # o sounddevice entrega amplitudes entre -1 e 1

def atualizar(frame):
    linha.set_ydata(buffer)  # troca só os valores de Y da linha existente
    return linha,

ani = FuncAnimation(fig, atualizar, interval=30, blit=True)

with sd.InputStream(samplerate=fs, channels=1, blocksize=1024, callback=callback):
    plt.show()