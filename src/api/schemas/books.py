from pydantic import BaseModel, Field
from typing import Optional


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    author_name: str = Field(min_length=1, max_length=255)
    genre: Optional[str] = Field(max_length=100)
    year: Optional[int] = Field(ge=0)


class BookCreate(BookBase):
    pass


class PartialBookUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    author_name: Optional[str] = Field(None, min_length=1, max_length=255)
    genre: Optional[str] = Field(None, max_length=100)
    year: Optional[int] = Field(None, ge=0)


class Book(BookBase):
    id: int
