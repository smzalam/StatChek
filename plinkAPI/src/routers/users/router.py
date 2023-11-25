from pprint import pprint
import json

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
from psycopg_pool import ConnectionPool
from pydantic import EmailStr


from plinkAPI.src.routers.users import dependencies as dependencies
from plinkAPI.src.routers.users import schemas as schemas


router = APIRouter()


@router.post(
    "/users/new",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
)
def new_user(
    user: schemas.UserCreate,
    user_data: schemas.User = Depends(dependencies.valid_new_user),
):
    return user_data


@router.post("/users/login")
def login(
    user_credentials: schemas.UserLogin,
    user_data=Depends(dependencies.valid_user_login),
):
    return user_data


@router.get(
    "/users/{user_email}",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
)
def current_user(
    user_email: EmailStr,
    user_data=Depends(dependencies.valid_user_details),
):
    return user_data


@router.delete(
    "/users/delete/{user_email}",
    status_code=status.HTTP_200_OK,
)
def delete_user(
    user_email: EmailStr,
    user_data=Depends(dependencies.valid_user_delete),
):
    return user_data
