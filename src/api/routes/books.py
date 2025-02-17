from fastapi import APIRouter, Depends, UploadFile, File, Query

from api.exceptions.books import BookNameConflictError, BookNotFoundError
from services.book_service import BookService
from api.schemas.books import BookCreate, PartialBookUpdateSchema, Book
from typing import List, Optional

book_router = APIRouter(prefix="/books", tags=["books"])


@book_router.post("/")
async def create_book(book_data: BookCreate, book_service: BookService = Depends(BookService)) -> Book:
    book = await book_service.create_book(book_data)
    if book is None:
        raise BookNameConflictError()
    return book


@book_router.get("/")
async def get_books(
        size: int = Query(10, ge=1),
        page: int = Query(1, ge=1),
        sort_by: str = Query("title", enum=["title", "year", "author_name"]),
        sort_order: str = Query("asc", enum=["asc", "desc"]),
        title: Optional[str] = None,
        author_name: Optional[str] = None,
        genre: Optional[str] = None,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        book_service: BookService = Depends(BookService)
) -> List[Book]:
    return await book_service.get_books(
        size=size, page=page, sort_by=sort_by, sort_by_asc=(sort_order == "asc"),
        title=title, author_name=author_name, genre=genre, year_min=year_min, year_max=year_max
    )


@book_router.get("/{book_id}")
async def get_book_by_id(book_id: int, book_service: BookService = Depends(BookService)) -> Book:
    book = await book_service.get_book_by_id(book_id)
    if book is None:
        raise BookNotFoundError()
    return book


@book_router.patch("/{book_id}")
async def update_book(book_id: int, book_data: PartialBookUpdateSchema,
                      book_service: BookService = Depends(BookService)) -> Book:
    book = await book_service.update_book(book_id, book_data)
    if book is None:
        raise BookNotFoundError()
    return book


@book_router.delete("/{book_id}")
async def delete_book(book_id: int, book_service: BookService = Depends(BookService)) -> bool:
    return await book_service.delete_book(book_id)


@book_router.post("/import")
async def bulk_import_books(file: UploadFile = File(...), book_service: BookService = Depends(BookService)):
    content = await file.read()
    file_type = file.filename.split(".")[-1]
    return await book_service.bulk_import_books(content.decode(), file_type)
