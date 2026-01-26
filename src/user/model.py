import enum

from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.db.database import Base


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[String] = mapped_column(String, unique=True)
    password: Mapped[String] = mapped_column(String)

    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)
