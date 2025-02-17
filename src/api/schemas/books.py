from pydantic import BaseModel, Field, field_validator
from typing import Optional

from datetime import datetime
from enum import Enum


class GenreEnum(str, Enum):
    fiction = "Fiction"
    non_fiction = "Non-Fiction"
    science = "Science"
    history = "History"


class YearValidatorMixin(BaseModel):
    year: Optional[int] = None

    @field_validator("year")
    @classmethod
    def validate_year(cls, value: Optional[int]) -> Optional[int]:
        if value is None:
            return value
        current_year = datetime.utcnow().year
        if not (1800 <= value <= current_year):
            raise ValueError(f"Year must be between 1800 and {current_year}")
        return value


class GenreValidatorMixin(BaseModel):
    genre: Optional[GenreEnum] = None


class BookBase(YearValidatorMixin, GenreValidatorMixin):
    title: str = Field(min_length=1, max_length=255)
    author_name: str = Field(min_length=1, max_length=255)


class PartialBookUpdateSchema(YearValidatorMixin, GenreValidatorMixin):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    author_name: Optional[str] = Field(None, min_length=1, max_length=255)


class Book(BookBase):
    id: int


class BookCreate(BookBase):
    pass
