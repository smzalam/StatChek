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

from plinkAPI.src.routers.players import dependencies as dependencies
from plinkAPI.src.routers.players import schemas as schemas


router = APIRouter()


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
