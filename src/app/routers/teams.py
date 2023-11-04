from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from db_api_mediation_functions import *
from database.db_connect import get_pool
from pprint import pprint


router = APIRouter()
pool_conn = get_pool()

@app.get("/teams")
@app.get("/teams/{team_id}")
@app.get("/teams/{team_id}/players")
@app.get("/teams/{team_id}/roster")
@app.get("/teams/{team_id}/stats")
@app.get("/teams/{team_id}/ranks")
@app.get("/teams/{team_id}/links")
@app.get("/teams/{team_id}/schedule")
@app.get("/teams/{team_id}/history")
