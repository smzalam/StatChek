from .database.db_commands import *
from .database.db_helper_functions import *
from .database.db_commands import *
from pprint import pprint


def select_all_function(db_conn, table):
    columns = format_table_item(
        db_conn, select_column_names, True, None, params=[table]
    )
    records = format_table_item(db_conn, select_all_records, False, None, table)
    data = format_db_response(columns, records)
    return data


def select_conference_by_id_function(db_conn, table, conference_id):
    columns = format_table_item(
        db_conn, select_column_names, True, None, params=[table]
    )
    records = format_table_item(
        db_conn, select_conference_by_id, False, None, params=[conference_id]
    )
    data = format_db_response(columns, records)
    return data


def select_divisions_by_ids_function(db_conn, table, id_type, id_num):
    columns = format_table_item(
        db_conn, select_column_names, True, None, params=[table]
    )
    records = format_table_item(
        db_conn, select_division_by_id, False, id_type, params=[id_num]
    )
    data = format_db_response(columns, records)
    return data


def select_teams_by_ids_function(db_conn, table, id_type, id_num):
    columns = format_table_item(
        db_conn, select_column_names, True, None, params=[table]
    )
    records = format_table_item(
        db_conn, select_teams_by_id, False, id_type, params=[id_num]
    )
    data = format_db_response(columns, records)
    return data


def select_teamstatsranks_by_teamid_function(
    db_conn, table, id_type, id_num, detail_type
):
    function = (
        select_teamstats_by_id if detail_type == "stats" else select_teamranks_by_id
    )
    columns = format_table_item(
        db_conn, select_column_names, True, None, params=[table]
    )
    records = format_table_item(db_conn, function, False, id_type, params=[id_num])
    data = format_db_response(columns, records)
    return data


def select_teamstatsranks_by_teamid_season_function(
    db_conn, table, team_id, season, detail_type
):
    function = (
        select_teamstats_by_id_season
        if detail_type == "stats"
        else select_teamranks_by_id_season
    )
    columns = format_table_item(
        db_conn, select_column_names, True, None, params=[table]
    )
    records = format_table_item(
        db_conn, function, False, None, params=[team_id, season]
    )
    data = format_db_response(columns, records)
    return data


def select_players_by_ids_function(db_conn, table, id_type, id_num):
    columns = format_table_item(
        db_conn, select_column_names, True, None, params=[table]
    )
    records = format_table_item(
        db_conn, select_players_by_id, False, id_type, params=[id_num]
    )
    data = format_db_response(columns, records)
    return data


def select_players_by_teamid_season_function(db_conn, table, team_id, season):
    columns = format_table_item(
        db_conn, select_column_names, True, None, params=[table]
    )
    records = format_table_item(
        db_conn, select_players_by_teamid_season, False, None, params=[team_id, season]
    )
    data = format_db_response(columns, records)
    return data
