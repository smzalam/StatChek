import os
import sys
from functools import lru_cache
from pprint import pprint

import psycopg
from psycopg_pool import ConnectionPool

from plinkAPI.src.config import config

settings = config.get_db_settings()

conninfo = f"""
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
        return psycopg.connect(conninfo=conninfo, autocommit=True)
    elif auto:
        return psycopg.connect(conninfo=conninfo_wo_db, autocommit=True)
    else:
        return psycopg.connect(conninfo=conninfo)


@lru_cache
def get_pool():
    pool_conn = ConnectionPool(conninfo=conninfo)
    try:
        return pool_conn
    except Exception as e:
        return {"message": "error", "error": e}
