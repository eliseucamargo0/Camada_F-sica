import numpy as np
import sounddevice as sd
import time

# MÉTODO 2 - FSK (Frequency Shift Keying)

# Bit 0 -> 440 Hz
# Bit 1 -> 880 Hz

FS = 44100

F0 = 440
F1 = 880

DURACAO_BIT = 0.12

PREAMBULO = [1, 0, 1, 0, 1, 0, 1, 0]

# CRC-8

def calcular_crc8(dados):
    """
    Calcula o CRC-8 dos bytes recebidos.
    """

    crc = 0

    for byte in dados:
        crc ^= byte

        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ 0x07) & 0xFF
            else:
                crc = (crc << 1) & 0xFF

    return crc

# CONVERSÃO DE BYTES PARA BITS

def bytes_para_bits(dados):
    bits = []

    for byte in dados:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)

    return bits


def bits_para_bytes(bits):
    if len(bits) % 8 != 0:
        return None

    dados = bytearray()

    for i in range(0, len(bits), 8):
        byte = 0

        for bit in bits[i:i + 8]:
            byte = (byte << 1) | bit

        dados.append(byte)

    return bytes(dados)

# MONTAGEM DO QUADRO

def criar_quadro(mensagem):
    """
    Estrutura:

    PREÂMBULO
    TAMANHO
    DADOS
    CRC-8
    """

    dados = mensagem.encode("utf-8")

    if len(dados) > 255:
        raise ValueError("Mensagem muito grande. Máximo: 255 bytes.")

    tamanho = len(dados)

    conteudo_crc = bytes([tamanho]) + dados

    crc = calcular_crc8(conteudo_crc)

    quadro = bytes([tamanho]) + dados + bytes([crc])

    bits = PREAMBULO + bytes_para_bits(quadro)

    return bits

# GERAÇÃO DO TOM

def gerar_tom(frequencia, duracao):
    """
    Gera uma senoide na frequência especificada.
    """

    quantidade = int(FS * duracao)

    t = np.arange(quantidade) / FS

    return np.sin(2 * np.pi * frequencia * t)

# EMISSOR FSK

def emitir_bits(bits):
    """
    Converte cada bit em uma frequência:

    0 -> 440 Hz
    1 -> 880 Hz
    """

    sinal = []

    for bit in bits:

        if bit == 0:
            tom = gerar_tom(F0, DURACAO_BIT)
        else:
            tom = gerar_tom(F1, DURACAO_BIT)

        sinal.append(tom)

    if not sinal:
        return np.array([])

    return np.concatenate(sinal)


def transmitir_mensagem(mensagem):
    """
    Cria o quadro, transforma em FSK e reproduz pelo alto-falante.
    """

    bits = criar_quadro(mensagem)

    sinal = emitir_bits(bits)

    print("\n================================")
    print("       TRANSMISSÃO FSK")
    print("================================")

    print("Mensagem:", mensagem)
    print("Bits transmitidos:", len(bits))

    taxa = 1 / DURACAO_BIT

    print(f"Taxa teórica: {taxa:.2f} bps")

    print("\nTransmitindo...")

    sd.play(sinal.astype(np.float32), FS)
    sd.wait()

    print("Transmissão concluída.")


# DETECÇÃO DE FREQUÊNCIA

def detectar_frequencia(janela):
    """
    Detecta se a janela possui F0 ou F1.

    Em vez de procurar qualquer frequência da FFT,
    verificamos diretamente as duas frequências utilizadas
    pelo protocolo FSK.
    """

    janela = janela * np.hanning(len(janela))

    fft = np.fft.rfft(janela)

    frequencias = np.fft.rfftfreq(len(janela), 1 / FS)

    magnitudes = np.abs(fft)

    indice_f0 = np.argmin(np.abs(frequencias - F0))
    indice_f1 = np.argmin(np.abs(frequencias - F1))

    magnitude_f0 = magnitudes[indice_f0]
    magnitude_f1 = magnitudes[indice_f1]

    if magnitude_f0 > magnitude_f1:
        return 0

    return 1

# DECODIFICAÇÃO DOS BITS

def decodificar_bits(sinal):
    """
    Divide o áudio em janelas e identifica cada bit.
    """

    tamanho_bit = int(FS * DURACAO_BIT)

    quantidade_bits = len(sinal) // tamanho_bit

    bits = []

    for i in range(quantidade_bits):

        inicio = i * tamanho_bit
        fim = inicio + tamanho_bit

        janela = sinal[inicio:fim]

        if len(janela) < tamanho_bit:
            break

        bit = detectar_frequencia(janela)

        bits.append(bit)

    return bits

# LOCALIZAÇÃO DO PREÂMBULO

def encontrar_preambulo(bits):
    """
    Procura a sequência:

    10101010

    usada para identificar o início do quadro.
    """

    tamanho = len(PREAMBULO)

    for i in range(len(bits) - tamanho + 1):

        if bits[i:i + tamanho] == PREAMBULO:
            return i + tamanho

    return -1

