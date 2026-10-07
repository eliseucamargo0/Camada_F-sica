# Camada Física usando Som - Redes de Computadores
import importlib
import importlib.util
import os
import runpy
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)


def _sem_acento(nome):
    return unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode().lower()


def localizar(nome_modulo):
    """Caminho do .py correspondente, ignorando acento/caixa/prefixo 'teste_'. None se não achar."""
    alvo = _sem_acento(nome_modulo) + ".py"
    for f in sorted(os.listdir(AQUI)):
        k = _sem_acento(f)
        if k == alvo or k == "teste_" + alvo or k == "teste" + alvo:
            return os.path.join(AQUI, f)
    return None


def garantir(nome_modulo):
    """Se 'import nome_modulo' não funcionaria (nome de arquivo diferente), carrega pelo
    caminho e registra com o nome esperado. Devolve o módulo."""
    if nome_modulo in sys.modules:
        return sys.modules[nome_modulo]
    try:
        if importlib.util.find_spec(nome_modulo) is not None:
            return importlib.import_module(nome_modulo)
    except (ImportError, ValueError):
        pass
    caminho = localizar(nome_modulo)
    if caminho is None:
        py = sorted(f for f in os.listdir(AQUI) if f.lower().endswith(".py"))
        raise ImportError(f"não achei '{nome_modulo}.py' em {AQUI} (há: {', '.join(py)})")
    spec = importlib.util.spec_from_file_location(nome_modulo, caminho)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nome_modulo] = mod
    spec.loader.exec_module(mod)
    return mod


garantir("estetica_oficial")   # o hub usa o visual logo de cara

from estetica_oficial import titulo, cor, CIANO, CINZA, VERMELHO, AMARELO  # noqa: E402


def _rodar_modulo(nome):
    """Importa o módulo só quando escolhido (evita carregar sounddevice/matplotlib à toa)
    e chama a função main() dele."""
    garantir(nome).main()


def metodo_um():
    _rodar_modulo("metodo_um")


def metodo_um_graficos():
    _rodar_modulo("grafico_oficial")


def metodo_dois():
    _rodar_modulo("metodo_dois")


def demo_paridade():
    # paridade_oficial.py executa a demonstração ao ser carregado,
    # então usamos runpy para poder rodar quantas vezes quiser.
    runpy.run_path(os.path.join(AQUI, "paridade_oficial.py"), run_name="__main__")
    input(cor("\n Pressione Enter para voltar ao menu...", CINZA))


OPCOES = {
    "1": ("Método 1 — Batidas (terminal)", metodo_um),
    "2": ("Método 1 — Batidas com gráficos", metodo_um_graficos),
    "3": ("Método 2 — FSK (frequências)", metodo_dois),
    "4": ("Demonstração de paridade", demo_paridade),
}


def main():
    while True:
        titulo("CAMADA FÍSICA USANDO SOM — MENU PRINCIPAL")
        for k, (nome, _) in OPCOES.items():
            print(f"  [{k}] {nome}")
        print("  [q] Sair")
        op = input("\n > ").strip().lower()

        if op == "q":
            print(cor(" Encerrando.", CINZA))
            return
        if op not in OPCOES:
            print(cor(" Opção inválida.", VERMELHO))
            continue

        try:
            OPCOES[op][1]()
        except KeyboardInterrupt:
            print(cor("\n Interrompido. Voltando ao menu...", AMARELO))
        except ImportError as e:
            print(cor(f"\n Dependência ou arquivo ausente: {e}", VERMELHO))
            print(cor(" Verifique os arquivos na pasta e rode: "
                      "pip install numpy sounddevice matplotlib", CINZA))
        except Exception as e:  # um método com erro não derruba o hub
            print(cor(f"\n Erro em '{OPCOES[op][0]}': {e}", VERMELHO))


if __name__ == "__main__":
    main()
