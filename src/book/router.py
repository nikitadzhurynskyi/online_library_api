from fastapi import APIRouter, Response
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_admin, get_current_user
from src.book.schema import BookResponse, FavoriteBooksSchema, CreateBookSchema, UpdateBookSchema
from src.book.service import get_favorite_books_by_user_id, add_book_to_favorite, create_book, update_book, delete_book, \
    get_book_by_id, get_all_books, get_books_by_title, remove_book_from_favorite
from src.db.database import get_db
from src.user.model import User

router = APIRouter(prefix="/api/books", tags=["Books"])


@router.post("", response_model=BookResponse, dependencies=[Depends(get_current_admin)])
async def post_books(dto: CreateBookSchema,
                     db: AsyncSession = Depends(get_db)) -> BookResponse:
    return BookResponse.model_validate(await create_book(dto, db))


@router.get("/search", response_model=list[BookResponse])
async def search_books(title: str, db: AsyncSession = Depends(get_db)) -> list[BookResponse]:
    return [BookResponse.model_validate(book) for book in await get_books_by_title(title, db)]


@router.post("/favorite", response_model=BookResponse)
async def post_favorite_book(book_id: int,
                             user: User = Depends(get_current_user),
                             db: AsyncSession = Depends(get_db)) -> BookResponse:
    book = await add_book_to_favorite(user.id, book_id, db)
    return BookResponse.model_validate(book)


@router.get("/favorites", response_model=FavoriteBooksSchema)
async def get_favorite_books(user: User = Depends(get_current_user),
                             db: AsyncSession = Depends(get_db)) -> FavoriteBooksSchema:
    books = await get_favorite_books_by_user_id(user.id, db)
    return FavoriteBooksSchema(user_id=user.id, book_ids=[book.id for book in books])


@router.delete("/favorite/{book_id}", response_model=BookResponse)
async def delete_favorite_book(book_id: int, user: User = Depends(get_current_user),
                               db: AsyncSession = Depends(get_db)) -> BookResponse:
    book = await remove_book_from_favorite(user.id, book_id, db)
    return BookResponse.model_validate(book)


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
