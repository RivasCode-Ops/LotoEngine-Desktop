class Auditor:
    ACERTOS = {11: "11 pontos", 12: "12 pontos", 13: "13 pontos", 14: "14 pontos", 15: "15 pontos"}

    @staticmethod
    def comparar(jogo_gerado, resultado_oficial):
        acertos = sorted(set(jogo_gerado) & set(resultado_oficial))
        qtd = len(acertos)

        return {
            "jogo": sorted(jogo_gerado),
            "oficial": sorted(resultado_oficial),
            "acertos": acertos,
            "quantidade": qtd,
            "classificacao": Auditor.ACERTOS.get(qtd, "Abaixo de 11 pontos"),
            "premiado": qtd >= 11,
        }

    @staticmethod
    def auditar_lote(jogos, resultado_oficial):
        resultados = [Auditor.comparar(j, resultado_oficial) for j in jogos]
        qtd_premiados = sum(1 for r in resultados if r["premiado"])
        return {
            "resultados": resultados,
            "total_jogos": len(resultados),
            "total_premiados": qtd_premiados,
            "aproveitamento": round(qtd_premiados / len(resultados) * 100, 2) if resultados else 0,
        }
