import enum

from pydantic import BaseModel


class TokenType(str, enum.Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str
