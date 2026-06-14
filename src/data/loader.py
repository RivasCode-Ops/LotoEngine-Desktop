import csv
import json
import os

import pandas as pd


class CarregadorDados:
    COLUNAS_RESULTADO = [
        "Concurso", "Data", "Bola1", "Bola2", "Bola3", "Bola4", "Bola5",
        "Bola6", "Bola7", "Bola8", "Bola9", "Bola10", "Bola11", "Bola12",
        "Bola13", "Bola14", "Bola15",
    ]

    @staticmethod
    def carregar_csv(caminho):
        try:
            df = pd.read_csv(caminho, sep=None, engine="python")
            colunas_bola = [c for c in df.columns if "Bola" in c or "bola" in c or "bola" in c.lower()]
            if len(colunas_bola) >= 15:
                df[colunas_bola] = df[colunas_bola].apply(pd.to_numeric, errors="coerce")
                return df
            return None
        except Exception:
            return None

    @staticmethod
    def carregar_excel(caminho):
        try:
            df = pd.read_excel(caminho)
            colunas_bola = [c for c in df.columns if "bola" in c.lower()]
            if len(colunas_bola) >= 15:
                df[colunas_bola] = df[colunas_bola].apply(pd.to_numeric, errors="coerce")
                return df
            return None
        except Exception:
            return None

    @staticmethod
    def carregar_json(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    @staticmethod
    def extrair_ultimo_concurso(df):
        if df is None or df.empty:
            return None
        colunas_bola = sorted([c for c in df.columns if "bola" in c.lower()])
        if len(colunas_bola) < 15:
            colunas_bola = [f"Bola{i}" for i in range(1, 16) if f"Bola{i}" in df.columns]
        if len(colunas_bola) < 15:
            return None
        ultima = df.iloc[-1]
        return sorted([int(ultima[c]) for c in colunas_bola[:15]])

    @staticmethod
    def salvar_pesos(caminho, pesos):
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(pesos, f, indent=2, ensure_ascii=False)

    @staticmethod
    def carregar_pesos(caminho):
        if not os.path.exists(caminho):
            return {"soma": 1.0, "par_impar": 1.0, "primos": 1.0}
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def gerar_resultados_exemplo():
        import random
        random.seed(42)
        linhas = []
        for concurso in range(1, 101):
            nums = set()
            while len(nums) < 15:
                nums.add(random.randint(1, 25))
            linha = [concurso, f"2025-{(concurso % 12) + 1:02d}-{(concurso % 28) + 1:02d}"] + sorted(nums)
            linhas.append(linha)
        return pd.DataFrame(linhas, columns=CarregadorDados.COLUNAS_RESULTADO)
