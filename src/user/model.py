import enum

from sqlalchemy import Integer, String, Enum, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.book.model import Book
from src.db.database import Base

user_books = Table(
    "user_books",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True))


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[String] = mapped_column(String, unique=True)
    password: Mapped[String] = mapped_column(String)
    favorite_books: Mapped[list["Book"]] = relationship("Book", secondary=user_books)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)
