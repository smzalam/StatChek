from psycopg.errors import OperationalError, ProgrammingError, InternalError
from db_connect import get_conn
from db_helper_functions import readSQLCommands

file_commands = readSQLCommands('./database/statchekapi_sql/create_statchekapi.sql')
sql_commands = [command for command in file_commands if '---' not in command and command != '']

# for creating database
with get_conn(auto=True) as conn:
    try:
        command = sql_commands[0]
        conn.execute(command)
        print(f"\nCommand executued: {command}")
    except (ProgrammingError, OperationalError, InternalError) as e:
        print(e)

# for creating tables
with get_conn(db=True, auto=True) as conn:
    for command in sql_commands[1:]:
        try:
            conn.execute(command)
            print(f"\nCommand executed: {command}")
        except (ProgrammingError, OperationalError, InternalError) as e:
            print(e)
