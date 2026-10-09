# Licença: MIT (ajuste para a licença escolhida pela equipe)
# Camada Física usando Som - Redes de Computadores

import io
import os
import sys
import time
import contextlib
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# Paleta (um único conjunto de cores para terminal E gráficos)
# ----------------------------------------------------------------------------
BG, PAINEL, TEXTO = "#0f172a", "#1e293b", "#e2e8f0"
CINZA = "#64748b"
ROSA, VERDE, VERMELHO = "#ff8da1", "#4ade80", "#f87171"
AMARELO, ROXO, CIANO = "#fbbf24", "#a78bfa", "#7dd3fc"

COR_BIT = {0: ROSA, 1: ROXO}     # bit 0 = rosa, bit 1 = roxo
COR_PARIDADE = AMARELO

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": PAINEL, "axes.edgecolor": "#475569",
    "axes.labelcolor": TEXTO, "xtick.color": TEXTO, "ytick.color": TEXTO,
    "text.color": TEXTO, "axes.grid": True, "grid.color": "#334155",
    "grid.alpha": 0.6, "axes.spines.top": False, "axes.spines.right": False,
    "font.size": 11,
})

# ----------------------------------------------------------------------------
# Terminal colorido (24 bits; aceita "#rrggbb" ou código ANSI)
# ----------------------------------------------------------------------------
os.system("")   # habilita cores ANSI no terminal do Windows
LARGURA = 64


def cor(texto, codigo, negrito=False):
    """Colore texto. 'codigo' pode ser hex ("#ff8da1") ou ANSI ("92", "96;1")."""
    if isinstance(codigo, str) and codigo.startswith("#"):
        r, g, b = (int(codigo[i:i + 2], 16) for i in (1, 3, 5))
        codigo = f"38;2;{r};{g};{b}" + (";1" if negrito else "")
    return f"\033[{codigo}m{texto}\033[0m"


def _centro(texto, codigo, negrito=True):
    return cor(texto.center(LARGURA), codigo, negrito)


def titulo(texto):
    linha = "═" * LARGURA
    print(f"\n{cor(linha, CIANO)}\n{_centro(texto, CIANO)}\n{cor(linha, CIANO)}")


def banner(mensagem, codigo):
    barra = "█" * LARGURA
    print(f"\n{cor(barra, codigo)}\n{_centro(mensagem, codigo)}\n{cor(barra, codigo)}\n")


def sucesso():
    banner("✔  SUCESSO", VERDE)


def falha():
    banner("✘  FALHA DE TRANSMISSÃO", VERMELHO)


# ----------------------------------------------------------------------------
# Teclado sem bloquear (Windows e Linux/Mac)
# ----------------------------------------------------------------------------
def ler_tecla():
    """Devolve uma tecla (minúscula) se houver alguma pressionada; senão None."""
    try:
        import msvcrt
        return msvcrt.getwch().lower() if msvcrt.kbhit() else None
    except ImportError:
        import select
        if select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1).lower()
        return None


@contextlib.contextmanager
def modo_teclado():
    """Linux/Mac: terminal em modo 'tecla imediata'. Windows: não precisa."""
    try:
        import termios
        import tty
        if not sys.stdin.isatty():
            yield
            return
        antigo = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        try:
            yield
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, antigo)
    except ImportError:
        yield


# ----------------------------------------------------------------------------
# Osciloscópio em texto
# ----------------------------------------------------------------------------
_BLOCOS = " ▁▂▃▄▅▆▇█"


def osciloscopio(amostras, largura=LARGURA, threshold=0.75):
    """Sinal em uma linha de blocos; picos acima do limiar ficam rosa."""
    a = np.abs(np.asarray(amostras, dtype=float).ravel())
    if a.size == 0:
        return cor("▁" * largura, CINZA)
    saida = ""
    for p in np.array_split(a, largura):
        v = float(p.max()) if p.size else 0.0
        nivel = min(int(min(v, 1.0) * (len(_BLOCOS) - 1)), len(_BLOCOS) - 1)
        c = ROSA if v > threshold else (CIANO if v > threshold * 0.2 else CINZA)
        saida += cor(_BLOCOS[max(nivel, 1)], c)
    return saida


