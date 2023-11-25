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


from plinkAPI.src.routers.conferences import dependencies as dependencies
from plinkAPI.src.routers.conferences import schemas as schemas


router = APIRouter()


@router.get(
    path="/conferences",
    response_model=schemas.Conferences,
    status_code=status.HTTP_200_OK,
)
def conferences_data(
    conference_data: schemas.Conferences = Depends(
        dependencies.valid_all_conference_data
    ),
):
    return conference_data


@router.get(
    path="/conferences/all",
    response_model=schemas.Conferences,
    status_code=status.HTTP_200_OK,
)
def all_conferences_data(
    all_conferences_data=Depends(dependencies.get_conference_data),
):
    pass


@router.get(
    path="/conferences/ids",
    response_model=dict[str, list[schemas.ConferenceIds]],
    status_code=status.HTTP_200_OK,
)
def all_conferences_ids(
    conference_ids: dict[str, list[schemas.ConferenceIds]] = Depends(
        dependencies.valid_conference_ids
    ),
):
    return conference_ids


@router.get(
    path="/conferences/{conference_id}",
    response_model=schemas.Conferences,
    status_code=status.HTTP_200_OK,
)
def conference_data_id(
    conference_id: int,
    conference_data: schemas.Conferences = Depends(
        dependencies.valid_conference_id_data
    ),
):
    return conference_data


@router.get(
    path="/conferences/{conference_id}/divisions",
    response_model=schemas.Conferences,
    status_code=status.HTTP_200_OK,
)
def conference_id_division_data(
    conference_id: int,
    conference_data: schemas.Conferences = Depends(
        dependencies.valid_conference_id_data
    ),
    division_data: schemas.Divisions = Depends(dependencies.valid_division_data),
):
    response = {"conferences": conference_data["conferences"]}
    response["conferences"][0]["divisions"] = division_data["divisions"]
    return response


@router.get(
    path="/conferences/{conference_id}/teams",
    response_model=schemas.Conferences,
    status_code=status.HTTP_200_OK,
)
def conference_id_teams_data(
    conference_id: int,
    conference_data: schemas.Conferences = Depends(
        dependencies.valid_conference_id_data
    ),
    team_data: schemas.Teams = Depends(dependencies.valid_teams_data),
):
    response = {"conferences": conference_data["conferences"]}
    response["conferences"][0]["teams"] = team_data["teams"]
    return response


@router.get(
    path="/conferences/{conference_id}/all",
    response_model=schemas.Conferences,
    status_code=status.HTTP_200_OK,
)
def all_conference_data_id(
    conference_id: int,
    conference_data: schemas.Conferences = Depends(
        dependencies.valid_conference_id_data
    ),
    division_data: schemas.Divisions = Depends(dependencies.valid_division_data),
    team_data: schemas.Teams = Depends(dependencies.valid_teams_data),
):
    response = {"conferences": conference_data["conferences"]}
    response["conferences"][0]["divisions"] = division_data["divisions"]
    response["conferences"][0]["teams"] = team_data["teams"]
    return response
