import asyncio

from sqlalchemy import String, ForeignKey, Integer, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base, engine


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[int] = mapped_column(String(), unique=True, nullable=False)
    genre: Mapped[str] = mapped_column(String())
    year: Mapped[int] = mapped_column(Integer())

    author_name: Mapped[str] = mapped_column(String(50), ForeignKey("authors.name"))
    author = relationship("Author", back_populates="books")


class Author(Base):
    __tablename__ = "authors"

    name: Mapped[str] = mapped_column(String(50), primary_key=True)
    books = relationship("Book", back_populates="author")
