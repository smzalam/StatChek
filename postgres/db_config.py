from functools import lru_cache
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class DBSettings(BaseServiceSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str

    class Config:
        env_file = ".env"


class DBVariables(BaseModel):
    db_user: str = DBSettings().db_user
    db_password: str = DBSettings().db_password
    db_host: str = DBSettings().db_host
    db_port: str = DBSettings().db_port
    db_name: str = DBSettings().db_name


@lru_cache
def get_db_settings():
    return DBVariables()
