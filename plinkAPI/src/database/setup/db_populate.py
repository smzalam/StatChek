import os
import csv

from psycopg import sql
from psycopg.errors import (
    OperationalError,
    ProgrammingError,
    InternalError,
    ForeignKeyViolation,
    UniqueViolation,
)
from plinkAPI.src.database.setup import db_connect
from plinkAPI.src.utils import file_operations


base_file_path = "./src/app/scraped_data/cleaned_csv/"
csv_files = [file for file in os.listdir(base_file_path)]
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
    "conferences",
    "divisions",
    "teams",
    "teams_info",
    "teams_stats",
    "teams_ranks",
    "players",
    "rosters",
]
sql_csv_files = {k: v for k, v in zip(sql_table_names, csv_files)}


def main():
    def check_null(table):
        table_null = conn.execute(
            sql.SQL(sql_check_null_command).format(table=sql.Identifier(table))
        ).fetchone()[0]
        return True if not table_null else False

    def insert_records(table, data):
        with conn.cursor().copy(
            sql.SQL(sql_db_command).format(table=sql.Identifier(table))
        ) as copy:
            for record in data[1:]:
                print(record)
                copy.write_row(record)
        print("All records successfully inserted.")

    with db_connect.get_conn(db=True, auto=True) as conn:
        for order, table in enumerate(sql_table_names):
            null_value = check_null(table)
            if null_value:
                try:
                    data = file_operations.convert_csv_to_tuple_list(
                        f"{base_file_path}{csv_files[order]}"
                    )
                    insert_records(table, data)
                except (ProgrammingError, OperationalError, InternalError) as e:
                    print(e)
            else:
                continue


if __name__ == "__main__":
    main()
