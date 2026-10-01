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
# Terminal colorido
# ----------------------------------------------------------------------------
os.system("")   # habilita cores ANSI no terminal do Windows


def cor(texto, codigo):
    """Colore texto no terminal. Ex.: 92=verde, 91=vermelho, 93=amarelo, 96=ciano (;1 = negrito)."""
    return f"\033[{codigo}m{texto}\033[0m"


def titulo(texto):
    """Imprime um título destacado no terminal."""
    linha = "═" * 60
    print(f"\n{cor(linha, '96')}\n{cor(texto.center(60), '96;1')}\n{cor(linha, '96')}")


def banner(mensagem, codigo):
    """Imprime uma faixa grande colorida (usada para SUCESSO / FALHA)."""
    barra = "█" * 60
    print(f"\n{cor(barra, codigo)}\n{cor(mensagem.center(60), codigo + ';1')}\n{cor(barra, codigo)}\n")


def sucesso():
    """Faixa verde padrão de SUCESSO."""
    banner("✔  SUCESSO", "92")


def falha():
    """Faixa vermelha padrão de FALHA DE TRANSMISSÃO."""
    banner("✘  FALHA DE TRANSMISSÃO", "91")
