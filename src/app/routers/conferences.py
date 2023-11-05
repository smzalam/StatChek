from typing import Annotated
from fastapi import (
    FastAPI,
    Response,
    status,
    HTTPException,
    Depends,
    APIRouter,
    Query,
    Path,
)
from .db_api_mediation_functions import *
from .database.db_connect import get_pool
from .schemas import *
from pprint import pprint
import json


router = APIRouter()
pool_conn = get_pool()


def get_all_conference_data(conference_ids: list):
    tables = {
        "conference_table": "conferences",
        "divisions_table": "divisions",
        "teams_table": "teams_info",
    }
    response = []
    for conference_id in conference_ids:
        conference_data = select_conference_by_id_function(
            pool_conn, tables["conference_table"], conference_id
        )[0]
        conference_data["divisions"] = select_divisions_by_ids_function(
            pool_conn, tables["divisions_table"], "conference_id", conference_id
        )
        conference_data["teams"] = select_teams_by_ids_function(
            pool_conn, tables["teams_table"], "conference_id", conference_id
        )

        response.append(conference_data)
    return response


@router.get("/conferences", response_model=Conferences)
def conferences_data(all: bool = False):
    if not all:
        table = "conferences"
        conference_data = select_all_function(pool_conn, table)
        response = {"conferences": conference_data}
        return response
    else:
        conference_ids = [5, 6]
        conference_data = get_all_conference_data(conference_ids)
        if not conference_data:
            return {
                "message": f"No such conference exists with id: {conference_id}",
                "id_sent": f"{conference_id}",
            }
        else:
            response = {"conferences": conference_data}
            return response


@router.get("/conferences/{conference_id}", response_model=Conferences)
def conference_data_id(
    conference_id: Annotated[int, Path(title="the ID of the conference to get")]
):
    table = "conferences"
    conference_data = select_conference_by_id_function(pool_conn, table, conference_id)
    if not conference_data:
        return {
            "message": f"No such conference exists with id: {conference_id}",
            "id_sent": f"{conference_id}",
        }
    else:
        response = {"conferences": conference_data}
        return response


@router.get("/conferences/{conference_id}/divisions", response_model=Conferences)
def conference_id_division_data(
    conference_id: Annotated[
        int, Path(title="the ID of the conference from which to get divisions")
    ]
):
    tables = {"conference_table": "conferences", "division_table": "divisions"}
    conference_data = select_conference_by_id_function(
        pool_conn, tables["conference_table"], conference_id
    )[0]
    conference_data["divisions"] = select_divisions_by_ids_function(
        pool_conn, tables["division_table"], "conference_id", conference_id
    )
    response = {"conferences": [conference_data]}
    if not response:
        return {
            "message": f"No such conference exists with id: {conference_id}",
            "id_sent": f"{conference_id}",
        }
    else:
        return response


@router.get("/conferences/{conference_id}/teams", response_model=Conferences)
def conference_id_teams_data(
    conference_id: Annotated[
        int, Path(title="the ID of the conference from which to get teams")
    ]
):
    tables = {"conference_table": "conferences", "teams_table": "teams_info"}
    conference_data = select_conference_by_id_function(
        pool_conn, tables["conference_table"], conference_id
    )[0]
    conference_data["teams"] = select_teams_by_ids_function(
        pool_conn, tables["teams_table"], "conference_id", conference_id
    )
    response = {"conferences": [conference_data]}
    if not response:
        return {
            "message": f"No such conference exists with id: {conference_id}",
            "id_sent": f"{conference_id}",
        }
    else:
        return response
