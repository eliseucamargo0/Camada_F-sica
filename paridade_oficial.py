def calcular_paridade(bits):
    # Conta quantos bits 1 existem nos 8 bits de dados.
    quantidade = sum(bits)

    # A paridade garante que o total de bits 1 seja par.
    if quantidade % 2 == 0:
        paridade = 0
    else:
        paridade = 1

    return paridade


def verificar_paridade(bits, paridade_recebida):
    # Calcula qual deveria ser o bit de paridade.
    paridade_esperada = calcular_paridade(bits)

    # Compara a paridade esperada com a recebida.
    if paridade_esperada == paridade_recebida:
        return True
    else:
        return False


# Simulação de uma mensagem com 8 bits.
bits = [1, 0, 1, 1, 0, 0, 1, 0]

# Calcula o 9º bit.
paridade = calcular_paridade(bits)

print("Bits recebidos:", bits)
print("Bit de paridade:", paridade)

# Simula que o receptor recebeu corretamente o mesmo bit de paridade.
paridade_recebida = paridade

# Verifica se a transmissão está correta.
if verificar_paridade(bits, paridade_recebida):
    print("SUCESSO")
else:
    print("FALHA DE TRANSMISSÃO")