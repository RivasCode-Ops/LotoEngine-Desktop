import random
from itertools import combinations

from .validator import (
    QTD_NUMEROS, TOTAL_NUMEROS,
    numeros_validos, analisar_criterios,
)


class Gerador9_6:
    REPETIR = 9
    NOVOS = 6

    def __init__(self, pesos=None):
        self.pesos = pesos or {
            "soma": 1.0,
            "par_impar": 1.0,
            "primos": 1.0,
        }

    def _separar(self, ultimo_concurso):
        todos = set(range(1, TOTAL_NUMEROS + 1))
        sorteados = set(ultimo_concurso)
        return sorteados, todos - sorteados

    def _calcular_pontuacao(self, nums):
        analise = analisar_criterios(nums)
        if not analise["valido"]:
            return 0.0
        pontos = 0.0
        if analise["soma_ok"]:
            pontos += self.pesos["soma"]
        if analise["par_impar_ok"]:
            pontos += self.pesos["par_impar"]
        if analise["primos_ok"]:
            pontos += self.pesos["primos"]
        return pontos

    def gerar(self, ultimo_concurso, forcado=False, max_tentativas=5000):
        if not numeros_validos(ultimo_concurso):
            return {"erro": "Ultimo concurso deve conter 15 numeros unicos entre 1 e 25"}

        repetir_candidatos, novos_candidatos = self._separar(ultimo_concurso)

        if len(repetir_candidatos) < self.REPETIR or len(novos_candidatos) < self.NOVOS:
            return {"erro": "Dados insuficientes para gerar jogo"}

        if forcado:
            melhor = None
            melhor_pontos = -1
            for rep in combinations(sorted(repetir_candidatos), self.REPETIR):
                for novos in combinations(sorted(novos_candidatos), self.NOVOS):
                    combinacao = sorted(list(rep) + list(novos))
                    pontos = self._calcular_pontuacao(combinacao)
                    if pontos > melhor_pontos:
                        melhor_pontos = pontos
                        melhor = combinacao
            if melhor is None:
                return {"erro": "Nenhuma combinacao viavel encontrada"}
            combinacao = melhor
        else:
            tentativas = 0
            while tentativas < max_tentativas:
                rep = set(random.sample(list(repetir_candidatos), self.REPETIR))
                novos = set(random.sample(list(novos_candidatos), self.NOVOS))
                combinacao = sorted(rep | novos)
                if numeros_validos(combinacao) and analisar_criterios(combinacao)["valido"]:
                    break
                tentativas += 1
            else:
                return {"erro": f"Nao foi possivel gerar jogo em {max_tentativas} tentativas"}

        return {
            "jogo": combinacao,
            "repete_do_ultimo": sorted(set(combinacao) & set(ultimo_concurso)),
            "novos": sorted(set(combinacao) - set(ultimo_concurso)),
            "analise": analisar_criterios(combinacao),
        }

    def gerar_multiplos(self, ultimo_concurso, quantidade=5, forcado=False):
        return [self.gerar(ultimo_concurso, forcado=forcado) for _ in range(quantidade)]
