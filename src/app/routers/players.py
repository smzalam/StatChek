from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .db_api_mediation_functions import *
from .database.db_connect import get_pool
from pprint import pprint


router = APIRouter()
pool_conn = get_pool()


@router.get("/players/{player_id}")
def player_data(player_id: int):
    table = "rosters"
    response = select_players_by_ids_function(pool_conn, table, "player_id", player_id)
    return response


# @app.get("/players/search")
