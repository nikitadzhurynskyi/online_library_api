from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.db.database import Base

book_authors = Table('book_authors',
                     Base.metadata,
                     Column('author_id',
                            Integer,
                            ForeignKey('authors.id', ondelete="CASCADE"),
                            primary_key=True),
                     Column('book_id',
                            Integer,
                            ForeignKey('books.id', ondelete="CASCADE"),
                            primary_key=True))

book_genres = Table('book_genres',
                    Base.metadata,
                    Column('genre_id',
                           Integer,
                           ForeignKey('genres.id', ondelete="CASCADE"),
                           primary_key=True),
                    Column('book_id',
                           Integer,
                           ForeignKey('books.id', ondelete="CASCADE"),
                           primary_key=True))


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False, unique=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    authors: Mapped[list["Author"]] = relationship(secondary=book_authors, back_populates="books",
                                                   passive_deletes=True)
    genres: Mapped[list["Genre"]] = relationship(secondary=book_genres, back_populates="books",
                                                 passive_deletes=True)


class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=False)
    surname: Mapped[str] = mapped_column(String, nullable=False, unique=False)
    books: Mapped[list["Book"]] = relationship(secondary=book_authors, back_populates="authors", passive_deletes=True)

    @property
    def fullname(self):
        return f"{self.name} {self.surname}"


class Genre(Base):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    books: Mapped[list["Book"]] = relationship(secondary=book_genres, back_populates="genres", passive_deletes=True)
