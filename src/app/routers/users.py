from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, status
from pydantic import EmailStr
from pprint import pprint
from .db_api_mediation_functions import *
from .database.db_connect import get_pool
from .schemas import *
from .utils import *
from .oauth2 import *


router = APIRouter()
pool_conn = get_pool()


@router.get("/users/new", status_code=status.HTTP_201_CREATED, response_model=User)
def new_user(user: UserCreate):
    metadata = {"table": "users"}
    # generating random user_id
    user.user_id = generate_random_user_id()
    # hashing password
    user.password = hash(user.password)
    # creating user
    user_data = insert_users_new_function(
        pool_conn, metadata["table"], [user.user_id, user.email, user.password]
    )
    response = {"users": user_data}
    return response


@router.post("/users/login")
def login(user_credentials: UserLogin):
    metadata = {"table": "users", "id_type": "email"}

    user_data = select_user_details_id_function(
        pool_conn, metadata["table"], metadata["id_type"], user_credentials.email
    )

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    else:
        user_data = user_data[0]
        if not verify(user_credentials.password, user_data["password"]):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
            )
        else:
            access_token = create_access_token(data={"user_id": user_data["user_id"]})
            return {"token": access_token, "token_type": "bearer"}


@router.get("/users/{user_email}", status_code=status.HTTP_200_OK, response_model=User)
def current_user(user_email: EmailStr):
    metadata = {"table": "users", "id_type": "email"}
    user_data = select_user_details_id_function(
        pool_conn, metadata["table"], metadata["id_type"], user_email
    )
    response = {"users": user_data}
    return response
