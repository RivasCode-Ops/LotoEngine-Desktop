import pytest
import pandas as pd
from src.data.loader import CarregadorDados


def test_extrair_ultimo_concurso():
    df = CarregadorDados.gerar_resultados_exemplo()
    ultimo = CarregadorDados.extrair_ultimo_concurso(df)
    assert ultimo is not None
    assert len(ultimo) == 15
    assert all(1 <= n <= 25 for n in ultimo)
    assert len(set(ultimo)) == 15


def test_gerar_resultados_exemplo():
    df = CarregadorDados.gerar_resultados_exemplo()
    assert len(df) == 100
    assert "Concurso" in df.columns
    assert "Bola1" in df.columns


def test_extrair_ultimo_df_vazio():
    df = pd.DataFrame()
    assert CarregadorDados.extrair_ultimo_concurso(df) is None


def test_pesos_save_load(tmp_path):
    pesos = {"soma": 2.5, "par_impar": 1.0, "primos": 0.5}
    path = tmp_path / "pesos.json"
    CarregadorDados.salvar_pesos(str(path), pesos)
    carregados = CarregadorDados.carregar_pesos(str(path))
    assert carregados == pesos


def test_pesos_default():
    import os, tempfile
    path = os.path.join(tempfile.gettempdir(), "nonexistent_pesos.json")
    if os.path.exists(path):
        os.remove(path)
    default = CarregadorDados.carregar_pesos(path)
    assert default == {"soma": 1.0, "par_impar": 1.0, "primos": 1.0}
