import pytest
from src.core.generator import Gerador9_6
from src.core.validator import numeros_validos


ULTIMO = [1, 2, 5, 7, 8, 9, 11, 13, 14, 17, 19, 20, 22, 24, 25]


def test_gerar_jogo():
    g = Gerador9_6()
    r = g.gerar(ULTIMO)
    assert "erro" not in r
    assert numeros_validos(r["jogo"])
    assert r["analise"]["valido"] is True
    assert len(r["repete_do_ultimo"]) == 9
    assert len(r["novos"]) == 6


def test_gerar_forcado():
    g = Gerador9_6()
    r = g.gerar(ULTIMO, forcado=True)
    assert "erro" not in r
    assert numeros_validos(r["jogo"])
    assert r["analise"]["valido"] is True


def test_gerar_entrada_invalida():
    g = Gerador9_6()
    r = g.gerar([1, 2, 3])
    assert "erro" in r


def test_gerar_multiplos():
    g = Gerador9_6()
    rs = g.gerar_multiplos(ULTIMO, quantidade=3)
    assert len(rs) == 3
    for r in rs:
        assert "erro" not in r
        assert r["analise"]["valido"] is True


def test_gerar_com_pesos():
    g = Gerador9_6(pesos={"soma": 2.0, "par_impar": 0.5, "primos": 3.0})
    r = g.gerar(ULTIMO)
    assert "erro" not in r
    assert r["analise"]["valido"] is True
