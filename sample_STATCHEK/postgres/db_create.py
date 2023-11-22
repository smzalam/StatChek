from psycopg.errors import OperationalError, ProgrammingError, InternalError
from db_connect import get_conn
from db_helper_functions import readSQLCommands

file_create_commands = readSQLCommands(
    "postgres/statchekapi_sql/create_statchekapi.sql"
)
file_delete_commands = readSQLCommands(
    "postgres/statchekapi_sql/delete_statchekapi.sql"
)
create_sql_commands = [
    command
    for command in file_create_commands
    if "---" not in command and command != ""
]
delete_database_sql_command = [
    command
    for command in file_delete_commands
    if "---" not in command and command != ""
]


def main():
    # for deleting database
    print("deleting database")
    with get_conn(auto=True) as conn:
        try:
            command = delete_database_sql_command[0]
            conn.execute(command)
            print(f"\nCommand executed: {command}")
        except (ProgrammingError, OperationalError, InternalError) as e:
            print(f"error: {e}")

    # for creating database
    with get_conn(auto=True) as conn:
        try:
            command = create_sql_commands[0]
            conn.execute(command)
            print(f"\nCommand executued: {command}")
        except (ProgrammingError, OperationalError, InternalError) as e:
            print(f"error: {e}")

    # for creating tables
    with get_conn(db=True, auto=True) as conn:
        for command in create_sql_commands[1:]:
            try:
                conn.execute(command)
                print(f"\nCommand executed: {command}")
            except (ProgrammingError, OperationalError, InternalError) as e:
                print(f"error: {e}")


if __name__ == "__main__":
    main()
