from .database.db_commands import *
from .database.db_helper_functions import *
from .database.db_commands import *
from pprint import pprint
from enum import Enum
import json
import os
import shutil


class CACHE_ACTION(Enum):
    READ = "read"
    WRITE = "write"


def update_cache():
    for root, dirs, files in os.walk("src/app/routers/cache"):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


def reading_or_writing_cache(file_path, action, json_data=None):
    if action == "read":
        with open(file_path, "r") as file:
            data = json.load(file)
            print("Fetched data from local cache")
            return data
    elif action == "write":
        with open(file_path, "w+") as file:
            json.dump(json_data, file)


def executing_formatting_query_from_db(
    db_conn,
    rec_query,
    col_identifer,
    rec_identifier,
    col_params,
    rec_params: list = None,
):
    columns = format_table_item(
        db_conn, select_column_names, True, col_identifer, params=[col_params]
    )
    records = format_table_item(
        db_conn, rec_query, False, rec_identifier, params=rec_params
    )
    data = format_db_response(columns, records)
    return data


def select_all_function(db_conn, table):
    json_cache = f"src/app/routers/cache/{table}_all_data"
    try:
        data = reading_or_writing_cache(json_cache, CACHE_ACTION.READ.value)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"No local cache found... ({e})")
        print("Fetched new data from database...(Creating local cache)")
        data = executing_formatting_query_from_db(
            db_conn, select_all_records, None, table, table, None
        )
        reading_or_writing_cache(json_cache, CACHE_ACTION.WRITE.value, data)
    return data


def select_conference_by_id_function(db_conn, table, conference_id):
    json_cache = f"src/app/routers/cache/{table}_{conference_id}"
    try:
        data = reading_or_writing_cache(json_cache, CACHE_ACTION.READ.value)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"No local cache found... ({e})")
        print("Fetched new data from database...(Creating local cache)")
        data = executing_formatting_query_from_db(
            db_conn, select_conference_by_id, None, None, table, [conference_id]
        )
        reading_or_writing_cache(json_cache, CACHE_ACTION.WRITE.value, data)

    return data


def select_divisions_by_ids_function(db_conn, table, id_type, id_num):
    json_cache = f"src/app/routers/cache/{table}_{id_type}_{id_num}"
    try:
        data = reading_or_writing_cache(json_cache, CACHE_ACTION.READ.value)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"No local cache found... ({e})")
        print("Fetched new data from database...(Creating local cache)")
        data = executing_formatting_query_from_db(
            db_conn, select_division_by_id, None, id_type, table, [id_num]
        )
        reading_or_writing_cache(json_cache, CACHE_ACTION.WRITE.value, data)

    return data


def select_teams_by_ids_function(db_conn, table, id_type, id_num):
    json_cache = f"src/app/routers/cache/{table}_{id_type}_{id_num}"
    try:
        data = reading_or_writing_cache(json_cache, CACHE_ACTION.READ.value)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"No local cache found... ({e})")
        print("Fetched new data from database...(Creating local cache)")
        data = executing_formatting_query_from_db(
            db_conn, select_teams_by_id, None, id_type, table, [id_num]
        )
        reading_or_writing_cache(json_cache, CACHE_ACTION.WRITE.value, data)

    return data


def select_teamstatsranks_by_teamid_function(
    db_conn, table, id_type, id_num, detail_type
):
    function = (
        select_teamstats_by_id if detail_type == "stats" else select_teamranks_by_id
    )
    json_cache = f"src/app/routers/cache/{table}_{id_type}_{id_num}"
    try:
        data = reading_or_writing_cache(json_cache, CACHE_ACTION.READ.value)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"No local cache found... ({e})")
        print("Fetched new data from database...(Creating local cache)")
        data = executing_formatting_query_from_db(
            db_conn, function, None, id_type, table, [id_num]
        )
        reading_or_writing_cache(json_cache, CACHE_ACTION.WRITE.value, data)

    return data


def select_teamstatsranks_by_teamid_season_function(
    db_conn, table, team_id, season, detail_type
):
    function = (
        select_teamstats_by_id_season
        if detail_type == "stats"
        else select_teamranks_by_id_season
    )
    json_cache = f"src/app/routers/cache/{table}_{team_id}_{season}_{detail_type}"
    try:
        data = reading_or_writing_cache(json_cache, CACHE_ACTION.READ.value)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"No local cache found... ({e})")
        print("Fetched new data from database...(Creating local cache)")
        data = executing_formatting_query_from_db(
            db_conn, function, None, None, table, [team_id, season]
        )
        reading_or_writing_cache(json_cache, CACHE_ACTION.WRITE.value, data)

    return data


def select_players_by_ids_function(db_conn, table, id_type, id_num):
    json_cache = f"src/app/routers/cache/{table}_{id_type}_{id_num}"
    try:
        data = reading_or_writing_cache(json_cache, CACHE_ACTION.READ.value)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"No local cache found... ({e})")
        print("Fetched new data from database...(Creating local cache)")
        data = executing_formatting_query_from_db(
            db_conn, select_players_by_id, None, id_type, table, [id_num]
        )
        reading_or_writing_cache(json_cache, CACHE_ACTION.WRITE.value, data)

    return data


def select_players_by_teamid_season_function(db_conn, table, team_id, season):
    json_cache = f"src/app/routers/cache/{table}_{team_id}_{season}"
    try:
        data = reading_or_writing_cache(json_cache, CACHE_ACTION.READ.value)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"No local cache found... ({e})")
        print("Fetched new data from database...(Creating local cache)")
        data = executing_formatting_query_from_db(
            db_conn,
            select_players_by_teamid_season,
            None,
            None,
            table,
            [team_id, season],
        )
        reading_or_writing_cache(json_cache, CACHE_ACTION.WRITE.value, data)

    return data


def select_user_details_id_function(db_conn, table, id_type, id_num):
    data = executing_formatting_query_from_db(
        db_conn, select_user_details_id, None, id_type, table, [id_num]
    )
    return data


def insert_users_new_function(db_conn, table, user_details: list):
    sql_execute_write_query(db_conn, insert_new_user, user_details)
    new_user = select_user_details_id_function(db_conn, table, None, user_details[0])
    return new_user


update_cache()
