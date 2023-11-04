from psycopg import sql
from db_connect import get_pool
from db_commands import *
from pprint import pprint

pool_conn = get_pool()


def sql_execute_query(db_conn, query, params: list | tuple = None):
    with db_conn.connection() as conn:
        data = conn.execute(query, params).fetchall()
        return data


def format_table_item(db_conn, query: str, column: bool, params: list | tuple = None):
    table_columns = sql_execute_query(db_conn, query, params)
    if column:
        formatted_table_columns = [name[0] for name in table_columns]
        return formatted_table_columns
    else:
        formatted_table_columns = [list(name) for name in table_columns]
        return formatted_table_columns


def format_db_response(columns: list, records: list):
    db_response = [
        {col: rec for col, rec in zip(columns, record)} for record in records
    ]
    return db_response
