from fastapi import APIRouter, HTTPException, status, Response
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.model import Token
from src.auth.security import create_access_token, create_refresh_token
from src.config import jwt_settings
from src.db.database import get_db
from src.user.schema import UserCreateSchema, UserResponseSchema
from src.user.service import create_user, authenticate_user

router = APIRouter(prefix="/api/auth", tags=["Authorization"])


@router.post("/register", status_code=201, response_model=UserResponseSchema)
async def register_user(user_dto: UserCreateSchema, db: AsyncSession = Depends(get_db)) -> UserResponseSchema:
    user = await create_user(user_dto, db)
    return UserResponseSchema.model_validate(user, from_attributes=True)

@router.post("/login", status_code=200, response_model=Token)
async def login_user(response: Response,
                     form_data: OAuth2PasswordRequestForm = Depends(),
                     db: AsyncSession = Depends(get_db)) -> Token:
    user = await authenticate_user(str(form_data.username), form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    payload = {
        "id": user.id,
        "role": user.role.value
    }

    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )
    return Token(access_token=access_token)