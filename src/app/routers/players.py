from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .db_api_mediation_functions import *
from .database.db_connect import get_pool
from .schemas import *
from pprint import pprint
from psycopg_pool import ConnectionPool


router = APIRouter()


@router.get("/players/{player_id}", response_model=Players)
def player_data(player_id: int, pool_conn: ConnectionPool = Depends(get_pool)):
    metadata = {"table": "rosters", "id_type": "player_id"}
    players_data = select_players_by_ids_function(
        pool_conn, metadata["table"], metadata["id_type"], player_id
    )
    response = {"player_id": player_id, "players": players_data}
    return response


# @app.get("/players/search")
