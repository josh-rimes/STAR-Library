from typing import Optional
from sqlmodel import SQLModel, Field


class Author(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    bio: Optional[str] = None


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    summary: Optional[str] = None
    published_year: Optional[int] = None
    author_id: Optional[int] = Field(default=None, foreign_key="author.id")


class Reader(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: Optional[str] = None


class BookReader(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="book.id")
    reader_id: int = Field(foreign_key="reader.id")
    notes: Optional[str] = None
