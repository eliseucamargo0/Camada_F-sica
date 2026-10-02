# Licença: MIT (ajuste para a licença escolhida pela equipe)
# Camada Física usando Som - Redes de Computadores
"""
metodo_um.py - Método 1 (batidas): EMISSOR e RECEPTOR.

    Bit 0 = silêncio + 1 batida  + silêncio
    Bit 1 = silêncio + 2 batidas + silêncio
    Quadro = 8 bits de dados + 1 bit de paridade par (9 bits)

O receptor usa o 9º bit RECEBIDO (batido por quem transmite) para validar o quadro;
por isso uma paridade errada gera FALHA DE TRANSMISSÃO de verdade.
O visual fica em testeestetico.py.

Rodar:  python metodo_um.py
"""
import threading
import time
from datetime import datetime

import numpy as np

from testeestetico import (Painel, cor, titulo, ler_tecla, modo_teclado,
                      CIANO, VERDE, AMARELO, VERMELHO, CINZA, TEXTO)

# ----------------------------------------------------------------------------
# CADÊNCIA E LIMIARES  (ajuste aqui para casar com o vídeo de referência)
# Medidos no vídeo do simulador: 2ª batida ~0,3 s depois da 1ª; ≥ 1,4 s entre bits.
# ----------------------------------------------------------------------------
FS = 44100
T_ENTRE_BATIDAS = 0.30     # EMISSOR: intervalo entre as 2 batidas do bit 1 (s)
T_SILENCIO_SIMBOLO = 1.50  # EMISSOR: silêncio entre o fim de um bit e o próximo (s)
T_QUEBRA = 0.05            # RECEPTOR: amostras acima do limiar a menos disso = mesma batida
T_FIM_SIMBOLO = 0.45       # RECEPTOR: silêncio que encerra um bit (> 0,30 e < 1,50)
T_MAX_BATIDA = 0.25        # RECEPTOR: "batida" mais longa que isso é ruído (voz, tosse)
T_TIMEOUT_QUADRO = 6.0     # RECEPTOR: quadro incompleto parado por isso é descartado
BITS_DADOS, BITS_QUADRO = 8, 9
SIMBOLO_INVALIDO = 3       # 3+ batidas (ou 0) no mesmo bit

# ----------------------------------------------------------------------------
# Quadro e paridade
# ----------------------------------------------------------------------------
def calcular_paridade(bits):
    """Paridade par: 0 se a quantidade de 1s for par, 1 se for ímpar."""
    return sum(bits) % 2


def verificar_paridade(bits, paridade_recebida):
    return calcular_paridade(bits) == paridade_recebida


def caractere_para_bits(c):
    return [int(b) for b in format(ord(c), "08b")]


def bits_para_caractere(bits):
    return chr(int("".join(map(str, bits)), 2))


def montar_quadro(dados):
    """8 bits de dados -> quadro de 9 bits (dados + paridade par)."""
    return list(dados) + [calcular_paridade(dados)]


def validar_quadro(bits):
    """Valida os 9 bits RECEBIDOS. Retorna (ok, motivo)."""
    if len(bits) != BITS_QUADRO:
        return False, "Quadro incompleto"
    if SIMBOLO_INVALIDO in bits:
        return False, "Símbolo inválido (ruído ou batidas demais)"
    esperada = calcular_paridade(bits[:BITS_DADOS])
    if esperada != bits[BITS_DADOS]:
        return False, f"Paridade esperada {esperada}, recebida {bits[BITS_DADOS]}"
    return True, ""


# ----------------------------------------------------------------------------
# EMISSOR: gera as batidas pelo alto-falante
# ----------------------------------------------------------------------------
def gerar_clique(fs=FS):
    """Som de UMA batida: 'boing' de desenho animado (180 ms)."""
    dur = 0.2
    t = np.arange(int(dur * fs)) / fs
    f = 400 + 350 * np.exp(-t / 0.05) + 70 * np.sin(2 * np.pi * 28 * t) * np.exp(-t / 0.08)
    fase = 2 * np.pi * np.cumsum(f) / fs
    onda = (np.sin(fase) + 0.3 * np.sin(2 * fase) + 0.1 * np.sin(3 * fase)) \
           * np.minimum(t / 0.003, 1) * np.exp(-t / 0.08)
    return onda / np.abs(onda).max()

def gerar_audio_quadro(bits, fs=FS, t_inicio=0.5, t_final=1.0):
    """Retorna (onda, cliques, duração). cliques = [(tempo_s, índice_do_bit)]."""
    cliques, t = [], t_inicio
    for i, b in enumerate(bits):
        n = 2 if b == 1 else 1
        for k in range(n):
            cliques.append((t + k * T_ENTRE_BATIDAS, i))
        t += (n - 1) * T_ENTRE_BATIDAS + T_SILENCIO_SIMBOLO
    duracao = t + t_final
    onda = np.zeros(int(duracao * fs))
    c = gerar_clique(fs)
    for tc, _ in cliques:
        i0 = int(tc * fs)
        onda[i0:i0 + len(c)] += c
    return np.clip(onda / max(np.abs(onda).max(), 1e-9), -1, 1), cliques, duracao


