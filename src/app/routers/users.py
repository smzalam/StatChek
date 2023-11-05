from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, status
from pydantic import EmailStr
from .db_api_mediation_functions import *
from .database.db_connect import get_pool
from .schemas import *
from pprint import pprint
import uuid


router = APIRouter()
pool_conn = get_pool()


@router.get("/users/new", status_code=status.HTTP_201_CREATED, response_model=User)
def new_user(user: UserCreate):
    table = "users"
    user.user_id = str(uuid.uuid4())
    user_data = insert_users_new_function(
        pool_conn, table, [user.user_id, user.email, user.password]
    )
    response = {"users": user_data}
    return response


@router.get("/users/{email}", status_code=status.HTTP_200_OK, response_model=User)
def current_user(email: EmailStr):
    table = "users"
    id_type = "email"
    user_data = select_user_details_id_function(pool_conn, table, id_type, email)
    response = {"users": user_data}
    return response
