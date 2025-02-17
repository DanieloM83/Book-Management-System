from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from db.models import Book


class BookRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_book_by_id(self, book_id: int) -> Book | None:
        result = await self.session.execute(
            text("SELECT * FROM books WHERE id = :id"),
            {"id": book_id}
        )
        row = result.fetchone()
        return row._mapping if row else None

    async def get_book_by_title(self, title: str) -> Book | None:
        result = await self.session.execute(
            text("SELECT * FROM books WHERE title ILIKE :title"),
            {"title": f"%{title}%"}
        )
        row = result.fetchone()
        return row._mapping if row else None

    async def get_books(self, size: int = 10, page: int = 1, sort_by: str = "", sort_by_asc: bool = True,
                        title: Optional[str] = None, author_name: Optional[str] = None, genre: Optional[str] = None,
                        year_min: Optional[int] = None, year_max: Optional[int] = None) -> list[Book]:
        query = "SELECT * FROM books WHERE 1=1"

        params = {}
        if title:
            query += " AND title ILIKE :title"
            params["title"] = f"%{title}%"
        if author_name:
            query += " AND author_name ILIKE :author_name"
            params["author_name"] = f"%{author_name}%"
        if genre:
            query += " AND genre ILIKE :genre"
            params["genre"] = f"%{genre}%"
        if year_min is not None:
            query += " AND year >= :year_min"
            params["year_min"] = year_min
        if year_max is not None:
            query += " AND year <= :year_max"
            params["year_max"] = year_max

        query += f" ORDER BY {sort_by} {"ASC" if sort_by_asc else "DESC"}"
        offset = (page - 1) * size
        query += " LIMIT :size OFFSET :offset"
        params["size"] = size
        params["offset"] = offset

        result = await self.session.execute(text(query), params)
        result = result.fetchall()
        return [Book(**row._mapping) for row in result]

    async def create_book(self, title: str, author_name: str, genre: str, year: int) -> Book | None:
        query1 = text("""
            INSERT INTO authors (name) 
            VALUES (:author_name)
            ON CONFLICT (name) DO NOTHING;
        """)
        await self.session.execute(query1, {"author_name": author_name})
        query2 = text("""
            INSERT INTO books (title, author_name, genre, year)
            VALUES (:title, :author_name, :genre, :year)
            RETURNING *;
        """)
        params = {"title": title, "author_name": author_name, "genre": genre, "year": year}
        result = await self.session.execute(query2, params)
        result = result.fetchone()
        await self.session.commit()
        return Book(**result._mapping) if result else None

    async def delete_book(self, book_id: int) -> bool:
        result = await self.session.execute(text("DELETE FROM books WHERE id = :id"), {"id": book_id})
        await self.session.commit()
        return result.rowcount > 0

    async def update_book(self, book_id: int, book_data) -> Book:
        update_data = {k: v for k, v in book_data.dict(exclude_unset=True).items()}
        if not update_data:
            return None
        set_clause = ", ".join(f"{key} = :{key}" for key in update_data.keys())
        update_data["id"] = book_id
        result = await self.session.execute(
            text(f"UPDATE books SET {set_clause} WHERE id = :id RETURNING *"),
            update_data
        )
        result = result.fetchone()
        if not result:
            return None
        return Book(**result._mapping)
