from functools import lru_cache
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    database_url: str
    test_database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file="./src/config/.env")


class DBSettings:
    db_user: str = Settings().db_user
    db_password: str = Settings().db_password
    db_host: str = Settings().db_host
    db_port: str = Settings().db_port
    db_name: str = Settings().db_name
    database_url: str = Settings().database_url
    test_database_url: str = Settings().test_database_url


class AuthSettings:
    secret_key: str = Settings().secret_key
    algorithm: str = Settings().algorithm
    access_token_expire_minutes: int = Settings().access_token_expire_minutes


@lru_cache
def get_db_settings():
    return DBSettings


@lru_cache
def get_auth_settings():
    return AuthSettings
