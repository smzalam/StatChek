from pprint import pprint
from enum import Enum
import json
import os
import shutil

from plinkAPI.src.database.setup import db_commands
from plinkAPI.src.utils import database_operations



"""
CACHE FUNCTIONS
"""


class CACHE_ACTION(str, Enum):
    READ = "read"
    WRITE = "write"


def update_cache(directory):
    for root, dirs, files in os.walk(directory):
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
            print("Created local cache from data")


"""
DATABASE FUNCTIONS
"""


def query_data_from_db(
    json_cache_api: str | None,
    db_conn_api,
    rec_query_api,
    col_identifier_api,
    rec_identifier_api,
    col_paramas_api,
    rec_params_api,
    cache: bool = True,
):
    if cache:
        try:
            data = reading_or_writing_cache(json_cache_api, CACHE_ACTION.READ.value)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"No local cache found... ({e})")
            print("Fetched new data from database...(Creating local cache)")
            data = database_operations.executing_formatting_query_from_db(
                db_conn=db_conn_api,
                col_query=db_commands.select_column_names,
                rec_query=rec_query_api,
                col_identifer=col_identifier_api,
                rec_identifier=rec_identifier_api,
                col_params=col_paramas_api,
                rec_params=rec_params_api,
            )
            reading_or_writing_cache(json_cache_api, CACHE_ACTION.WRITE.value, data)
    else:
        data = database_operations.executing_formatting_query_from_db(
            db_conn=db_conn_api,
            col_query=db_commands.select_column_names,
            rec_query=rec_query_api,
            col_identifer=col_identifier_api,
            rec_identifier=rec_identifier_api,
            col_params=col_paramas_api,
            rec_params=rec_params_api,
        )
    return data


def select_all_ids_function(directory, db_conn, db_table):
    record_command_mapping = {
        "conferences": db_commands.select_conference_ids,
        "divisions": db_commands.select_division_ids,
        "teams": db_commands.select_team_ids,
        "teams_info": db_commands.select_team_ids,
    }
    json_cache = f"{directory}/{db_table}_all_ids"
    data = query_data_from_db(
        json_cache_api=json_cache,
        db_conn_api=db_conn,
        rec_query_api=record_command_mapping[db_table],
        col_identifier_api=None,
        rec_identifier_api=None,
        col_paramas_api=db_table,
        rec_params_api=None,
        cache=False,
    )
    data = [list(row.values())[0] for row in data]
    return data


def select_all_function(directory, db_conn, db_table):
    json_cache = f"{directory}/{db_table}_all_data"
    data = query_data_from_db(
        json_cache_api=json_cache,
        db_conn_api=db_conn,
        rec_query_api=db_commands.select_all_records,
        col_identifier_api=None,
        rec_identifier_api=db_table,
        col_paramas_api=db_table,
        rec_params_api=None,
    )
    return data


def select_conference_by_id_function(directory, db_conn, db_table, conference_id):
    json_cache = f"{directory}/{db_table}_{conference_id}"
    data = query_data_from_db(
        json_cache_api=json_cache,
        db_conn_api=db_conn,
        rec_query_api=db_commands.select_conference_by_id,
        col_identifier_api=None,
        rec_identifier_api=None,
        col_paramas_api=db_table,
        rec_params_api=conference_id,
    )

    return data


def select_divisions_by_ids_function(directory, db_conn, db_table, id_type, id_num):
    json_cache = f"{directory}/{db_table}_{id_type}_{id_num}"
    data = query_data_from_db(
        json_cache_api=json_cache,
        db_conn_api=db_conn,
        rec_query_api=db_commands.select_division_by_id,
        col_identifier_api=None,
        rec_identifier_api=id_type,
        col_paramas_api=db_table,
        rec_params_api=id_num,
    )

    return data


def select_teams_by_ids_function(directory, db_conn, db_table, id_type, id_num):
    json_cache = f"{directory}/{db_table}_{id_type}_{id_num}"
    data = query_data_from_db(
        json_cache_api=json_cache,
        db_conn_api=db_conn,
        rec_query_api=db_commands.select_teams_by_id,
        col_identifier_api=None,
        rec_identifier_api=id_type,
        col_paramas_api=db_table,
        rec_params_api=id_num,
    )

    return data


def select_teamstatsranks_by_teamid_function(
    directory, db_conn, db_table, team_id, detail_type
):
    db_function = (
        db_commands.select_teamstats_by_id
        if detail_type == "stats"
        else db_commands.select_teamranks_by_id
    )
    json_cache = f"{directory}/{db_table}_{detail_type}_{team_id}"
    data = query_data_from_db(
        json_cache_api=json_cache,
        db_conn_api=db_conn,
        rec_query_api=db_function,
        col_identifier_api=None,
        rec_identifier_api=None,
        col_paramas_api=db_table,
        rec_params_api=team_id,
    )

    return data


def select_teamstatsranks_by_teamid_season_function(
    directory, db_conn, db_table, team_id, season, detail_type
):
    db_function = (
        db_commands.select_teamstats_by_id_season
        if detail_type == "stats"
        else db_commands.select_teamranks_by_id_season
    )
    json_cache = f"{directory}/{db_table}_{team_id}_{season}_{detail_type}"
    data = query_data_from_db(
        json_cache_api=json_cache,
        db_conn_api=db_conn,
        rec_query_api=db_function,
        col_identifier_api=None,
        rec_identifier_api=None,
        col_paramas_api=db_table,
        rec_params_api=[team_id, season],
    )

    return data


def select_players_by_teamid_function(directory, db_conn, db_table, id_type, id_num):
    json_cache = f"{directory}/{db_table}_{id_type}_{id_num}"
    data = query_data_from_db(
        json_cache_api=json_cache,
        db_conn_api=db_conn,
        rec_query_api=db_commands.select_players_by_id,
        col_identifier_api=None,
        rec_identifier_api=id_type,
        col_paramas_api=db_table,
        rec_params_api=id_num,
    )

    return data


def select_players_by_teamid_season_function(
    directory, db_conn, db_table, team_id, season
):
    json_cache = f"{directory}/{db_table}_{team_id}_{season}"
    data = query_data_from_db(
        json_cache_api=json_cache,
        db_conn_api=db_conn,
        rec_query_api=db_commands.select_players_by_teamid_season,
        col_identifier_api=None,
        rec_identifier_api=None,
        col_paramas_api=db_table,
        rec_params_api=[team_id, season],
    )

    return data


def select_user_details_id_function(db_conn, db_table, id_type, id_num):
    json_cache = None
    data = query_data_from_db(
        json_cache_api=json_cache,
        db_conn_api=db_conn,
        rec_query_api=db_commands.select_user_details_id,
        col_identifier_api=None,
        rec_identifier_api=id_type,
        col_paramas_api=db_table,
        rec_params_api=[id_num],
        cache=False,
    )

    return data


def delete_user_function(db_conn, db_table, user_details: list, id_type):
    database_operations.sql_execute_write_query(
        db_conn=db_conn,
        query=db_commands.delete_user,
        params=user_details,
    )
    return f"Deleted user with email: {user_details[0]} successfully!"


def insert_users_new_function(
    db_conn,
    db_table,
    user_details: list,
    id_type,
):
    database_operations.sql_execute_write_query(
        db_conn=db_conn,
        query=db_commands.insert_new_user,
        params=user_details,
    )
    new_user = select_user_details_id_function(
        db_conn=db_conn,
        db_table=db_table,
        id_type=id_type,
        id_num=user_details[0],
    )
    return new_user
