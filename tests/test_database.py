import pytest
import os
import uuid

from src.database.migrations import rodar_migracoes
from src.database.models import ConcursoDB, JogoDB, AuditoriaDB
from src.database.connection import Database


@pytest.fixture(autouse=True)
def setup_db():
    Database._reset()
    uid = uuid.uuid4().hex[:8]
    db_path = os.path.join(os.environ.get("TEMP", "/tmp"), f"loto_test_{uid}.db")
    os.environ["LOTOENGINE_DB_PATH"] = db_path
    rodar_migracoes()
    yield
    Database._reset()
    for f in [db_path, db_path + "-wal", db_path + "-shm"]:
        if os.path.exists(f):
            try:
                os.remove(f)
            except PermissionError:
                pass


def test_rodar_migracoes():
    assert rodar_migracoes() is True


def test_concurso_inserir():
    c = ConcursoDB()
    c.inserir(1, "2025-01-01", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    assert c.contar() == 1
    ultimo = c.ultimo()
    assert ultimo is not None
    assert ultimo["concurso_numero"] == 1
    assert len(ultimo["numeros"]) == 15


def test_concurso_duplicado():
    c = ConcursoDB()
    c.inserir(1, "2025-01-01", list(range(1, 16)))
    c.inserir(1, "2025-01-01", list(range(2, 17)))
    assert c.contar() == 1


def test_jogo_inserir():
    j = JogoDB()
    jogo_id = j.inserir(
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [10, 11, 12, 13, 14, 15],
        {"soma": 120, "pares": 7, "impares": 8, "primos": 6},
        {"soma": 1.0, "par_impar": 1.0, "primos": 1.0},
    )
    assert jogo_id > 0


def test_jogo_listar():
    j = JogoDB()
    j.inserir(
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [10, 11, 12, 13, 14, 15],
        {"soma": 120, "pares": 7, "impares": 8, "primos": 6},
        {"soma": 1.0, "par_impar": 1.0, "primos": 1.0},
    )
    jogos = j.listar_ultimos(10)
    assert len(jogos) == 1
    assert len(jogos[0]["numeros"]) == 15


def test_auditoria_inserir():
    j = JogoDB()
    jogo_id = j.inserir(
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [10, 11, 12, 13, 14, 15],
        {"soma": 120, "pares": 7, "impares": 8, "primos": 6},
        {"soma": 1.0, "par_impar": 1.0, "primos": 1.0},
    )
    a = AuditoriaDB()
    a.inserir(jogo_id, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
              11, "11 pontos", True)
    stats = a.estatisticas()
    assert stats["total"] == 1
    assert stats["total_premiados"] == 1
    assert stats["max_acertos"] == 11


def test_auditoria_estatisticas_vazias():
    a = AuditoriaDB()
    stats = a.estatisticas()
    assert stats["total"] == 0
