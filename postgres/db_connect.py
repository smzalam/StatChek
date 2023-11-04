import psycopg
from psycopg_pool import ConnectionPool
from db_config import get_settings

settings = get_settings()

conninfo_w_db = f"""
    user = {settings.db_user} 
    password = {settings.db_password}
    host = {settings.db_host}
    port = {settings.db_port}
    dbname = {settings.db_name}
"""

conninfo_wo_db = f"""
    user = {settings.db_user} 
    password = {settings.db_password}
    host = {settings.db_host}
    port = {settings.db_port}
"""

def get_conn(db: bool = False, auto: bool = False):
    if auto and db:
        return psycopg.connect(conninfo=conninfo_w_db, autocommit=True) 
    elif auto:
        return psycopg.connect(conninfo=conninfo_wo_db, autocommit=True)
    else:
        return psycopg.connect(conninfo=conninfo_w_db)