from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

class JWTSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ACCESS_TOKEN_SECRET: str
    REFRESH_TOKEN_EXPIRE_DAYS: int
    REFRESH_TOKEN_SECRET: str
    ALGORITHM: str = Field("HS256")

db_settings = DBSettings()
jwt_settings = JWTSettings()