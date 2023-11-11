from psycopg import sql


def sql_execute_read_query(db_conn, query, identifier, params):
    with db_conn.connection() as conn:
        if identifier:
            data = conn.execute(
                sql.SQL(query).format(table=sql.Identifier(identifier)), params
            ).fetchall()
        else:
            data = conn.execute(query, params).fetchall()
        return data


def sql_execute_write_query(db_conn, query, params: list):
    with db_conn.connection() as conn:
        data = conn.execute(query, params)
        return data


def format_table_columns(
    db_conn,
    query: str,
    identifier: str = None,
    params: list | tuple = None,
):
    table_columns = sql_execute_read_query(db_conn, query, identifier, params)
    formatted_table_columns = [name[0] for name in table_columns]
    return formatted_table_columns


def format_table_records(
    db_conn,
    query: str,
    identifier: str = None,
    params: list | tuple = None,
):
    table_records = sql_execute_read_query(db_conn, query, identifier, params)
    formatted_table_records = [list(name) for name in table_records]
    return formatted_table_records


def format_db_response(columns: list, records: list):
    db_response = [
        {col: rec for col, rec in zip(columns, record)} for record in records
    ]
    return db_response


def executing_formatting_query_from_db(
    db_conn,
    col_query,
    rec_query,
    col_identifer,
    rec_identifier,
    col_params,
    rec_params,
):
    columns = format_table_columns(
        db_conn, col_query, col_identifer, params=[col_params]
    )
    try:
        rec_params = list(rec_params) if rec_params != None else None
    except TypeError as e:
        print(f"Error: {e}")
        rec_params = [rec_params]
    records = format_table_records(
        db_conn, rec_query, rec_identifier, params=rec_params
    )
    data = format_db_response(columns, records)
    return data
