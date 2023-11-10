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
from psycopg_pool import ConnectionPool


router = APIRouter()


def get_all_divisons_data(division_ids: list, pool_conn: ConnectionPool):
    metadata = {
        "divisions_table": "divisions",
        "teams_table": "teams_info",
        "pool_conn": pool_conn,
        "division_id_type": "id",
        "teams_id_type": "division_id",
    }
    response = []
    for division_id in division_ids:
        division_data = select_divisions_by_ids_function(
            metadata["pool_conn"],
            metadata["divisions_table"],
            metadata["division_id_type"],
            division_id,
        )[0]
        division_data["teams"] = select_teams_by_ids_function(
            metadata["pool_conn"],
            metadata["teams_table"],
            metadata["teams_id_type"],
            division_id,
        )
        response.append(division_data)
    return response


@router.get("/divisions", response_model=Divisions)
def divisions_data(
    pool_conn_init: ConnectionPool = Depends(get_pool), all: bool = False
):
    if not all:
        metadata = {"table": "divisions", "pool_conn": pool_conn_init}
        division_data = select_all_function(metadata["pool_conn"], metadata["table"])
        response = {"divisions": division_data}
        return response
    else:
        metadata = {"division_ids": [15, 16, 17, 18], "pool_conn": pool_conn_init}
        division_data = get_all_divisons_data(
            metadata["division_ids"], metadata["pool_conn"]
        )
        response = {"divisions": division_data}
        if not response:
            return {
                "message": f"No such division exists with id: {division_ids}",
                "ids_sent": f"{division_ids}",
            }
        else:
            return response


@router.get("/divisions/{division_id}", response_model=Divisions)
def divisions_data_id(
    division_id: int,
    pool_conn_init: ConnectionPool = Depends(get_pool),
    all: bool = False,
):
    if not all:
        metadata = {
            "table": "divisions",
            "pool_conn": pool_conn_init,
            "division_id_type": "id",
        }
        division_data = select_divisions_by_ids_function(
            metadata["pool_conn"],
            metadata["table"],
            metadata["division_id_type"],
            division_id,
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
        metadata = {"pool_conn": pool_conn_init}
        division_data = get_all_divisons_data([division_id], metadata["pool_conn"])
        response = {"divisions": division_data}
        return response


@router.get(
    "/divisions/{division_id}/teams", response_model=dict[str, list[TeamsRequest]]
)
def division_id_teams_data(
    division_id: int,
    pool_conn_init: ConnectionPool = Depends(get_pool),
):
    metadata = {
        "teams_table": "teams_info",
        "pool_conn": pool_conn_init,
        "teams_id_type": "division_id",
    }
    teams_data = select_teams_by_ids_function(
        metadata["pool_conn"],
        metadata["teams_table"],
        metadata["teams_id_type"],
        division_id,
    )
    response = {"teams": teams_data}
    if not response:
        return {
            "message": f"No such division exists with id: {division_id}",
            "id_sent": f"{division_id}",
        }
    else:
        return response