# ----------------------------------------------------------------------------
# Painel "Simulador de Camada Física"
# ----------------------------------------------------------------------------
class Painel:
    """Painel de terminal. modo: "RECEPTOR" ou "EMISSOR"."""

    def __init__(self, modo="RECEPTOR", threshold=0.75, limpar=True):
        self.modo, self.threshold, self.limpar = modo, threshold, limpar

    def _estado(self, batidas, tem_bits):
        if batidas == 1:
            return cor("BIT 0 — uma batida", COR_BIT[0], True)
        if batidas == 2:
            return cor("BIT 1 — duas batidas", COR_BIT[1], True)
        if batidas > 2:
            return cor(f"RUÍDO — {batidas} batidas", VERMELHO, True)
        if self.modo == "EMISSOR":
            return cor("Transmitindo..." if tem_bits else "Preparando...", CINZA)
        return cor("Recebendo..." if tem_bits else "Aguardando sinal...", CINZA)

    def _bits_txt(self, bits):
        if not bits:
            return cor("—", CINZA)
        partes = []
        for i, b in enumerate(bits):
            if i == 8:                         # 9º bit = paridade
                partes.append(cor("│", CINZA))
                partes.append(cor(str(b) if b in (0, 1) else "?", COR_PARIDADE, True))
            else:
                partes.append(cor(str(b) if b in (0, 1) else "?", COR_BIT.get(b, VERMELHO), True))
        return " ".join(partes)

    def _marcas(self, batidas):
        return "  ".join(cor("●", AMARELO, True) for _ in range(batidas)) or cor("○", CINZA)

    def desenhar(self, batidas=0, bits=None, onda=None, mensagem=""):
        """Monta o quadro em memória e escreve de uma vez (não pisca)."""
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self._corpo(batidas, bits or [], onda, mensagem)
        texto = buf.getvalue()
        if self.limpar:
            texto = "\033[H" + texto.replace("\n", "\033[K\n") + "\033[J"
        print(texto, end="", flush=True)

    def _corpo(self, batidas, bits, onda, mensagem):
        linha = cor("─" * LARGURA, "#334155")
        rotulo = "Bits enviados:" if self.modo == "EMISSOR" else "Bits recebidos:"
        print(_centro("SIMULADOR DE CAMADA FÍSICA", ROSA))
        print(_centro(f"Método 1 (batidas) — {self.modo}", CINZA, False))
        print(linha)
        print(cor(" OSCILOSCÓPIO — CANAL ACÚSTICO", CIANO, True)
              + cor(f"   limiar {self.threshold:.2f}", CINZA))
        print(" " + osciloscopio(onda if onda is not None else [], LARGURA - 2, self.threshold))
        print(linha)
        print(f" {cor('Estado:', TEXTO, True)} {self._estado(batidas, bool(bits))}")
        print(f" {cor('Batidas no símbolo atual:', TEXTO, True)} {self._marcas(batidas)}")
        print(f" {cor(rotulo, TEXTO, True)} {self._bits_txt(bits)}")
        print(linha)
        print(cor(" CODIFICAÇÃO", CIANO, True))
        print(f"   1 batida  {cor('→', CINZA)} {cor('0', COR_BIT[0], True)}"
              f"        2 batidas {cor('→', CINZA)} {cor('1', COR_BIT[1], True)}")
        print(linha)
        if self.modo == "RECEPTOR":
            print(cor(" [q] Sair    [r] Reiniciar    [s] Salvar", CINZA))
        if mensagem:
            print("\n " + mensagem)

    def resultado(self, dados, paridade, ok, motivo=""):
        """Quadro final (8 dados + paridade) com SUCESSO / FALHA DE TRANSMISSÃO."""
        self.desenhar(0, list(dados) + [paridade])
        print(f"\n {cor('Dados (8 bits):', TEXTO, True)} {self._bits_txt(list(dados))}   "
              f"{cor('Paridade recebida:', TEXTO, True)} "
              f"{cor(str(paridade) if paridade in (0, 1) else '?', COR_PARIDADE, True)}")
        if motivo:
            print(" " + cor(motivo, VERMELHO if not ok else CINZA))
        sucesso() if ok else falha()

    def reproduzir(self, bits, atraso=0.5):
        """Só para pré-visualização: anima bits chegando."""
        acumulado = []
        for b in bits:
            for k in range(1, (2 if b == 1 else 1) + 1):
                self.desenhar(k, acumulado)
                time.sleep(atraso / 2)
            acumulado.append(b)
            self.desenhar(0, acumulado)
            time.sleep(atraso / 2)


if __name__ == "__main__":
    p = Painel()
    msg = [0, 1, 0, 1, 0, 1, 1, 0]
    p.reproduzir(msg)
    p.resultado(msg, 0, True)
    time.sleep(1.5)
    p.resultado(msg, 1, False, "Paridade esperada 0, recebida 1")