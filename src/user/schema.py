from pydantic import BaseModel, EmailStr, ConfigDict

from src.user.model import UserRole


class UserSchema(BaseModel):
    email: EmailStr

class UserCreateSchema(UserSchema):
    password: str

class UserResponseSchema(UserSchema):
    id: int
    role: UserRole

    model_config = ConfigDict(from_attributes=True)