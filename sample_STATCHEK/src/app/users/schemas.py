from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

"""USER SCHEMAS"""


class UserCreate(BaseModel):
    user_id: str | None = None
    email: EmailStr
    password: str


class UserRequest(BaseModel):
    user_id: str
    email: EmailStr
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    users: list[UserRequest]


"""
TOKEN SCHEMAS
"""


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str
