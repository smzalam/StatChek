from psycopg_pool import ConnectionPool
from fastapi import Depends
from pprint import pprint

import src.database.database as db
import src.database.db_service as db_funcs
import src.divisions.schemas as schemas
import src.divisions.constants as constants


def valid_divisions_ids_list(
    pool_conn: ConnectionPool = db.get_pool(),
) -> list:
    division_ids = db_funcs.select_all_ids_function(
        directory=constants.CACHE_DIRECTORY,
        db_conn=pool_conn,
        db_table=constants.DIVISION_TABLE,
    )

    return division_ids


def valid_division_ids(
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> dict[str, [schemas.DivisionsIds]]:
    division_data = db_funcs.select_all_function(
        directory=constants.CACHE_DIRECTORY,
        db_conn=pool_conn,
        db_table=constants.DIVISION_TABLE,
    )
    division_ids = [
        #! CHANGE 'ID' TO 'DIVISION_ID' FOR DIVISONS TABLE IN DATABASE
        #! CHANGE 'NAME' TO 'DIVISION_NAME' FOR DIVISIONS TABLE IN DATABASE
        {
            "division_id": division_data_row[constants.DIVISION_ID_COLUMN],
            "name": division_data_row[constants.DIVISION_NAME_COLUMN],
        }
        for division_data_row in division_data
    ]
    return {"division_ids": division_ids}


def valid_division_id_data(
    division_id: int,
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> schemas.Divisions:
    division_data = db_funcs.select_divisions_by_ids_function(
        directory=constants.CACHE_DIRECTORY,
        db_conn=pool_conn,
        db_table=constants.DIVISION_TABLE,
        division_id=division_id,
    )
    if not division_data:
        raise NameError
    return {"divisions": division_data}


def valid_all_division_data(
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> schemas.Divisions:
    divisions_data = db_funcs.select_all_function(
        directory=constants.CACHE_DIRECTORY,
        db_conn=pool_conn,
        db_table=constants.DIVISION_TABLE,
    )

    if not divisions_data:
        raise NameError

    return {"divisions": divisions_data}


def valid_teams_data(
    division_id: int,
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> schemas.Teams:
    teams_data = db_funcs.select_teams_by_ids_function(
        directory=constants.CACHE_DIRECTORY,
        db_conn=pool_conn,
        db_table=constants.TEAMS_INFO_TABLE,
        id_type=constants.DIVISION_ID_TYPE,
        id_num=division_id,
    )

    if not teams_data:
        raise NameError
    return {"teams": teams_data}


def get_conference_data(
    conference_id: int,
    division_data: schemas.Divisions = Depends(valid_division_id_data),
    teams_data: schemas.Teams = Depends(valid_teams_data),
):
    pass


constants.ALL_DIVISION_IDS = valid_divisions_ids_list()
print("Updated division ids constant!")
