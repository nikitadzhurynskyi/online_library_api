import csv
import io

from fastapi import HTTPException
from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.book.model import Book, Author, Genre
from src.book.schema import UpdateBookSchema, CreateBookSchema
from src.user.service import get_user_by_id

NOT_FOUND = "Book not found."


async def create_book(dto: CreateBookSchema, db: AsyncSession) -> Book:
    book = Book(title=dto.title, description=dto.description)
    for author in dto.authors:
        name, surname = author.split(maxsplit=1)
        query = select(Author).where(Author.name == name, Author.surname == surname)
        result = await db.execute(query)
        author = result.scalar_one_or_none()
        if author:
            book.authors.append(author)
        else:
            book.authors.append(Author(name=name, surname=surname))

    for genre_name in dto.genres:
        query = select(Genre).where(Genre.name == genre_name)
        result = await db.execute(query)
        genre = result.scalar_one_or_none()
        if genre:
            book.genres.append(genre)
        else:
            book.genres.append(Genre(name=genre_name))

    db.add(book)
    await db.commit()
    return book


async def get_all_books(limit: int, offset: int, db: AsyncSession) -> Sequence[Book]:
    query = select(Book).offset(offset).limit(limit).options(
        selectinload(Book.authors), selectinload(Book.genres)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def get_books_by_title(title: str, db: AsyncSession) -> Sequence[Book]:
    query = select(Book).where(Book.title.ilike(f"%{title}%")).options(
        selectinload(Book.authors), selectinload(Book.genres)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def get_book_by_id(book_id: int, db: AsyncSession) -> Book:
    query = select(Book).where(Book.id == book_id).options(
        selectinload(Book.authors), selectinload(Book.genres)
    )
    result = await db.execute(query)
    book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return book


async def get_favorite_books_by_user_id(user_id: int, db: AsyncSession) -> Sequence[Book]:
    user = await get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user.favorite_books


async def add_book_to_favorite(user_id: int, book_id: int, db: AsyncSession) -> Book:
    user = await get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    book = await get_book_by_id(book_id, db)
    if book is None:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    user.favorite_books.append(book)
    await db.commit()
    return book


async def remove_book_from_favorite(user_id: int, book_id: int, db: AsyncSession) -> Book:
    try:
        user = await get_user_by_id(user_id, db)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found.")
        book = await get_book_by_id(book_id, db)
        if book is None:
            raise HTTPException(status_code=404, detail=NOT_FOUND)
        user.favorite_books.remove(book)
    except ValueError:
        raise HTTPException(status_code=404, detail="Book is not in your favorite list.")
    await db.commit()
    return book


async def delete_book(book_id: int, db: AsyncSession) -> None:
    book = await get_book_by_id(book_id, db)
    await db.delete(book)
    await db.commit()


async def update_book(book_id: int, dto: UpdateBookSchema, db: AsyncSession) -> Book:
    book = await get_book_by_id(book_id, db)
    if book is None:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    update_data = dto.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in update_data.items():
        setattr(book, key, value)

    await db.commit()
    await db.refresh(book)
    return book


async def load_books_to_csv(db: AsyncSession):
    query = select(Book).options(selectinload(Book.authors), selectinload(Book.genres))
    result = await db.execute(query)
    books = result.scalars().all()

    output = io.StringIO()
    writer = csv.writer(output, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['ID', 'Title', 'Description', 'Authors', 'Genres'])
    for book in books:
        authors_str = ", ".join([f"{a.name} {getattr(a, 'surname', '')}".strip() for a in book.authors])
        genres_str = ", ".join([g.name for g in book.genres])

        writer.writerow([
            book.id,
            book.title,
            book.description or "",
            authors_str,
            genres_str
        ])
    return output.getvalue()
