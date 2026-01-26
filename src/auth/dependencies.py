from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import jwt_settings
from src.db.database import get_db
from src.user.model import User, UserRole
from src.user.service import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            jwt_settings.ACCESS_TOKEN_SECRET,
            algorithms=[jwt_settings.ALGORITHM]
        )

        user_id: int = payload.get("id")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = await get_user_by_id(user_id, db)

    if user is None:
        raise credentials_exception

    return user


async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges"
        )
    return current_user
