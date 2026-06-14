PRIMOS = {2, 3, 5, 7, 11, 13, 17, 19, 23}

TOTAL_NUMEROS = 25
QTD_NUMEROS = 15
SOMA_MIN = 180
SOMA_MAX = 220


def numeros_validos(nums):
    return (
        len(nums) == QTD_NUMEROS
        and all(1 <= n <= TOTAL_NUMEROS for n in nums)
        and len(set(nums)) == QTD_NUMEROS
    )


def contar_pares(nums):
    return sum(1 for n in nums if n % 2 == 0)


def contar_impares(nums):
    return QTD_NUMEROS - contar_pares(nums)


def contar_primos(nums):
    return sum(1 for n in nums if n in PRIMOS)


def soma(nums):
    return sum(nums)


def analisar_criterios(nums):
    if not numeros_validos(nums):
        return {"valido": False, "erro": "Numeros invalidos"}

    soma_val = soma(nums)
    pares = contar_pares(nums)
    impares = contar_impares(nums)
    primos = contar_primos(nums)

    return {
        "valido": (
            SOMA_MIN <= soma_val <= SOMA_MAX
            and ((impares == 8 and pares == 7) or (impares == 7 and pares == 8))
            and 5 <= primos <= 6
        ),
        "soma": soma_val,
        "pares": pares,
        "impares": impares,
        "primos": primos,
        "soma_ok": SOMA_MIN <= soma_val <= SOMA_MAX,
        "par_impar_ok": (impares == 8 and pares == 7) or (impares == 7 and pares == 8),
        "primos_ok": 5 <= primos <= 6,
    }
