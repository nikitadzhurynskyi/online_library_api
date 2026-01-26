
from fastapi import HTTPException, status
from sqlalchemy import select, String
from sqlalchemy.ext.asyncio import AsyncSession

from src.user.schema import UserCreateSchema, UserResponseSchema
from src.user.model import User


async def create_user(user_dto: UserCreateSchema, db: AsyncSession) -> User:
    query = select(User).where(User.email == user_dto.email)
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User with this email already exists.")

    # hash password
    user_dict = user_dto.model_dump()
    user = User(**user_dict)

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_email(email: str, db: AsyncSession) -> User:
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user

async def get_user_by_id(user_id: int, db: AsyncSession) -> User:
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user