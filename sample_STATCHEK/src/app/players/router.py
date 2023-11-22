from pprint import pprint
import json

from fastapi import (
    FastAPI,
    Response,
    status,
    HTTPException,
    Depends,
    APIRouter,
    Query,
    Path,
    Depends,
)
from psycopg_pool import ConnectionPool

import src.app.auth as auth

import src.app.database.database as db

import src.app.players.dependencies as dependencies
import src.app.players.schemas as schemas


router = APIRouter(dependencies=[Depends(auth.valid_current_user)])


@router.get(
    "/players/{player_id}",
    response_model=schemas.Players,
    status_code=status.HTTP_200_OK,
)
def player_data(
    player_id: int,
    player_data=Depends(dependencies.valid_player_id_data),
):
    return player_data
