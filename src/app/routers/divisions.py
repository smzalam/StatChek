from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .db_api_mediation_functions import *
from .database.db_connect import get_pool
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
        )
        teams_data = select_teams_by_ids_function(
            pool_conn, tables["teams_table"], "division_id", division_id
        )
        response.append(
            {
                "divisions": division_data,
                "teams": teams_data,
            }
        )
    return response


@router.get("/divisions")
def divisions_data(all: bool = False):
    if not all:
        table = "divisions"
        response = select_all_function(pool_conn, table)
        return response
    else:
        division_ids = [15, 16, 17, 18]
        response = get_all_divisons_data(division_ids)
        if not response:
            return {
                "message": f"No such division exists with id: {division_ids}",
                "ids_sent": f"{division_ids}",
            }
        else:
            return response


@router.get("/divisions/{division_id}")
def divisions_data_id(division_id: int, all: bool = False):
    if not all:
        table = "divisions"
        response = select_divisions_by_ids_function(pool_conn, table, "id", division_id)
        if not response:
            return {
                "message": f"No such division exists with id: {division_id}",
                "id_sent": f"{division_id}",
            }
        else:
            return response
    else:
        response = get_all_divisons_data([division_id])
        return response


@router.get("/divisions/{division_id}/teams")
def division_id_teams_data(division_id):
    tables = {"divisions_table": "divisions", "teams_table": "teams_info"}
    division_data = select_divisions_by_ids_function(
        pool_conn, tables["divisions_table"], "id", division_id
    )
    teams_data = select_teams_by_ids_function(
        pool_conn, tables["teams_table"], "division_id", division_id
    )
    response = {"division": division_data, "teams": teams_data}
    if not response:
        return {
            "message": f"No such division exists with id: {division_id}",
            "id_sent": f"{division_id}",
        }
    else:
        return response
