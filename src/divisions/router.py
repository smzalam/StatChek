from typing import Annotated
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

import src.database.database as db

import src.divisions.dependencies as dependencies
import src.divisions.schemas as schemas


router = APIRouter()


@router.get(
    path="/divisions",
    response_model=schemas.Divisions,
    status_code=status.HTTP_200_OK,
)
def divisions_data(
    division_data: schemas.Divisions = Depends(dependencies.valid_all_division_data),
):
    return division_data


@router.get(
    path="/divisions/ids",
    response_model=dict[str, list[schemas.DivisionsIds]],
    status_code=status.HTTP_200_OK,
)
def all_division_ids(
    division_ids: dict[str, list[schemas.DivisionsIds]] = Depends(
        dependencies.valid_division_ids
    ),
):
    return division_ids


@router.get(
    path="/divisions/{division_id}",
    response_model=schemas.Divisions,
    status_code=status.HTTP_200_OK,
)
def division_data_id(
    division_id: int,
    division_data: schemas.Divisions = Depends(dependencies.valid_division_id_data),
):
    return division_data


@router.get(
    path="/divisions/{division_id}/teams",
    response_model=schemas.Divisions,
    status_code=status.HTTP_200_OK,
)
def conference_id_teams_data(
    division_id: int,
    division_data: schemas.Divisions = Depends(dependencies.valid_division_id_data),
    team_data: schemas.Teams = Depends(dependencies.valid_teams_data),
):
    response = {"divisions": division_data["divisions"]}
    response["divisions"][0]["teams"] = team_data["teams"]
    return response
