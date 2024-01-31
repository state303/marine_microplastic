import os
import urllib.parse
import sqlalchemy.engine
from dotenv import load_dotenv
from sqlalchemy import create_engine as sqla_create_engine

__USERNAME = "DB_USER"
__PASSWORD = "DB_PASS"
__HOSTNAME = "DB_HOST"
__PORT = "DB_PORT"
__DATABASE = "DB_NAME"
__POOL_SIZE = "DB_POOL_SIZE"
__POOL_RECYCLE = "DB_POOL_RECYCLE"
__ECHO = "DB_ECHO"


# DSN for sqlalchemy.create_engine()
# dialect[+driver]://user:password@host:port/dbname[?key=value..]

def create_engine() -> sqlalchemy.engine.Engine:
    load_dotenv()
    host = os.getenv(__HOSTNAME)
    port = os.getenv(__PORT)
    username = read_and_encode_env(__USERNAME)
    password = read_and_encode_env(__PASSWORD)
    dbname = read_and_encode_env(__DATABASE)
    pool_recycle = os.getenv(__POOL_RECYCLE)
    echo = os.getenv(__ECHO)
    pool_size = os.getenv(__POOL_SIZE)

    if pool_recycle is None:
        pool_recycle = 3600
    else:
        pool_recycle = int(pool_recycle)

    if echo is not None and echo.lower() == "true":
        echo = True
    else:
        echo = False

    if pool_size is None:
        pool_size = 5
    else:
        pool_size = int(pool_size)

    if port is None:
        port = "5432"

    dsn = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(username, password, host, port, dbname)
    return sqla_create_engine(
        url=dsn,
        pool_recycle=pool_recycle,
        echo=echo,
        pool_size=pool_size
    )


def read_and_encode_env(key: str) -> str:
    v = os.getenv(key)
    if v:
        return urllib.parse.quote_plus(v)
    else:
        return ""
