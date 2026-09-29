import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt


# MÉTODO 2 - FSK (Frequency Shift Keying)
#   bit 0 → tom em F0
#   bit 1 → tom em F1 


fs = 44100          # taxa de amostragem
duracao_bit = 0.3   # duração de cada bit em segundos

# Frequências escolhidas (precisam ser audíveis e distintas)
F0 = 440    # Hz - frequência para bit 0
F1 = 880    # Hz - frequência para bit 1


# EMISSOR: gerar o som de uma sequência de bits


def gerar_tom(frequencia, duracao, fs):
    """Gera uma senoide pura na frequência desejada."""
    t = np.linspace(0, duracao, int(fs * duracao), endpoint=False)
    sinal = np.sin(2 * np.pi * frequencia * t)
    return sinal


def emitir_bits(bits, duracao_bit, fs):
    """
    Converte uma lista de bits em um sinal de áudio.
    Cada bit vira um tom na frequência correspondente.
    """
    sinal = np.array([])

    for bit in bits:
        if bit == 0:
            tom = gerar_tom(F0, duracao_bit, fs)
        else:
            tom = gerar_tom(F1, duracao_bit, fs)

        # Adiciona um pequeno silêncio entre os bits para facilitar a detecção
        silencio = np.zeros(int(fs * 0.05))
        sinal = np.concatenate([sinal, tom, silencio])

    return sinal


# Teste do emissor
bits_enviados = [1, 0, 1, 1, 0, 0, 1, 0]
print("Bits enviados:", bits_enviados)

sinal = emitir_bits(bits_enviados, duracao_bit, fs)

# Visualiza o sinal gerado
plt.figure(figsize=(12, 4))
plt.plot(sinal[:2000])
plt.title("Sinal gerado (início) - veja como a frequência muda entre os bits")
plt.xlabel("Amostra")
plt.ylabel("Amplitude")
plt.show()

# Toca o som
print("Tocando o som...")
sd.play(sinal.astype(np.float32), samplerate=fs)
sd.wait()
print("Fim da reprodução.")

#RECEPTOR: detectar a frequência de cada janela
def detectar_frequencia(janela, fs):
    """
    Usa FFT para descobrir a frequência dominante de um pedaço de áudio.
    Retorna a frequência em Hz.
    """
    # Aplica uma janela de Hanning para reduzir artefatos da FFT
    janela_hann = janela * np.hanning(len(janela))

    # Calcula a FFT (Transformada Rápida de Fourier)
    fft_resultado = np.fft.rfft(janela_hann)

    # Pega o valor absoluto (magnitude) de cada frequência
    magnitudes = np.abs(fft_resultado)

    # Descobre qual frequência tem a maior magnitude
    freq_indices = np.fft.rfftfreq(len(janela), d=1/fs)
    freq_dominante = freq_indices[np.argmax(magnitudes)]

    return freq_dominante

def receber_sinal(sinal, duracao_bit, fs):
    """
    Divide o sinal em janelas (uma por bit) e detecta a frequência de cada uma.
    """
    # Tamanho de cada janela = duração do bit em amostras
    tamanho_janela = int(fs * duracao_bit)

    # Tamanho do silêncio entre bits (para pular)
    tamanho_silencio = int(fs * 0.05)

    # Tamanho total de cada "slot" (bit + silêncio)
    slot = tamanho_janela + tamanho_silencio

    bits_recebidos = []
    posicao = 0

    while posicao + tamanho_janela <= len(sinal):
        # Extrai a janela do bit atual
        janela = sinal[posicao:posicao + tamanho_janela]

        # Detecta a frequência
        freq = detectar_frequencia(janela, fs)

        # Decide se é 0 ou 1 baseado na frequência detectada
        # Usamos o ponto médio entre F0 e F1 como threshold
        threshold_freq = (F0 + F1) / 2
        if freq < threshold_freq:
            bits_recebidos.append(0)
        else:
            bits_recebidos.append(1)

        # Avança para o próximo slot
        posicao += slot

    return bits_recebidos


#Teste do receptor com o sinal gerado (sem ruído)
print("\nTeste sem ruído")
bits_detectados = receber_sinal(sinal, duracao_bit, fs)
print("Bits detectados:", bits_detectados)
print("Correto?", bits_enviados == bits_detectados)

#TESTE COM RUÍDO
# Adiciona ruído aleatório ao sinal para simular um ambiente real
ruido = np.random.normal(0, 0.3, len(sinal))
sinal_com_ruido = sinal + ruido

print("\n--- Teste com ruído ---")
bits_com_ruido = receber_sinal(sinal_com_ruido, duracao_bit, fs)
print("Bits detectados:", bits_com_ruido)
print("Correto?", bits_enviados == bits_com_ruido)

# Visualiza o sinal com ruído
plt.figure(figsize=(12, 4))
plt.plot(sinal_com_ruido[:2000])
plt.title("Sinal com ruído (início)")
plt.xlabel("Amostra")
plt.ylabel("Amplitude")
plt.show()