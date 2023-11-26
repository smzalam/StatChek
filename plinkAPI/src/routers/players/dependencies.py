from psycopg_pool import ConnectionPool
from fastapi import Depends, HTTPException, status
from pprint import pprint

from src.config import constants as constants
from src.database.setup import db_connect as db
from src.middleware.data_adapter import db_service as db_funcs
from src.routers.players import schemas as schemas


def valid_player_id(
    player_id: int, 
    pool_conn: ConnectionPool = Depends(db.get_pool),
):
   pass

def valid_player_id_data(
    player_id: int,
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> schemas.Players:
    player_data = db_funcs.select_players_by_teamid_function(
        directory=constants.PLAYERS_CACHE_DIRECTORY,
        db_conn=pool_conn,
        db_table=constants.PLAYERS_TABLE,
        id_type=constants.PLAYERS_ID_COLUMN,
        id_num=player_id,
    )
    if not player_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                'response': 'Error',
                'message': 'Player ID does not exist'            }
        )
    return {"player": player_id, "data": player_data}

def valid_player_name_data(
    player_name: str,
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> schemas.Players:
    print(player_name)
    player_data = db_funcs.select_players_by_teamid_function(
        directory=constants.PLAYERS_CACHE_DIRECTORY,
        db_conn=pool_conn,
        db_table=constants.PLAYERS_TABLE,
        id_type=constants.PLAYERS_NAME_COLUMN,
        id_num=player_name,
    )
    if not player_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                'response': 'Error',
                'message': 'Player Name does not exist'            }
        )
    return {"player": player_name, "data": player_data}


# constants.ALL_PLAYER_IDS = valid_divisions_ids_list()
print("No function to update player ids constant!")
db_funcs.update_cache(constants.PLAYERS_CACHE_DIRECTORY)
