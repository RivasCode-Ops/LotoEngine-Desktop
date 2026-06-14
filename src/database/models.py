import json
from datetime import datetime

from .connection import Database


class ConcursoDB:
    def __init__(self):
        self.db = Database()

    def inserir(self, concurso_numero, data, numeros):
        soma = sum(numeros)
        self.db.executar(
            "INSERT OR IGNORE INTO concursos (concurso_numero, data, numeros, soma) VALUES (?, ?, ?, ?)",
            [concurso_numero, data, json.dumps(numeros), soma],
        )

    def listar_todos(self):
        rows = self.db.fetch_all("SELECT * FROM concursos ORDER BY concurso_numero DESC")
        return [dict(r) for r in rows]

    def ultimo(self):
        row = self.db.fetch_one("SELECT * FROM concursos ORDER BY concurso_numero DESC LIMIT 1")
        if row:
            r = dict(row)
            r["numeros"] = json.loads(r["numeros"])
            return r
        return None

    def contar(self):
        row = self.db.fetch_one("SELECT COUNT(*) AS total FROM concursos")
        return row["total"] if row else 0


class JogoDB:
    def __init__(self):
        self.db = Database()

    def inserir(self, numeros, repete_do_ultimo, novos, analise, pesos, concurso_base_id=None):
        self.db.executar(
            """INSERT INTO jogos_gerados
               (numeros, repete_do_ultimo, novos, soma, pares, impares, primos,
                peso_soma, peso_par_impar, peso_primos, concurso_base_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                json.dumps(numeros),
                json.dumps(repete_do_ultimo),
                json.dumps(novos),
                analise.get("soma"),
                analise.get("pares"),
                analise.get("impares"),
                analise.get("primos"),
                pesos.get("soma", 1.0),
                pesos.get("par_impar", 1.0),
                pesos.get("primos", 1.0),
                concurso_base_id,
            ],
        )
        return self.db.fetch_one("SELECT last_insert_rowid() AS id")["id"]

    def listar_ultimos(self, limite=50):
        rows = self.db.fetch_all(
            "SELECT * FROM jogos_gerados ORDER BY data_criacao DESC LIMIT ?",
            [limite],
        )
        resultados = []
        for r in rows:
            d = dict(r)
            d["numeros"] = json.loads(d["numeros"])
            d["repete_do_ultimo"] = json.loads(d["repete_do_ultimo"]) if d["repete_do_ultimo"] else []
            d["novos"] = json.loads(d["novos"]) if d["novos"] else []
            resultados.append(d)
        return resultados


class AuditoriaDB:
    def __init__(self):
        self.db = Database()

    def inserir(self, jogo_id, resultado_oficial, acertos, classificacao, premiado, concurso_id=None):
        self.db.executar(
            """INSERT INTO auditoria (jogo_id, concurso_id, resultado_oficial, acertos, classificacao, premiado)
               VALUES (?, ?, ?, ?, ?, ?)""",
            [jogo_id, concurso_id, json.dumps(resultado_oficial), acertos, classificacao, 1 if premiado else 0],
        )

    def estatisticas(self):
        row = self.db.fetch_one(
            """SELECT COUNT(*) AS total,
                      SUM(premiado) AS total_premiados,
                      ROUND(AVG(acertos), 2) AS media_acertos,
                      MAX(acertos) AS max_acertos
               FROM auditoria"""
        )
        return dict(row) if row else {"total": 0, "total_premiados": 0, "media_acertos": 0, "max_acertos": 0}

    def ultimas_auditorias(self, limite=20):
        rows = self.db.fetch_all(
            """SELECT a.*, j.numeros AS jogo_numeros
               FROM auditoria a
               LEFT JOIN jogos_gerados j ON a.jogo_id = j.id
               ORDER BY a.data_auditoria DESC LIMIT ?""",
            [limite],
        )
        return [dict(r) for r in rows]
