import psycopg
from psycopg_pool import ConnectionPool
from functools import lru_cache
from src.app.config import get_db_settings

settings = get_db_settings()

conninfo = f"""
    user = {settings.db_user} 
    password = {settings.db_password}
    host = {settings.db_host}
    port = {settings.db_port}
    dbname = {settings.db_name}
"""


@lru_cache
def get_pool():
    pool_conn = ConnectionPool(conninfo=conninfo)
    try:
        return pool_conn
    except Exception as e:
        return {"message": "error", "error": e}