def emitir(bits, painel):
    """Toca o quadro no alto-falante e anima o painel no mesmo ritmo."""
    import sounddevice as sd
    onda, cliques, duracao = gerar_audio_quadro(bits)
    sd.play(onda, samplerate=FS)
    t0 = time.monotonic()
    print("\033[2J\033[?25l", end="")
    try:
        while True:
            t = time.monotonic() - t0
            if t > duracao:
                break
            enviados, batidas = [], 0
            for i, b in enumerate(bits):
                tempos = [tc for tc, idx in cliques if idx == i]
                if t >= tempos[-1] + 0.15:
                    enviados.append(b)
                else:
                    batidas = sum(1 for tc in tempos if tc <= t)
                    break
            k = int(t * FS)
            painel.desenhar(batidas, enviados, onda[max(0, k - FS):k])
            time.sleep(0.03)
        sd.wait()
        painel.desenhar(0, list(bits), None,
                        cor("Transmissão concluída.", VERDE, True))
    finally:
        print("\033[?25h")


# ----------------------------------------------------------------------------
# RECEPTOR: calibração + detecção em tempo real
# ----------------------------------------------------------------------------
def calcular_threshold(pico_ruido, pico_teste, minimo=0.02, maximo=0.9):
    """Limiar relativo: metade do pico de uma batida de teste (nunca abaixo de 3x o ruído)."""
    if pico_teste >= 3 * pico_ruido and pico_teste >= minimo * 2:
        thr = 0.5 * pico_teste
    else:                                  # não ouviu a batida de teste: valor de segurança
        thr = max(0.15, 6 * pico_ruido)
    return float(np.clip(max(thr, 3 * pico_ruido), minimo, maximo))


def calibrar(fs=FS):
    """Mede o ruído ambiente e uma batida de teste; devolve o limiar."""
    import sounddevice as sd
    titulo("CALIBRAÇÃO DO MICROFONE")
    print(cor(" 1/2  Fique em silêncio por 2 segundos...", TEXTO))
    ruido = sd.rec(int(2 * fs), samplerate=fs, channels=1)
    sd.wait()
    print(cor(" 2/2  Dê UMA batida (como as do bit 0). Gravando 6 segundos...", TEXTO))
    teste = sd.rec(int(6 * fs), samplerate=fs, channels=1)
    sd.wait()
    pr, pt = float(np.abs(ruido).max()), float(np.abs(teste).max())
    thr = calcular_threshold(pr, pt)
    print(cor(f"\n ruído: {pr:.3f}   batida de teste: {pt:.3f}   ->  limiar: {thr:.3f}", VERDE, True))
    if pt < 3 * pr:
        print(cor(" ⚠  Batida de teste não foi ouvida; usando limiar de segurança.", AMARELO))
    return thr


class Receptor:
    """Máquina de estados: cada bloco de áudio entra por processar_bloco()."""

    def __init__(self, fs=FS, threshold=0.5):
        self.fs, self.threshold = fs, threshold
        self.q = int(T_QUEBRA * fs)
        self.t_simbolo = int(T_FIM_SIMBOLO * fs)
        self.max_batida = int(T_MAX_BATIDA * fs)
        self.timeout = int(T_TIMEOUT_QUADRO * fs)
        self.lock = threading.Lock()
        self.reiniciar()

    def reiniciar(self, mensagem=""):
        with self.lock:
            self.onda = np.zeros(self.fs)
            self.n = 0                    # amostras já processadas
            self.rajada_inicio = None     # início do "pico" em andamento
            self.ultimo_hit = None        # última amostra acima do limiar
            self.fim_aceito = 0           # fim da última batida válida
            self.t_atividade = 0
            self.batidas = 0              # batidas do bit atual
            self.bits = []
            self.resultado = None         # (dados, paridade, ok, motivo)
            self.ruidos = 0
            self.mensagem = mensagem
            self.mostrado = False

    def estado(self):
        with self.lock:
            return dict(batidas=self.batidas, bits=list(self.bits), onda=self.onda.copy(),
                        resultado=self.resultado, mensagem=self.mensagem, mostrado=self.mostrado)

    def marcar_mostrado(self):
        with self.lock:
            self.mostrado = True

    def processar_bloco(self, x):
        x = np.asarray(x, dtype=float).ravel()
        with self.lock:
            if self.resultado is not None:      # quadro pronto: espera [r]
                self.n += len(x)
                return
            y = x[-self.fs:]
            self.onda = np.roll(self.onda, -len(y))
            self.onda[-len(y):] = y
            for g in np.nonzero(np.abs(x) > self.threshold)[0] + self.n:
                if self.rajada_inicio is not None and g - self.ultimo_hit > self.q:
                    self._fechar_rajada()
                if self.rajada_inicio is None:
                    self.rajada_inicio = g
                self.ultimo_hit = g
            self.n += len(x)
            self._avancar_tempo()

    # -- internos (chamar com o lock) ---------------------------------------
    def _avancar_tempo(self):
        if self.rajada_inicio is not None and self.n - self.ultimo_hit > self.q:
            self._fechar_rajada()
        if self.rajada_inicio is None:
            if self.batidas and self.n - self.fim_aceito > self.t_simbolo:
                self._fechar_simbolo()
            elif (self.bits and not self.batidas
                  and self.n - self.t_atividade > self.timeout):
                self.bits = []                  # sincronismo: descarta quadro parado
                self.mensagem = "Quadro incompleto descartado (tempo esgotado)."

    def _fechar_rajada(self):
        ini, fim = self.rajada_inicio, self.ultimo_hit
        self.rajada_inicio = None
        if fim - ini > self.max_batida:         # longo demais: voz, tosse, arrasto
            self.ruidos += 1
            return
        if self.batidas and ini - self.fim_aceito > self.t_simbolo:
            self._fechar_simbolo()
        self.batidas += 1
        self.fim_aceito = fim

    def _fechar_simbolo(self):
        bit = {1: 0, 2: 1}.get(self.batidas, SIMBOLO_INVALIDO)
        self.bits.append(bit)
        self.batidas, self.t_atividade, self.mensagem = 0, self.fim_aceito, ""
        if len(self.bits) == BITS_QUADRO:
            ok, motivo = validar_quadro(self.bits)
            self.resultado = (self.bits[:BITS_DADOS], self.bits[BITS_DADOS], ok, motivo)


