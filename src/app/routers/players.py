from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .db_api_mediation_functions import *
from .database.db_connect import get_pool
from pprint import pprint


router = APIRouter()
pool_conn = get_pool()

# @app.get("/players/{player_id}")
# @app.get("/players/search")
