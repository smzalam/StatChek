from functools import lru_cache
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class AuthSettings(BaseServiceSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env.auth"


class AuthVariables(BaseModel):
    secret_key: str = AuthSettings().secret_key
    algorithm: str = AuthSettings().algorithm
    access_token_expire_minutes: int = AuthSettings().access_token_expire_minutes


@lru_cache
def get_auth_settings():
    return AuthVariables()