def salvar(bits):
    nome = datetime.now().strftime("transmissao_%Y%m%d_%H%M%S.txt")
    with open(nome, "w", encoding="utf-8") as f:
        f.write("".join(str(b) for b in bits) + "\n")
    return nome


def receber():
    import sounddevice as sd
    thr = calibrar()
    painel = Painel("RECEPTOR", threshold=thr)
    rx = Receptor(FS, thr)

    def callback(indata, frames, tempo, status):
        rx.processar_bloco(indata[:, 0])

    print("\033[2J\033[?25l", end="")
    try:
        with modo_teclado(), sd.InputStream(samplerate=FS, channels=1,
                                            blocksize=1024, callback=callback):
            while True:
                tecla = ler_tecla()
                if tecla == "q":
                    break
                if tecla == "r":
                    rx.reiniciar(cor("Transmissão atual apagada.", AMARELO))
                    print("\033[2J", end="")
                elif tecla == "s":
                    nome = salvar(rx.estado()["bits"])
                    rx.mensagem = cor(f"Salvo em {nome}", VERDE)
                e = rx.estado()
                if e["resultado"] is None:
                    painel.desenhar(e["batidas"], e["bits"], e["onda"],
                                    cor(e["mensagem"], AMARELO) if e["mensagem"] and "\033" not in e["mensagem"] else e["mensagem"])
                elif not e["mostrado"]:
                    dados, par, ok, motivo = e["resultado"]
                    painel.resultado(dados, par, ok, motivo)
                    if ok:
                        print(f" {cor('Caractere recebido:', TEXTO, True)} "
                              f"{cor(repr(bits_para_caractere(dados)), VERDE, True)}")
                    print(cor(" [r] Reiniciar    [s] Salvar    [q] Sair", CINZA))
                    rx.marcar_mostrado()
                time.sleep(0.05)
    finally:
        print("\033[?25h")


def transmitir():
    painel = Painel("EMISSOR")
    while True:
        titulo("EMISSOR — MÉTODO 1")
        txt = input(" Caractere ASCII para enviar (Enter = voltar): ")
        if not txt:
            return
        if ord(txt[0]) > 127:
            print(cor(" Use um caractere ASCII (0-127).", VERMELHO))
            continue
        bits = montar_quadro(caractere_para_bits(txt[0]))
        if input(" Simular erro de paridade (inverter o 9º bit)? [s/N] ").strip().lower() == "s":
            bits[BITS_DADOS] ^= 1
        print(cor(f" Quadro: {''.join(map(str, bits[:8]))} | {bits[8]}", CIANO, True))
        input(" Aponte o alto-falante para o receptor e pressione Enter...")
        emitir(bits, painel)


def main():
    while True:
        titulo("MÉTODO 1 — BATIDAS (CAMADA FÍSICA)")
        print("  [1] Emissor  (toca as batidas no alto-falante)")
        print("  [2] Receptor (escuta as batidas no microfone)")
        print("  [q] Sair")
        op = input("\n > ").strip().lower()
        if op == "1":
            transmitir()
        elif op == "2":
            receber()
        elif op == "q":
            return


if __name__ == "__main__":
    main()