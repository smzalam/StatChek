from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, status
from pydantic import EmailStr
from pprint import pprint
from .db_api_mediation_functions import *
from .database.db_connect import get_pool
from .schemas import *
from .utils import *


router = APIRouter()
pool_conn = get_pool()


@router.get("/users/new", status_code=status.HTTP_201_CREATED, response_model=User)
def new_user(user: UserCreate):
    table = "users"
    # generating random user_id
    user.user_id = generate_random_user_id()
    # hashing password
    user.password = hash(user.password)
    # creating user
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
