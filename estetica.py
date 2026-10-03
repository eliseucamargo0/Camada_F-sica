"""
Módulo de estética compartilhado (Método 1 e Método 2).

Importar este arquivo já aplica o tema escuro do matplotlib e habilita
cores no terminal. Também oferece as cores e funções de impressão.

"""

import os
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# Paleta de cores (para gráficos)
# ----------------------------------------------------------------------------
BG, PAINEL, TEXTO = "#0f172a", "#1e293b", "#e2e8f0"
CIANO, VERDE, VERMELHO, AMARELO, ROXO = "#22d3ee", "#4ade80", "#f87171", "#fbbf24", "#a78bfa"

# ----------------------------------------------------------------------------
# Tema escuro dos gráficos (aplicado automaticamente ao importar)
# ----------------------------------------------------------------------------
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": PAINEL, "axes.edgecolor": "#475569",
    "axes.labelcolor": TEXTO, "xtick.color": TEXTO, "ytick.color": TEXTO,
    "text.color": TEXTO, "axes.grid": True, "grid.color": "#334155",
    "grid.alpha": 0.6, "axes.spines.top": False, "axes.spines.right": False,
    "font.size": 11,
})

# ----------------------------------------------------------------------------
# Terminal colorido (cores reais 24 bits; aceita "#rrggbb" ou código ANSI)
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
    """Título destacado."""
    linha = "═" * LARGURA
    print(f"\n{cor(linha, CIANO)}\n{_centro(texto, CIANO)}\n{cor(linha, CIANO)}")


def banner(mensagem, codigo):
    """Faixa grande colorida (SUCESSO / FALHA)."""
    barra = "█" * LARGURA
    print(f"\n{cor(barra, codigo)}\n{_centro(mensagem, codigo)}\n{cor(barra, codigo)}\n")


def sucesso():
    banner("✔  SUCESSO", VERDE)


def falha():
    banner("✘  FALHA DE TRANSMISSÃO", VERMELHO)


# ----------------------------------------------------------------------------
# Osciloscópio em texto
# ----------------------------------------------------------------------------
_BLOCOS = " ▁▂▃▄▅▆▇█"


def osciloscopio(amostras, largura=LARGURA, threshold=0.75):
    """Desenha o sinal em uma linha de blocos; picos acima do threshold ficam rosa."""
    a = np.abs(np.asarray(amostras, dtype=float).ravel())
    if a.size == 0:
        return cor("▁" * largura, CINZA)
    pedacos = np.array_split(a, largura)
    saida = ""
    for p in pedacos:
        v = float(p.max()) if p.size else 0.0
        nivel = min(int(v * (len(_BLOCOS) - 1)), len(_BLOCOS) - 1)
        c = ROSA if v > threshold else (CIANO if v > 0.05 else CINZA)
        saida += cor(_BLOCOS[max(nivel, 1)], c)
    return saida


