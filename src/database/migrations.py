from .connection import Database


MIGRATIONS = [
    """
    CREATE TABLE IF NOT EXISTS concursos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        concurso_numero INTEGER UNIQUE NOT NULL,
        data TEXT NOT NULL,
        numeros TEXT NOT NULL,
        soma INTEGER,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS jogos_gerados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        numeros TEXT NOT NULL,
        repete_do_ultimo TEXT,
        novos TEXT,
        soma INTEGER,
        pares INTEGER,
        impares INTEGER,
        primos INTEGER,
        peso_soma REAL DEFAULT 1.0,
        peso_par_impar REAL DEFAULT 1.0,
        peso_primos REAL DEFAULT 1.0,
        concurso_base_id INTEGER REFERENCES concursos(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS auditoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jogo_id INTEGER NOT NULL REFERENCES jogos_gerados(id),
        concurso_id INTEGER REFERENCES concursos(id),
        resultado_oficial TEXT NOT NULL,
        acertos INTEGER NOT NULL,
        classificacao TEXT,
        premiado INTEGER DEFAULT 0,
        data_auditoria TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_jogos_data ON jogos_gerados(data_criacao)
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_auditoria_acertos ON auditoria(acertos)
    """,
]


def rodar_migracoes():
    db = Database()
    for sql in MIGRATIONS:
        db.executar(sql)
    return True
