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


router = APIRouter()
pool_conn = get_pool()


def get_all_divisons_data(division_ids: list):
    tables = {
        "divisions_table": "divisions",
        "teams_table": "teams_info",
    }
    response = []
    for division_id in division_ids:
        division_data = select_divisions_by_ids_function(
            pool_conn, tables["divisions_table"], "id", division_id
        )[0]
        division_data["teams"] = select_teams_by_ids_function(
            pool_conn, tables["teams_table"], "division_id", division_id
        )
        response.append(division_data)
    return response


@router.get("/divisions", response_model=Divisions)
def divisions_data(all: bool = False):
    if not all:
        table = "divisions"
        division_data = select_all_function(pool_conn, table)
        response = {"divisions": division_data}
        return response
    else:
        division_ids = [15, 16, 17, 18]
        division_data = get_all_divisons_data(division_ids)
        response = {"divisions": division_data}
        if not response:
            return {
                "message": f"No such division exists with id: {division_ids}",
                "ids_sent": f"{division_ids}",
            }
        else:
            return response


@router.get("/divisions/{division_id}", response_model=Divisions)
def divisions_data_id(division_id: int, all: bool = False):
    if not all:
        table = "divisions"
        division_data = select_divisions_by_ids_function(
            pool_conn, table, "id", division_id
        )
        response = {"divisions": division_data}
        if not response:
            return {
                "message": f"No such division exists with id: {division_id}",
                "id_sent": f"{division_id}",
            }
        else:
            return response
    else:
        division_data = get_all_divisons_data([division_id])
        response = {"divisions": division_data}
        return response


@router.get("/divisions/{division_id}/teams", response_model=Divisions)
def division_id_teams_data(division_id):
    tables = {"divisions_table": "divisions", "teams_table": "teams_info"}
    division_data = select_divisions_by_ids_function(
        pool_conn, tables["divisions_table"], "id", division_id
    )[0]
    division_data["teams"] = select_teams_by_ids_function(
        pool_conn, tables["teams_table"], "division_id", division_id
    )
    response = {"divisions": [division_data]}
    if not response:
        return {
            "message": f"No such division exists with id: {division_id}",
            "id_sent": f"{division_id}",
        }
    else:
        return response
