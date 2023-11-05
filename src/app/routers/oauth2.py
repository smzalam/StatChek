from jose import JWTError, jwt
from datetime import datetime, timedelta
from config import get_auth_settings


def create_access_token(data: dict):
    auth_settings = get_auth_settings()
    to_encode = data.copy()

    expire = datetime.now() + timedelta(
        minutes=auth_settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode, auth_settings.secret_key, algorithm=auth_settings.algorithm
    )

    return token
