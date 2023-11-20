import uuid
from fastapi import status
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from src.app.config import get_auth_settings
from src.app.users import schemas as schemas

auth_settings = get_auth_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
