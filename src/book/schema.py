from pydantic import BaseModel, ConfigDict, field_validator


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

    @field_validator("authors", mode="before")
    @classmethod
    def convert_authors_to_strings(cls, v):
        if not v:
            return []
        result = []
        for author in v:
            full_name = author.name
            if hasattr(author, "surname") and author.surname:
                full_name += f" {author.surname}"
            result.append(full_name)

        return result

    @field_validator("genres", mode="before")
    @classmethod
    def convert_genres_to_strings(cls, v):
        if not v:
            return []
        return [genre.name for genre in v]


class FavoriteBooksSchema(BaseModel):
    user_id: int
    books: list[BookSchema]
