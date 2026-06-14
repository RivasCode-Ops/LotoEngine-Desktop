import sqlite3
import os


_DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "lotoengine.db")


def _get_db_path():
    return os.environ.get("LOTOENGINE_DB_PATH", _DEFAULT_DB_PATH)


class Database:
    _instance = None
    _test_conn = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._conn = None
        return cls._instance

    @classmethod
    def _reset(cls):
        if cls._instance:
            cls._instance.fechar()
        cls._instance = None

    @property
    def conn(self):
        if self._conn is None:
            db_path = _get_db_path()
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            self._conn = sqlite3.connect(db_path)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA foreign_keys=ON")
        return self._conn

    def executar(self, sql, params=None):
        cur = self.conn.execute(sql, params or [])
        self.conn.commit()
        return cur

    def fetch_all(self, sql, params=None):
        return self.conn.execute(sql, params or []).fetchall()

    def fetch_one(self, sql, params=None):
        return self.conn.execute(sql, params or []).fetchone()

    def fechar(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.fechar()
