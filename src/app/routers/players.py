from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .db_api_mediation_functions import *
from .database.db_connect import get_pool
from .schemas import *
from pprint import pprint


router = APIRouter()
pool_conn = get_pool()


@router.get("/players/{player_id}", response_model=Players)
def player_data(player_id: int):
    table = "rosters"
    players_data = select_players_by_ids_function(
        pool_conn, table, "player_id", player_id
    )
    response = {"player_id": player_id, "players": players_data}
    return response


# @app.get("/players/search")
