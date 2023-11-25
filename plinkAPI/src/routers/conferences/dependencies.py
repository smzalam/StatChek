from psycopg_pool import ConnectionPool
from fastapi import Depends
from pprint import pprint

from plinkAPI.src.config import constants as constants
from plinkAPI.src.database.setup import db_connect as db
from plinkAPI.src.middleware.data_adapter import db_service as db_funcs
from plinkAPI.src.routers.conferences import schemas as schemas


def valid_conference_ids_list(
    pool_conn: ConnectionPool = db.get_pool(),
) -> list:
    conference_ids = db_funcs.select_all_ids_function(
        directory=constants.CONFERENCES_CACHE_DIRECTORY,
        db_conn=pool_conn,
        db_table=constants.CONFERENCE_TABLE,
    )

    return conference_ids


def valid_conference_ids(
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> dict[str, [schemas.ConferenceIds]]:
    conference_data = db_funcs.select_all_function(
        directory=constants.CONFERENCES_CACHE_DIRECTORY,
        db_conn=pool_conn,
        db_table=constants.CONFERENCE_TABLE,
    )
    print("conf: ", conference_data)
    conference_ids = [
        #! CHANGE 'ID' TO 'CONFERENCE_ID' FOR CONFERENCES TABLE IN DATABASE
        #! CHANGE 'NAME' TO 'CONFERENCE_NAME' FOR CONFERENCES TABLE IN DATABASE
        {
            "conference_id": conference_data_row[constants.CONFERENCE_ID_TYPE],
            "name": conference_data_row[constants.CONFERENCE_NAME_TYPE],
        }
        for conference_data_row in conference_data
    ]

    return {"conference_ids": conference_ids}

def valid_conference_id(
    conference_id: int,
):
    if conference_id not in constants.ALL_CONFERENCE_IDS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= {
                'response': 'Error',
                'message': 'Division ID does not exist'
            }
        )
    return conference_id

def valid_conference_id_data(
    conference_id = Depends(valid_conference_id),
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> schemas.Conferences:
    conference_data = db_funcs.select_conference_by_id_function(
        directory=constants.CONFERENCES_CACHE_DIRECTORY,
        db_conn=pool_conn,
        db_table=constants.CONFERENCE_TABLE,
        conference_id=conference_id,
    )
    if not conference_data:
        raise NameError
    return {"conferences": conference_data}


def valid_all_conference_data(
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> schemas.Conferences:
    conferences_data = db_funcs.select_all_function(
        directory=constants.CONFERENCES_CACHE_DIRECTORY,
        db_conn=pool_conn,
        db_table=constants.CONFERENCE_TABLE,
    )

    if not conferences_data:
        raise NameError

    return {"conferences": conferences_data}


def valid_division_data(
    conference_id = Depends(valid_conference_id),
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> schemas.Divisions:
    divisions_data = db_funcs.select_divisions_by_ids_function(
        directory=constants.CONFERENCES_CACHE_DIRECTORY,
        db_conn=pool_conn,
        db_table=constants.DIVISIONS_TABLE,
        id_type=constants.CONFERENCE_ID_TYPE,
        id_num=conference_id,
    )

    if not divisions_data:
        raise NameError
    return {"divisions": divisions_data}


def valid_teams_data(
    conference_id = Depends(valid_conference_id),
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> schemas.Teams:
    teams_data = db_funcs.select_teams_by_ids_function(
        directory=constants.CONFERENCES_CACHE_DIRECTORY,
        db_conn=pool_conn,
        db_table=constants.TEAMS_INFO_TABLE,
        id_type=constants.CONFERENCE_ID_TYPE,
        id_num=conference_id,
    )

    if not teams_data:
        raise NameError
    return {"teams": teams_data}


def get_conference_data(
    conference_id = Depends(valid_conference_id),
    conference_data: schemas.Conferences = Depends(valid_all_conference_data),
    division_data=Depends(valid_division_data),
    teams_data=Depends(valid_teams_data),
):
    pass


constants.ALL_CONFERENCE_IDS = valid_conference_ids_list()
print("Updated conference ids constant!")
db_funcs.update_cache(constants.CONFERENCES_CACHE_DIRECTORY)
