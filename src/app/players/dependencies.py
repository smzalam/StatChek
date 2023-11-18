from psycopg_pool import ConnectionPool
from fastapi import Depends
from pprint import pprint

import src.database.database as db
import src.database.db_service as db_funcs
import src.players.schemas as schemas
import src.players.constants as constants


def valid_player_id_data(
    player_id: int,
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> schemas.Players:
    player_data = db_funcs.select_players_by_teamid_function(
        directory=constants.CACHE_DIRECTORY,
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
db_funcs.update_cache(constants.CACHE_DIRECTORY)
