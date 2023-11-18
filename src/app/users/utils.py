import uuid
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from src.app.config import get_auth_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


# generates random user id
def generate_random_user_id():
    random_id = str(uuid.uuid4())
    return random_id


# takes in password and returns hashed password
def hash(password: str):
    return pwd_context.hash(password)


# verifies a given password is the same as the hashed password in the database
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
