# Camada Física usando Som - Redes de Computadores

import glob
import importlib.util
import os
import sys
import threading

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

# ----------------------------------------------------------------------------
# Carrega o teste_método_um.py (nome com acento/espaço: procura pelo padrão)
# ----------------------------------------------------------------------------
def _carregar_modulo():
    achados = sorted(glob.glob(os.path.join(AQUI, "metodo_um.py")))
    if not achados:
        py = sorted(f for f in os.listdir(AQUI) if f.lower().endswith(".py"))
        sys.exit("Não encontrei o arquivo 'metodo_um.py' nesta pasta.\n"
                 f"Arquivos .py aqui: {', '.join(py)}")
    spec = importlib.util.spec_from_file_location("metodo_um", achados[0])
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

mod = _carregar_modulo()
from estetica_oficial import (BG, PAINEL, TEXTO, CINZA, ROSA, VERDE, VERMELHO,  # noqa: E402
                           AMARELO, ROXO, CIANO, COR_BIT, titulo)

FS = mod.FS
ATUAL = None   # receptor em uso (preenchido pela subclasse abaixo)


# ----------------------------------------------------------------------------
# Receptor que também guarda o áudio (para o gráfico). A lógica é a do original.
# ----------------------------------------------------------------------------
class ReceptorGrafico(mod.Receptor):
    def __init__(self, *args, **kwargs):
        global ATUAL
        super().__init__(*args, **kwargs)
        ATUAL = self

    def reiniciar(self, mensagem=""):
        super().reiniciar(mensagem)
        self.gravado = []

    def processar_bloco(self, x):
        if self.resultado is None:                 # após o 9º bit, para de gravar
            self.gravado.append(np.asarray(x, dtype=float).ravel().copy())
        super().processar_bloco(x)
        ocioso = not self.bits and not self.batidas and self.rajada_inicio is None
        maximo = int(3 * FS / 1024) + 1            # aguardando sinal: guarda só ~3 s
        if ocioso and len(self.gravado) > maximo:
            del self.gravado[:-maximo]


mod.Receptor = ReceptorGrafico    # receber() passa a usar a subclasse


# ----------------------------------------------------------------------------
# Decodificação só para ANOTAR o gráfico (mesmas constantes do original)
# ----------------------------------------------------------------------------
PASSO = 50   # amostras por ponto do envelope (acelera o desenho)


def _simbolos(env, thr):
    """Devolve [(t_inicio, t_fim, nº_batidas)] a partir do envelope."""
    idx = np.nonzero(env > thr)[0]
    if idx.size == 0:
        return []
    q = max(int(mod.T_QUEBRA * FS / PASSO), 1)
    grupos = np.split(idx, np.nonzero(np.diff(idx) > q)[0] + 1)
    batidas = []
    for g in grupos:
        if (g[-1] - g[0]) * PASSO / FS <= mod.T_MAX_BATIDA:     # descarta ruído longo
            batidas.append((g[0], g[-1]))
    simbolos, atual = [], []
    for b in batidas:
        if atual and (b[0] - atual[-1][1]) * PASSO / FS > mod.T_FIM_SIMBOLO:
            simbolos.append(atual)
            atual = []
        atual.append(b)
    if atual:
        simbolos.append(atual)
    return [(s[0][0] * PASSO / FS, s[-1][1] * PASSO / FS, len(s)) for s in simbolos]


