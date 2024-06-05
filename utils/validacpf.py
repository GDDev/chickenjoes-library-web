import re

def valida_cpf(cpf):
    cpf = str(cpf)
    cpf = re.sub(r'[^0-9]', '', cpf)

    if not cpf or len(cpf) != 11: return False
    
    novo_cpf = cpf[:-2]
    reverso = 10
    total = 0

    for i in range(19):
        if i > 8:
            i -= 9

        total += int(novo_cpf[i]) * reverso

        reverso -= 1
        if reverso < 2:
            reverso = 11
            d = 11 - (total % 11)

            if d > 9:
                d = 0
            total = 0
            novo_cpf += str(d)

    sequencia = novo_cpf == str(novo_cpf[0]) * len(cpf)

    return True if cpf == novo_cpf and not sequencia else False 