# ----------------------------------------------------------------------------
# Painel estilo "Simulador de Camada Física"
# ----------------------------------------------------------------------------
class Painel:
    """Painel de terminal: estado, batidas, bits recebidos, legenda e atalhos."""

    def __init__(self, limpar=True):
        self.limpar = limpar

    # -- partes do painel ----------------------------------------------------
    def _estado(self, batidas, tem_bits):
        if batidas == 1:
            return cor("BIT 0 — uma batida", COR_BIT[0], True)
        if batidas == 2:
            return cor("BIT 1 — duas batidas", COR_BIT[1], True)
        if batidas > 2:
            return cor(f"RUÍDO — {batidas} batidas", VERMELHO, True)
        return cor("Recebendo..." if tem_bits else "Aguardando sinal...", CINZA)

    def _bits_txt(self, bits):
        if not bits:
            return cor("—", CINZA)
        partes = []
        for i, b in enumerate(bits):
            if i == 8:                         # 9º bit = paridade
                partes.append(cor("│", CINZA))
                partes.append(cor(str(b), COR_PARIDADE, True))
            else:
                partes.append(cor(str(b) if b in (0, 1) else "?", COR_BIT.get(b, VERMELHO), True))
        return " ".join(partes)

    def _marcas(self, batidas):
        return "  ".join(cor("●", AMARELO, True) for _ in range(batidas)) or cor("○", CINZA)

    # -- desenho -------------------------------------------------------------
    def desenhar(self, batidas=0, bits=None, onda=None, mensagem=""):
        """Monta o quadro em memória e escreve de uma vez (evita piscar)."""
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self._corpo(batidas, bits, onda, mensagem)
        texto = buf.getvalue()
        if self.limpar:
            texto = "\033[H" + texto.replace("\n", "\033[K\n") + "\033[J"
        print(texto, end="", flush=True)

    def _corpo(self, batidas=0, bits=None, onda=None, mensagem=""):
        bits = bits or []
        linha = cor("─" * LARGURA, "#334155")
        print(_centro("SIMULADOR DE CAMADA FÍSICA", ROSA))
        print(_centro("Aula de Redes de Computadores — Método 1 (batidas)", CINZA, False))
        print(linha)
        print(cor(" OSCILOSCÓPIO — CANAL ACÚSTICO", CIANO, True))
        print(" " + osciloscopio(onda if onda is not None else [], LARGURA - 2))
        print(linha)
        print(f" {cor('Estado:', TEXTO, True)} {self._estado(batidas, bool(bits))}")
        print(f" {cor('Batidas no símbolo atual:', TEXTO, True)} {self._marcas(batidas)}")
        print(f" {cor('Bits recebidos:', TEXTO, True)} {self._bits_txt(bits)}")
        print(linha)
        print(cor(" CODIFICAÇÃO", CIANO, True))
        print(f"   1 batida  {cor('→', CINZA)} {cor('0', COR_BIT[0], True)}"
              f"        2 batidas {cor('→', CINZA)} {cor('1', COR_BIT[1], True)}")
        print(linha)
        print(cor(" [q] Sair    [r] Reiniciar    [s] Salvar", CINZA))
        if mensagem:
            print("\n " + mensagem)

    def reproduzir(self, bits, atraso=0.5):
        """Anima cada símbolo chegando (1 ou 2 batidas) e acumulando os bits."""
        acumulado = []
        for b in bits:
            n = 2 if b == 1 else 1
            for k in range(1, n + 1):          # batida por batida
                self.desenhar(k, acumulado)
                time.sleep(atraso / 2)
            acumulado.append(b)
            self.desenhar(0, acumulado)
            time.sleep(atraso / 2)
        return acumulado

    def resultado(self, dados, paridade, ok):
        """Quadro final de 9 bits + faixa de SUCESSO / FALHA."""
        self.desenhar(0, list(dados) + [paridade])
        print()
        print(f" {cor('Dados (8 bits):', TEXTO, True)} "
              f"{self._bits_txt(list(dados))}   "
              f"{cor('Paridade:', TEXTO, True)} {cor(str(paridade), COR_PARIDADE, True)}")
        sucesso() if ok else falha()

    def erro(self, texto):
        self.desenhar(0, [], mensagem=cor("⚠  " + texto, AMARELO, True))


# ----------------------------------------------------------------------------
# Receptor AO VIVO: lê o microfone e decodifica as batidas em tempo real
# (mesmos limiares do metodo_um.py: threshold 0.75, quebra 0.05 s, símbolo 20000 amostras)
# ----------------------------------------------------------------------------
def _tecla():
    """Lê uma tecla sem bloquear (Windows e Linux/Mac). Devolve None se não houver."""
    try:
        import msvcrt
        return msvcrt.getwch().lower() if msvcrt.kbhit() else None
    except ImportError:
        import select
        if select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1).lower()
        return None


@contextlib.contextmanager
def _modo_teclado():
    """No Linux/Mac coloca o terminal em modo 'tecla imediata'; no Windows não precisa."""
    try:
        import termios, tty
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


