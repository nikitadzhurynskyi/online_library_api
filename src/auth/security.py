from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext

from src.auth.model import TokenType
from src.config import jwt_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(data: dict, token_type: TokenType) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)

    if token_type == TokenType.ACCESS:
        expires = now + timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        secret_key = jwt_settings.ACCESS_TOKEN_SECRET
        to_encode.update({"exp": expires})
        return jwt.encode(to_encode, secret_key, algorithm=jwt_settings.ALGORITHM)
    elif token_type == TokenType.REFRESH:
        expires = now + timedelta(days=jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS)
        secret_key = jwt_settings.REFRESH_TOKEN_SECRET
        to_encode.update({"exp": expires})
        return jwt.encode(to_encode, secret_key, algorithm=jwt_settings.ALGORITHM)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token type")

def create_access_token(data: dict) -> str:
    return create_jwt_token(data, TokenType.ACCESS)

def create_refresh_token(data: dict) -> str:
    return create_jwt_token(data, TokenType.REFRESH)