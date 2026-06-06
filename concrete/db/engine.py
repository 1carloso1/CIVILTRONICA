"""
Único punto del código que "sabe" cómo se conecta a la base de datos.

Toda la abstracción del proveedor vive AQUÍ: la lógica de negocio y los
repositorios sólo piden una sesión, nunca conocen Supabase, ni el driver,
ni el host. Para migrar de Supabase a un PostgreSQL self-hosted basta con
cambiar la variable de entorno DATABASE_URL: ni una línea de este archivo
(ni de los demás) se modifica.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from contextlib import contextmanager

# ---------------------------------------------------------------------------
# Cadena de conexión: SIEMPRE desde el entorno. Formato SQLAlchemy:
#   postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DBNAME?sslmode=require
#
# El prefijo "postgresql+psycopg2" sólo le indica a SQLAlchemy qué driver
# usar; el resto es una URL estándar de Postgres. Por eso pasar de Supabase
# a un servidor propio es únicamente cambiar HOST/PORT/credenciales.
# ---------------------------------------------------------------------------
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "Falta la variable de entorno DATABASE_URL."
    )

# create_engine mantiene un pool interno de SQLAlchemy (reemplaza a
# mysql.connector.pooling). Parámetros pensados para una app de escritorio
# persistente conectada a una BD en la nube:
_engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # valida la conexión antes de usarla: imprescindible
                          # en la nube, que cierra conexiones ociosas.
    pool_size=5,          # conexiones persistentes (sobra para 1 escritorio).
    max_overflow=5,       # picos puntuales (p.ej. lecturas ad-hoc).
    pool_recycle=1800,    # recicla conexiones cada 30 min (evita timeouts).
    future=True,
)

# Fábrica de sesiones. expire_on_commit=False permite seguir leyendo los
# atributos de los objetos después del commit (útil para mapear a tus
# serializadores sin re-consultar).
SessionLocal = sessionmaker(bind=_engine, class_=Session, expire_on_commit=False)


def get_engine():
    """Devuelve el engine compartido (por si necesitas DDL o pandas.read_sql)."""
    return _engine


@contextmanager
def session_scope():
    """
    Provee una sesión transaccional con commit/rollback automáticos.

        with session_scope() as session:
            repo = RegistroRepository(session)
            ...

    Si el bloque termina bien -> commit; si lanza excepción -> rollback.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()