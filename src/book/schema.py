from pydantic import BaseModel, ConfigDict


class BookSchema(BaseModel):
    title: str
    description: str | None = None
    authors: list[str]
    genres: list[str]


class CreateBookSchema(BookSchema):
    pass


class UpdateBookSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    authors: list[str] | None = None
    genres: list[str] | None = None


class BookResponse(BookSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class FavoriteBooksSchema(BaseModel):
    user_id: int
    books: list[BookSchema]
