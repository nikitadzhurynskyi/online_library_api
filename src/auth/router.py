from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.user.schema import UserCreateSchema, UserResponseSchema
from src.user.service import create_user

router = APIRouter(prefix="/api/auth", tags=["Authorization"])

@router.post("/register", status_code=201)
async def register_user(user_dto: UserCreateSchema, db: AsyncSession = Depends(get_db)) -> UserResponseSchema:
    user = await create_user(user_dto, db)
    return UserResponseSchema.model_validate(user, from_attributes=True)

