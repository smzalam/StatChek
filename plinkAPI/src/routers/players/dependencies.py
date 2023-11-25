from psycopg_pool import ConnectionPool
from fastapi import Depends
from pprint import pprint

from plinkAPI.src.config import constants as constants
from plinkAPI.src.database.setup import db_connect as db
from plinkAPI.src.middleware.data_adapter import db_service as db_funcs
from plinkAPI.src.routers.players import schemas as schemas


def valid_player_id_data(
    player_id: int,
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> schemas.Players:
    player_data = db_funcs.select_players_by_teamid_function(
        directory=constants.PLAYERS_CACHE_DIRECTORY,
        db_conn=pool_conn,
        db_table=constants.PLAYERS_TABLE,
        id_type="player_id",
        id_num=player_id,
    )
    if not player_data:
        raise NameError
    return {"player_id": player_id, "players": player_data}


# constants.ALL_PLAYER_IDS = valid_divisions_ids_list()
print("No function to update player ids constant!")
db_funcs.update_cache(constants.PLAYERS_CACHE_DIRECTORY)
