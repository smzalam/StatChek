from functools import lru_cache
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pprint import pprint


class DBSettings(BaseModel):
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str


class AuthSettings(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class Settings(BaseSettings):
    db_config: DBSettings
    auth_config: AuthSettings

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"


@lru_cache
def get_db_settings():
    return Settings().db_config


@lru_cache
def get_auth_settings():
    return Settings().auth_config


# pprint(get_auth_settings().algorithm)
