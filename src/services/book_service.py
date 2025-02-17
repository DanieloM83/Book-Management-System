import csv
import json
from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.books import BookCreate, PartialBookUpdateSchema
from db.database import get_db
from db.models import Book
from db.repositories.books import BookRepo


class BookService:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.repo = BookRepo(session)

    async def create_book(self, book_data: BookCreate) -> Book | None:
        return await self.repo.create_book(
            title=book_data.title,
            author_name=book_data.author_name,
            genre=book_data.genre,
            year=book_data.year
        )

    async def get_books(self, **filters) -> List[Book]:
        return await self.repo.get_books(**filters)

    async def get_book_by_id(self, book_id: int) -> Book | None:
        return await self.repo.get_book_by_id(book_id)

    async def get_book_by_title(self, title: str) -> Book | None:
        return await self.repo.get_book_by_title(title)

    async def update_book(self, book_id: int, book_data: PartialBookUpdateSchema) -> Book | None:
        return await self.repo.update_book(book_id, book_data)

    async def delete_book(self, book_id: int) -> bool:
        return await self.repo.delete_book(book_id)

    async def bulk_import_books(self, file_content: str, file_type: str) -> List[Book]:
        books = []
        if file_type == "csv":
            reader = csv.DictReader(file_content.splitlines())
            for row in reader:
                books.append(BookCreate(**row))
        elif file_type == "json":
            books_data = json.loads(file_content)
            books = [BookCreate(**book) for book in books_data]
        else:
            return []

        created_books = []
        for book in books:
            created_books.append(await self.create_book(book))
        return created_books
