from functools import lru_cache
import psycopg
from psycopg_pool import ConnectionPool
from config import get_db_settings

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
    return ConnectionPool(conninfo=conninfo)
