import pytest
from src.core.validator import (
    numeros_validos, contar_pares, contar_impares,
    contar_primos, soma, analisar_criterios,
)


def test_numeros_validos_ok():
    assert numeros_validos(list(range(1, 16))) is True


def test_numeros_validos_menos_de_15():
    assert numeros_validos([1, 2, 3]) is False


def test_numeros_validos_duplicados():
    nums = [1]*15
    assert numeros_validos(nums) is False


def test_numeros_validos_fora_range():
    nums = list(range(1, 15)) + [30]
    assert numeros_validos(nums) is False


def test_contar_pares():
    assert contar_pares([2, 4, 6, 8, 10, 12, 14, 1, 3, 5, 7, 9, 11, 13, 15]) == 7


def test_contar_impares():
    assert contar_impares([1, 3, 5, 7, 9, 11, 13, 15, 2, 4, 6, 8, 10, 12, 14]) == 8


def test_contar_primos():
    nums = [2, 3, 5, 7, 11, 13, 1, 4, 6, 8, 9, 10, 12, 14, 15]
    assert contar_primos(nums) == 6


def test_soma():
    assert soma(list(range(1, 16))) == 120


def test_analisar_criterios_invalido():
    r = analisar_criterios([1, 2, 3])
    assert r["valido"] is False
    assert "erro" in r


def test_analisar_criterios_valido():
    nums = [2, 4, 6, 7, 8, 10, 12, 13, 14, 16, 18, 19, 20, 22, 23]
    r = analisar_criterios(nums)
    assert all(k in r for k in ["valido", "soma", "pares", "impares", "primos"])
