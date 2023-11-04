from database.db_commands import *
from database.db_helper_functions import *
from database.db_commands import *
from pprint import pprint


def select_all_function(db_conn, table):
    columns = format_table_item(db_conn, select_column_names, True, params=[table])
    records = format_table_item(db_conn, select_all_records, False, table)
    data = format_db_response(columns, records)
    return data
