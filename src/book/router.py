from fastapi import APIRouter, Response
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_admin
from src.book.schema import UpdateBookSchema, BookResponse, CreateBookSchema
from src.book.service import create_book, get_books_by_title, get_all_books, get_book_by_id, update_book, delete_book
from src.db.database import get_db

router = APIRouter(prefix="/api/books", tags=["Books"])


@router.post("", response_model=BookResponse, dependencies=[Depends(get_current_admin)])
async def post_books(dto: CreateBookSchema,
                     db: AsyncSession = Depends(get_db)) -> BookResponse:
    return BookResponse.model_validate(await create_book(dto, db))


@router.get("/search", response_model=list[BookResponse])
async def search_books(title: str, db: AsyncSession = Depends(get_db)) -> list[BookResponse]:
    return [BookResponse.model_validate(book) for book in await get_books_by_title(title, db)]


@router.get("", response_model=list[BookResponse])
async def get_books(limit: int, offset: int, db: AsyncSession = Depends(get_db)) -> list[BookResponse]:
    return [BookResponse.model_validate(book) for book in await get_all_books(limit, offset, db)]


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)) -> BookResponse:
    return BookResponse.model_validate(await get_book_by_id(book_id, db))


@router.put("/{book_id}", response_model=BookResponse, dependencies=[Depends(get_current_admin)])
async def put_book(book_id: int, dto: UpdateBookSchema, db: AsyncSession = Depends(get_db)) -> BookResponse:
    return BookResponse.model_validate(await update_book(book_id, dto, db))


@router.delete("/{book_id}")
async def delete_book_by_id(book_id: int, db: AsyncSession = Depends(get_db)) -> Response:
    await delete_book(book_id, db)
    return Response(status_code=200)
