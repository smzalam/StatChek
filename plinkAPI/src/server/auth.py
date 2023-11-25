from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta

from plinkAPI.src.config import config
from plinkAPI.src.routers.users import schemas as schemas

oath2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
auth_settings = config.get_auth_settings()


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=auth_settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode, auth_settings.secret_key, algorithm=auth_settings.algorithm
    )

    return token


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token=token,
            key=auth_settings.secret_key,
            algorithms=auth_settings.algorithm,
        )

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
    except JWTError as e:
        print(e)
        raise credentials_exception
    return token_data


def valid_current_user(token: str = Depends(oath2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_access_token(token, credentials_exception)
