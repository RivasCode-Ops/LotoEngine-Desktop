import pytest
from src.core.auditor import Auditor


def test_comparar_11_acertos():
    jogo = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    oficial = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 16, 17, 18, 19]
    r = Auditor.comparar(jogo, oficial)
    assert r["quantidade"] == 11
    assert r["premiado"] is True
    assert r["classificacao"] == "11 pontos"


def test_comparar_15_acertos():
    jogo = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    r = Auditor.comparar(jogo, jogo)
    assert r["quantidade"] == 15
    assert r["premiado"] is True
    assert r["classificacao"] == "15 pontos"


def test_comparar_10_acertos():
    jogo = list(range(1, 16))
    oficial = list(range(6, 21))
    r = Auditor.comparar(jogo, oficial)
    assert r["quantidade"] == 10
    assert r["premiado"] is False


def test_auditar_lote():
    jogos = [list(range(1, 16)), list(range(3, 18)), list(range(5, 20))]
    oficial = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    r = Auditor.auditar_lote(jogos, oficial)
    assert r["total_jogos"] == 3
    assert r["total_premiados"] >= 0
    assert 0 <= r["aproveitamento"] <= 100