class ReceptorAoVivo:
    """Escuta o microfone; cada símbolo (1 batida = 0, 2 batidas = 1) aparece no painel.
    Quadro = 8 bits de dados + 1 bit de paridade par, validado ao receber o 9º bit."""

    def __init__(self, fs=44100, threshold=0.75, t_quebra=0.05, intervalo=20000):
        self.fs, self.threshold = fs, threshold
        self.t_quebra, self.intervalo = t_quebra, intervalo
        self.painel = Painel()
        self.lock = threading.Lock()
        self.reiniciar()

    def reiniciar(self, mensagem=""):
        with self.lock:
            self.onda = np.zeros(self.fs)      # janela de 1 s para o osciloscópio
            self.n = 0                         # contador global de amostras
            self.ultimo_hit = None             # última amostra acima do threshold
            self.batidas = 0                   # batidas do símbolo atual
            self.bits = []
            self.resultado = None              # (dados, paridade, ok) quando completa 9 bits
            self.mensagem = mensagem
            self._mostrado = False

    # -- detecção (roda a cada bloco de áudio) -------------------------------
    def processar_bloco(self, x):
        x = np.asarray(x, dtype=float).ravel()
        with self.lock:
            if self.resultado is not None:     # quadro completo: aguarda [r]
                return
            y = x[-self.fs:]
            self.onda = np.roll(self.onda, -len(y))
            self.onda[-len(y):] = y
            for g in np.nonzero(np.abs(x) > self.threshold)[0] + self.n:
                if self.ultimo_hit is not None and g - self.ultimo_hit > self.intervalo:
                    self._fechar_simbolo()
                if self.ultimo_hit is None or g - self.ultimo_hit > self.fs * self.t_quebra:
                    self.batidas += 1          # nova batida
                self.ultimo_hit = g
            self.n += len(x)
            if self.ultimo_hit is not None and self.n - self.ultimo_hit > self.intervalo:
                self._fechar_simbolo()         # silêncio longo: símbolo terminou

    def _fechar_simbolo(self):
        bit = {1: 0, 2: 1}.get(self.batidas, 3)   # 3 = símbolo inválido (ruído)
        self.bits.append(bit)
        self.batidas, self.ultimo_hit, self.mensagem = 0, None, ""
        if len(self.bits) == 9:
            dados, paridade = self.bits[:8], self.bits[8]
            ok = 3 not in self.bits and sum(dados) % 2 == paridade
            self.resultado = (dados, paridade, ok)

    # -- interface -----------------------------------------------------------
    def _salvar(self):
        with self.lock:
            bits = "".join(str(b) for b in self.bits)
        nome = datetime.now().strftime("transmissao_%Y%m%d_%H%M%S.txt")
        with open(nome, "w", encoding="utf-8") as f:
            f.write(bits + "\n")
        self.mensagem = cor(f"Salvo em {nome}", VERDE)

    def _render(self):
        with self.lock:
            batidas, bits, onda = self.batidas, list(self.bits), self.onda.copy()
            res, msg, mostrado = self.resultado, self.mensagem, self._mostrado
        if res is None:
            self.painel.desenhar(batidas, bits, onda, msg)
        elif not mostrado:
            dados, paridade, ok = res
            self.painel.resultado(dados, paridade, ok)
            if ok:
                c = int("".join(map(str, dados)), 2)
                if 32 <= c < 127:
                    print(f" {cor('Caractere recebido:', TEXTO, True)} {cor(chr(c), VERDE, True)}")
            print(cor(" [r] Reiniciar    [s] Salvar    [q] Sair", CINZA))
            self._mostrado = True

    def executar(self):
        import sounddevice as sd

        def callback(indata, frames, tempo, status):
            self.processar_bloco(indata[:, 0])

        print("\033[2J\033[?25l", end="")     # limpa a tela e esconde o cursor
        try:
            with _modo_teclado(), sd.InputStream(samplerate=self.fs, channels=1,
                                                 blocksize=1024, callback=callback):
                while True:
                    t = _tecla()
                    if t == "q":
                        break
                    if t == "r":
                        self.reiniciar(cor("Transmissão atual apagada.", AMARELO))
                        print("\033[2J", end="")
                    elif t == "s":
                        self._salvar()
                    self._render()
                    time.sleep(0.05)
        finally:
            print("\033[?25h")                # volta o cursor


# ----------------------------------------------------------------------------
# python estetica.py          -> receptor ao vivo (microfone)
# python estetica.py --demo   -> só pré-visualiza o visual (sem microfone)
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    if "--demo" in sys.argv:
        p = Painel()
        msg = [0, 1, 0, 1, 0, 1, 1, 0]
        p.reproduzir(msg)
        p.resultado(msg, paridade=0, ok=True)
        time.sleep(1.5)
        p.resultado(msg, paridade=1, ok=False)
    else:
        ReceptorAoVivo().executar()
