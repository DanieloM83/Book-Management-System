from database import Base


class User(Base):
    __tablename__ = "users"


class Book(Base):
    __tablename__ = "books"


class Author(Base):
    __tablename__ = "authors"

