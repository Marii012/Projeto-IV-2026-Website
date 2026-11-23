"""Ligação ao PostgreSQL (único sítio do projeto que fala com a base de dados)."""
import threading
from contextlib import contextmanager

from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool

from app.config import DB_CONFIG

_pool = None
_lock = threading.Lock()


def _obter_pool() -> ThreadedConnectionPool:
    global _pool
    if _pool is None:
        with _lock:
            if _pool is None:
                _pool = ThreadedConnectionPool(1, 10, connect_timeout=5, **DB_CONFIG)
    return _pool


@contextmanager
def transacao():
    """Dá um cursor (linhas como dicionários) dentro de uma transação.

    Faz commit se tudo correr bem e rollback se houver qualquer exceção.
    Várias operações no mesmo bloco `with` ficam na mesma transação.
    """
    pool = _obter_pool()
    conn = pool.getconn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            yield cur
        conn.commit()
    except BaseException:
        conn.rollback()
        raise
    finally:
        pool.putconn(conn)


def fechar_pool():
    global _pool
    if _pool is not None:
        _pool.closeall()
        _pool = None
