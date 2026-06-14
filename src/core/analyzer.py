import pandas as pd
import numpy as np

from .validator import PRIMOS, TOTAL_NUMEROS


class Analisador:
    def __init__(self, df_historico=None):
        self.df = df_historico if df_historico is not None else pd.DataFrame()

    def carregar_historico(self, df):
        self.df = df.copy()

    def frequencia_numeros(self):
        if self.df.empty:
            return pd.Series(dtype=int)
        numeros = []
        for _, row in self.df.iterrows():
            nums = row.filter(like="Bola").values.astype(int)
            numeros.extend(nums)
        serie = pd.Series(numeros)
        return serie.value_counts().sort_index()

    def numeros_mais_frequentes(self, top_n=10):
        freq = self.frequencia_numeros()
        return freq.head(top_n)

    def numeros_menos_frequentes(self, bottom_n=10):
        freq = self.frequencia_numeros()
        return freq.tail(bottom_n)

    def atraso_numeros(self):
        if self.df.empty:
            return pd.Series(dtype=int)
        ultimo_concurso = self.df.iloc[-1]["Concurso"]
        atrasos = {}
        for n in range(1, TOTAL_NUMEROS + 1):
            linhas = self.df[self.df.filter(like="Bola").eq(n).any(axis=1)]
            if linhas.empty:
                atrasos[n] = ultimo_concurso
            else:
                atrasos[n] = ultimo_concurso - linhas.iloc[-1]["Concurso"]
        return pd.Series(atrasos, name="atraso")

    def estatisticas_por_concurso(self, nums):
        return {
            "soma": int(np.sum(nums)),
            "pares": int(np.sum([1 for n in nums if n % 2 == 0])),
            "impares": int(np.sum([1 for n in nums if n % 2 != 0])),
            "primos": int(np.sum([1 for n in nums if n in PRIMOS])),
        }

    def resumo_historico(self):
        if self.df.empty:
            return {"erro": "Nenhum historico carregado"}
        freq = self.frequencia_numeros()
        return {
            "total_concursos": len(self.df),
            "media_soma": float(self.df["Soma"].mean()) if "Soma" in self.df.columns else 0,
            "numero_mais_frequente": int(freq.index[0]) if not freq.empty else None,
            "numero_menos_frequente": int(freq.index[-1]) if not freq.empty else None,
            "frequencia_max": int(freq.iloc[0]) if not freq.empty else 0,
            "frequencia_min": int(freq.iloc[-1]) if not freq.empty else 0,
        }
