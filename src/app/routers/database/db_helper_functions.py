from psycopg import sql


def sql_execute_query(db_conn, query, identifier, params):
    with db_conn.connection() as conn:
        if identifier:
            data = conn.execute(
                sql.SQL(query).format(table=sql.Identifier(identifier)), params
            ).fetchall()
        else:
            data = conn.execute(query, params).fetchall()
        return data


def format_table_item(
    db_conn,
    query: str,
    column: bool,
    identifier: str = None,
    params: list | tuple = None,
):
    table_columns = sql_execute_query(db_conn, query, identifier, params)
    if column:
        formatted_table_columns = [name[0] for name in table_columns]
        return formatted_table_columns
    else:
        formatted_table_records = [list(name) for name in table_columns]
        return formatted_table_records


def format_db_response(columns: list, records: list):
    db_response = [
        {col: rec for col, rec in zip(columns, record)} for record in records
    ]
    return db_response


# pprint(format_table_item(pool_conn, identify, False, "conferences"))
