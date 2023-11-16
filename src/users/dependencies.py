from psycopg_pool import ConnectionPool
from fastapi import Depends
from pprint import pprint
from pydantic import EmailStr

import src.database.database as db
import src.database.db_service as db_funcs
import src.users.schemas as schemas
import src.users.constants as constants
import src.users.utils as utils


def valid_new_user(
    user: schemas.UserCreate,
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> schemas.User:
    # generating random user_id
    user.user_id = utils.generate_random_user_id()
    # hashing password
    user.password = utils.hash(user.password)
    # creating user
    user_data = db_funcs.insert_users_new_function(
        db_conn=pool_conn,
        db_table=constants.USERS_TABLE,
        user_details=[user.user_id, user.email, user.password],
        id_type=constants.USER_ID_TYPE,
    )

    return {"users": user_data}


def valid_user_login(
    user_credentials: schemas.UserLogin,
    pool_conn: ConnectionPool = Depends(db.get_pool),
):
    user_data = db_funcs.select_user_details_id_function(
        db_conn=pool_conn,
        db_table=constants.USERS_TABLE,
        id_type=constants.EMAIL_ID_TYPE,
        id_num=user_credentials.email,
    )

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    else:
        user_data = user_data[0]
        if not utils.verify(user_credentials.password, user_data["password"]):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
            )
        else:
            access_token = utils.create_access_token(
                data={"user_id": user_data["user_id"]}
            )
            return {"token": access_token, "token_type": "bearer"}


def valid_user_details(
    user_email: EmailStr,
    pool_conn: ConnectionPool = Depends(db.get_pool),
):
    user_data = db_funcs.select_user_details_id_function(
        db_conn=pool_conn,
        db_table=constants.USERS_TABLE,
        id_type=constants.EMAIL_ID_TYPE,
        id_num=user_email,
    )
    return {"users": user_data}


def valid_user_delete(
    user_email: EmailStr,
    pool_conn: ConnectionPool = Depends(db.get_pool),
):
    db_funcs.delete_user_function(
        db_conn=pool_conn,
        db_table=constants.USERS_TABLE,
        user_details=[user_email],
        id_type=constants.EMAIL_ID_TYPE,
    )
    user_data = db_funcs.select_user_details_id_function(
        db_conn=pool_conn,
        db_table=constants.USERS_TABLE,
        id_type=constants.EMAIL_ID_TYPE,
        id_num=user_email,
    )
    if not user_data:
        return {"message": f"Deleted user with email: {user_email} successfully!"}
    else:
        return {"message": f"Failed to delete user with email: {user_email}"}


print("No function to update user ids constant!")