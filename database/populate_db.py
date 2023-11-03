from psycopg import sql
from psycopg.errors import OperationalError, ProgrammingError, InternalError, ForeignKeyViolation, UniqueViolation
from db_connect import get_conn
from helper_functions import readSQLCommands, convert_csv_to_tuple_list
import pandas as pd
import os
import csv

base_file_path = './src/data/cleaned_csv/'
csv_files = [file for file in os.listdir('./src/data/cleaned_csv')]
sql_db_command = """
                    COPY {table}
                    FROM STDIN;
                """
sql_check_null_command = """
                            SELECT CASE 
                            WHEN EXISTS (SELECT * FROM {table} LIMIT 1) THEN 1
                            ELSE 0 
                            END
                        """
sql_table_names = [
                'conferences',
                'divisions',
                'teams',
                'teams_info',
                'teams_stats',
                'teams_ranks',
                'players',
                'rosters'
]
sql_csv_files = {k:v for k,v in zip(sql_table_names,csv_files)}

with get_conn(db=True, auto=True) as conn:
    for order, table in enumerate(sql_table_names):
        table_null = conn.execute(sql.SQL(sql_check_null_command).format(table=sql.Identifier(table))).fetchone()[0]
        if not table_null:
            try:
                data = convert_csv_to_tuple_list(f'{base_file_path}{csv_files[order]}')
            except Exception as e:
                print(e)
            try:
                with conn.cursor().copy(
                    sql.SQL(sql_db_command).format(table=sql.Identifier(table))
                ) as copy:
                    for record in data[1:]:
                        print(record)
                        copy.write_row(record)
                print('All records successfully inserted.')
            except (ProgrammingError, OperationalError, InternalError) as e:
                print(e)
        else: 
            continue