# ----------------------------------------------------------------------------
# Janela com os gráficos
# ----------------------------------------------------------------------------
def _criar_figura(thread):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7))
    fig.canvas.manager.set_window_title("Método 1 — Gráficos do receptor")
    fig.tight_layout(pad=3)
    linha, = ax1.plot(np.zeros(FS), color=ROSA, lw=1)
    h1 = ax1.axhline(0, color=AMARELO, ls="--", lw=1)
    h2 = ax1.axhline(0, color=AMARELO, ls="--", lw=1)
    ax1.set_ylim(-1, 1)
    ax1.set_xlim(0, FS)
    ax1.set_xticks([0, FS / 2, FS])
    ax1.set_xticklabels(["-1 s", "-0,5 s", "agora"])
    ax1.set_ylabel("Amplitude")
    ax1.set_title("Microfone ao vivo", color=TEXTO)
    estado = {"quadro": 0}

    def desenhar_baixo(rx, thr):
        blocos = list(rx.gravado)
        ax2.clear()
        ax2.set_ylim(0, 1.25)
        ax2.set_xlabel("Tempo (s)")
        ax2.set_ylabel("|sinal|")
        if not blocos:
            ax2.set_title("Aguardando a primeira batida...", color=CINZA)
            return
        x = np.concatenate(blocos)
        m = len(x) // PASSO
        if m < 2:
            return
        env = np.abs(x[:m * PASSO]).reshape(m, PASSO).max(axis=1)
        t = np.arange(m) * PASSO / FS
        ax2.plot(t, env, color=ROSA, lw=1)
        ax2.axhline(thr, color=AMARELO, ls="--", lw=1)
        ax2.fill_between(t, 0, 1, where=env > thr, color=ROSA, alpha=0.35, step="mid")
        syms = _simbolos(env, thr)
        for k, (ini, fim, nb) in enumerate(syms):
            bit = {1: 0, 2: 1}.get(nb)
            txt = str(bit) if bit is not None else "?"
            c = COR_BIT.get(bit, VERMELHO)
            if k == mod.BITS_DADOS:
                c = AMARELO                        # 9º bit = paridade
            ax2.text((ini + fim) / 2, 1.08, txt, color=c, ha="center",
                     fontsize=15, fontweight="bold")
        titulo_txt = f"Transmissão: {len(syms)}/{mod.BITS_QUADRO} símbolos"
        cor_t = TEXTO
        if rx.resultado is not None:
            ok = rx.resultado[2]
            titulo_txt += "  —  SUCESSO" if ok else "  —  FALHA DE TRANSMISSÃO"
            cor_t = VERDE if ok else VERMELHO
        ax2.set_title(titulo_txt, color=cor_t)

    def atualizar(_):
        estado["quadro"] += 1
        if not thread.is_alive():
            plt.close(fig)
            return linha,
        rx = ATUAL
        if rx is None:
            ax1.set_title("Calibrando... siga as instruções no terminal", color=AMARELO)
            return linha,
        ax1.set_title("Microfone ao vivo", color=TEXTO)
        thr = rx.threshold
        with rx.lock:
            onda = rx.onda.copy()
        linha.set_ydata(onda)
        h1.set_ydata([thr, thr])
        h2.set_ydata([-thr, -thr])
        if estado["quadro"] % 4 == 0:
            desenhar_baixo(rx, thr)
        return linha,

    fig._ani = FuncAnimation(fig, atualizar, interval=60, blit=False,
                             cache_frame_data=False)
    return fig


def receptor_com_graficos():
    global ATUAL
    ATUAL = None
    t = threading.Thread(target=mod.receber, daemon=True)
    t.start()
    _criar_figura(t)
    plt.show()                      # fecha sozinho quando o receptor termina ([q])
    if t.is_alive():
        print("\nJanela fechada. Pressione [q] no terminal para sair do receptor.")
        t.join()


# ----------------------------------------------------------------------------
def main():
    while True:
        titulo("MÉTODO 1 — BATIDAS (COM GRÁFICOS)")
        print("  [1] Emissor  (toca as batidas no alto-falante)")
        print("  [2] Receptor (painel no terminal + gráficos)")
        print("  [q] Sair")
        op = input("\n > ").strip().lower()
        if op == "1":
            mod.transmitir()
        elif op == "2":
            receptor_com_graficos()
        elif op == "q":
            return


if __name__ == "__main__":
    main()