from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, status
from .db_api_mediation_functions import *
from .database.db_connect import get_pool
from .schemas import *
from pprint import pprint
import uuid


router = APIRouter()
pool_conn = get_pool()


@router.get("/users/new", status_code=status.HTTP_201_CREATED)
def new_user(user: UserCreate):
    user_id = str(uuid.uuid4())
    x = insert_users_new_function(pool_conn, [user_id, user.email, user.password])
    return {x}
