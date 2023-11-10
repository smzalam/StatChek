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
    Depends,
)
from .db_api_mediation_functions import *
from .database.db_connect import get_pool
from .schemas import *
from pprint import pprint
import json
from psycopg_pool import ConnectionPool


router = APIRouter()


def get_all_conference_data(conference_ids: list, pool_conn: ConnectionPool):
    metadata = {
        "conference_table": "conferences",
        "divisions_table": "divisions",
        "teams_table": "teams_info",
        "pool_conn": pool_conn,
        "id_type": "conference_id",
        "conference_ids": conference_ids,
    }
    response = []
    for conference_id in metadata["conference_ids"]:
        conference_data = select_conference_by_id_function(
            metadata["pool_conn"], metadata["conference_table"], conference_id
        )[0]
        conference_data["divisions"] = select_divisions_by_ids_function(
            metadata["pool_conn"],
            metadata["divisions_table"],
            metadata["id_type"],
            conference_id,
        )
        conference_data["teams"] = select_teams_by_ids_function(
            metadata["pool_conn"],
            metadata["teams_table"],
            metadata["id_type"],
            conference_id,
        )

        response.append(conference_data)
    return response


@router.get("/conferences", response_model=Conferences)
def conferences_data(
    pool_conn_init: ConnectionPool = Depends(get_pool), all: bool = False
):
    if not all:
        metadata = {"table": "conferences", "pool_conn": pool_conn_init}
        conference_data = select_all_function(metadata["pool_conn"], metadata["table"])
        if not conference_data:
            return {
                "message": "conference data not available",
                "data": conference_data,
            }
        response = {"conferences": conference_data}
        return response
    else:
        metadata = {
            "conference_ids": [5, 6],
            "pool_conn": pool_conn_init,
        }
        conference_data = get_all_conference_data(
            metadata["conference_ids"], metadata["pool_conn"]
        )
        if not conference_data:
            return {
                "message": f"No such conference exists with id: {conference_id}",
                "id_sent": f"{conference_id}",
            }
        response = {"conferences": conference_data}
        return response


@router.get("/conferences/{conference_id}", response_model=Conferences)
def conference_data_id(
    conference_id: Annotated[
        int,
        Path(title="the ID of the conference to get"),
    ],
    pool_conn_init: ConnectionPool = Depends(get_pool),
):
    metadata = {
        "table": "conferences",
        "pool_conn": pool_conn_init,
    }
    conference_data = select_conference_by_id_function(
        metadata["pool_conn"], metadata["table"], conference_id
    )
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
    ],
    pool_conn_init: ConnectionPool = Depends(get_pool),
):
    metadata = {
        "conference_table": "conferences",
        "division_table": "divisions",
        "pool_conn": pool_conn_init,
        "id_type": "conference_id",
    }
    conference_data = select_conference_by_id_function(
        metadata["pool_conn"], metadata["conference_table"], conference_id
    )[0]
    conference_data["divisions"] = select_divisions_by_ids_function(
        metadata["pool_conn"],
        metadata["division_table"],
        metadata["id_type"],
        conference_id,
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
    ],
    pool_conn_init: ConnectionPool = Depends(get_pool),
):
    metdata = {
        "conference_table": "conferences",
        "teams_table": "teams_info",
        "pool_conn": pool_conn_init,
        "id_type": "conference_id",
    }
    conference_data = select_conference_by_id_function(
        metdata["pool_conn"], metdata["conference_table"], conference_id
    )[0]
    conference_data["teams"] = select_teams_by_ids_function(
        metdata["pool_conn"], metdata["teams_table"], metdata["id_type"], conference_id
    )
    response = {"conferences": [conference_data]}
    if not response:
        return {
            "message": f"No such conference exists with id: {conference_id}",
            "id_sent": f"{conference_id}",
        }
    else:
        return response
