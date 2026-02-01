from fastapi import HTTPException
from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from src.book.model import Book
from src.book.schema import BookSchema, UpdateBookSchema

NOT_FOUND = "Book not found."

async def create_book(dto: BookSchema, db: AsyncSession) -> Book:
    query = select(Book).where(Book.title == dto.title)
    result = await db.execute(query)
    if result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail=NOT_FOUND)

    book = Book(**dto.model_dump())
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book

async def get_all_books(limit: int, offset: int, db: AsyncSession) -> Sequence[Book]:
    query = select(Book).offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def get_books_by_title(title: str, db: AsyncSession) -> Sequence[Book]:
    query = select(Book).where(Book.title.ilike(f"%{title}%"))
    result = await db.execute(query)
    return result.scalars().all()

async def get_book_by_id(book_id: int, db: AsyncSession) -> Book:
    query = select(Book).where(Book.id == book_id)
    result = await db.execute(query)
    if result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    return result.scalar()

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

