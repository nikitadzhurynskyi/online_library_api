from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.db.database import Base

book_authors = Table('book_authors',
                     Base.metadata,
                     Column('author_id', Integer, ForeignKey('authors.id'), primary_key=True),
                     Column('book_id', Integer, ForeignKey('books.id'), primary_key=True))

book_genres = Table('book_genres',
                    Base.metadata,
                    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True),
                    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True))


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[String] = mapped_column(String, nullable=False, unique=False)
    description: Mapped[String] = mapped_column(String, nullable=False)
    authors: Mapped[list["Author"]] = relationship(secondary=book_authors, back_populates="books")
    genres: Mapped[list["Genre"]] = relationship(secondary=book_genres, back_populates="books")


class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[String] = mapped_column(String, nullable=False, unique=False)
    surname: Mapped[String] = mapped_column(String, nullable=False, unique=False)
    books: Mapped[list["Book"]] = relationship(secondary=book_authors, back_populates="authors")


class Genre(Base):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[String] = mapped_column(String, nullable=False, unique=True)
    books: Mapped[list["Book"]] = relationship(secondary=book_genres, back_populates="genres")
