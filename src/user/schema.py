from pydantic import BaseModel, EmailStr, ConfigDict

from src.user.model import UserRole


class UserSchema(BaseModel):
    email: EmailStr


class UserCreateSchema(UserSchema):
    password: str


class UserResponseSchema(UserSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
    role: UserRole
