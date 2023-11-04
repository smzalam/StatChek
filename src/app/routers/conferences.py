from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .db_api_mediation_functions import *
from .database.db_connect import get_pool
from pprint import pprint
import json


router = APIRouter()
pool_conn = get_pool()


@router.get("/conferences")
def get_conferences_data():
    table = "teams_info"
    response = select_all_function(pool_conn, table)
    return response


# @router.get("/conferences/{conference_id}")
# @router.get("/conferences/{conference_id}/divisions")
# @router.get("/conferences/{conference_id}/teams")