# RECEPÇÃO E VERIFICAÇÃO

def processar_bits(bits):
    """
    Localiza o quadro, recupera os dados e verifica o CRC.
    """

    inicio = encontrar_preambulo(bits)

    if inicio == -1:
        print("\nFALHA DE TRANSMISSÃO")
        print("Preâmbulo não encontrado.")
        return None

    bits_quadro = bits[inicio:]
    
    if len(bits_quadro) < 8:
        print("\nFALHA DE TRANSMISSÃO")
        print("Quadro incompleto.")
        return None

    # Primeiro byte = tamanho da mensagem
    tamanho_bits = bits_quadro[:8]

    tamanho_bytes = bits_para_bytes(tamanho_bits)[0]

    quantidade_total_bits = (1 + tamanho_bytes + 1) * 8

    if len(bits_quadro) < quantidade_total_bits:
        print("\nFALHA DE TRANSMISSÃO")
        print("Quadro incompleto.")
        return None

    quadro = bits_para_bytes(
        bits_quadro[:quantidade_total_bits]
    )

    if quadro is None:
        print("\nFALHA DE TRANSMISSÃO")
        return None

    tamanho = quadro[0]

    dados = quadro[1:1 + tamanho]

    crc_recebido = quadro[1 + tamanho]

    dados_crc = bytes([tamanho]) + dados

    crc_calculado = calcular_crc8(dados_crc)

    print("\n================================")
    print("          RESULTADO")
    print("================================")

    print("CRC recebido:", hex(crc_recebido))
    print("CRC calculado:", hex(crc_calculado))

    if crc_recebido != crc_calculado:

        print("\nFALHA DE TRANSMISSÃO")
        print("Os dados foram corrompidos.")

        return None

    try:
        mensagem = dados.decode("utf-8")
    except UnicodeDecodeError:

        print("\nFALHA DE TRANSMISSÃO")
        print("Dados inválidos.")

        return None

    print("\nSUCESSO")
    print("Dados íntegros.")
    print("Mensagem recebida:", mensagem)

    return mensagem

# RECEPÇÃO PELO MICROFONE

def receber_microfone(duracao):
    """
    Grava o áudio através do microfone.
    """

    print("\n================================")
    print("        RECEPÇÃO FSK")
    print("================================")

    print(f"Gravando por {duracao:.1f} segundos...")
    print("Fale/transmita o sinal agora.")

    audio = sd.rec(
        int(duracao * FS),
        samplerate=FS,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    print("Gravação concluída.")

    return audio[:, 0]

# TESTE LOCAL

def teste_local():
    """
    Testa o método sem utilizar microfone.
    """

    mensagem = "Teste FSK"

    print("\n================================")
    print("          TESTE LOCAL")
    print("================================")

    bits = criar_quadro(mensagem)

    print("Mensagem original:", mensagem)
    print("Quantidade de bits:", len(bits))

    sinal = emitir_bits(bits)

    bits_recebidos = decodificar_bits(sinal)

    processar_bits(bits_recebidos)

# TESTE COM MICROFONE

def teste_microfone():
    """
    O receptor grava o áudio pelo microfone.

    Em outro computador deve estar sendo executada
    a transmissão.
    """

    mensagem = input("\nMensagem a transmitir: ")

    bits = criar_quadro(mensagem)

    duracao_total = len(bits) * DURACAO_BIT

    print("\nPrepare o outro computador para transmitir.")

    input(
        "\nPressione ENTER quando estiver pronto para iniciar "
        "a gravação do microfone..."
    )

    # Pequena margem para iniciar a transmissão
    duracao_gravacao = duracao_total + 3

    audio = receber_microfone(duracao_gravacao)

    print("\nProcessando áudio...")

    bits_recebidos = decodificar_bits(audio)

    print("Bits detectados:", len(bits_recebidos))

    processar_bits(bits_recebidos)

# MENU

def main():

    while True:

        print("\n======================================")
        print("       MÉTODO 2 - FSK")
        print("======================================")

        print("1 - Teste local")
        print("2 - Receber pelo microfone")
        print("3 - Transmitir mensagem")
        print("0 - Sair")

        opcao = input("\nEscolha: ")

        if opcao == "1":

            teste_local()

        elif opcao == "2":

            duracao = float(
                input("Duração da gravação em segundos: ")
            )

            audio = receber_microfone(duracao)

            bits = decodificar_bits(audio)

            print("\nBits detectados:", bits)

            processar_bits(bits)

        elif opcao == "3":

            mensagem = input("\nMensagem: ")

            transmitir_mensagem(mensagem)

        elif opcao == "0":

            print("Encerrando.")

            break

        else:

            print("Opção inválida.")


if __name__ == "__main__":
    main()
