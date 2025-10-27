from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .db import get_session, init_db, seed_data
from .models import Author, Book, Reader, BookReader
from sqlmodel import select

app = FastAPI(title="STAR Library API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()
    try:
        seed_data()
    except Exception:
        # seeding should not crash the server; surface errors via logs if needed
        pass


@app.get("/health")
def health():
    return {"status": "ok"}


# --- Authors CRUD ---


@app.post("/authors", response_model=Author)
def create_author(author: Author):
    with get_session() as session:
        session.add(author)
        session.commit()
        session.refresh(author)
        return author


@app.get("/authors")
def list_authors():
    with get_session() as session:
        authors = session.exec(select(Author)).all()
        return authors


@app.get("/authors/{author_id}")
def get_author(author_id: int):
    with get_session() as session:
        author = session.get(Author, author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return author


@app.put("/authors/{author_id}", response_model=Author)
def update_author(author_id: int, author: Author):
    with get_session() as session:
        db = session.get(Author, author_id)
        if not db:
            raise HTTPException(status_code=404, detail="Author not found")
        db.name = author.name
        db.bio = author.bio
        session.add(db)
        session.commit()
        session.refresh(db)
        return db


@app.delete("/authors/{author_id}")
def delete_author(author_id: int):
    with get_session() as session:
        author = session.get(Author, author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        session.delete(author)
        session.commit()
        return {"ok": True}


# --- Books CRUD ---


@app.post("/books", response_model=Book)
def create_book(book: Book):
    with get_session() as session:
        session.add(book)
        session.commit()
        session.refresh(book)
        return book


@app.get("/books")
def list_books():
    with get_session() as session:
        books = session.exec(select(Book)).all()
        return books


@app.get("/books/{book_id}")
def get_book(book_id: int):
    with get_session() as session:
        book = session.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book


@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: Book):
    with get_session() as session:
        db = session.get(Book, book_id)
        if not db:
            raise HTTPException(status_code=404, detail="Book not found")
        db.title = book.title
        db.summary = book.summary
        db.published_year = book.published_year
        db.author_id = book.author_id
        session.add(db)
        session.commit()
        session.refresh(db)
        return db


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    with get_session() as session:
        book = session.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        session.delete(book)
        session.commit()
        return {"ok": True}


# --- Readers CRUD ---


@app.post("/readers", response_model=Reader)
def create_reader(reader: Reader):
    with get_session() as session:
        session.add(reader)
        session.commit()
        session.refresh(reader)
        return reader


@app.get("/readers")
def list_readers():
    with get_session() as session:
        readers = session.exec(select(Reader)).all()
        return readers


@app.get("/readers/{reader_id}")
def get_reader(reader_id: int):
    with get_session() as session:
        reader = session.get(Reader, reader_id)
        if not reader:
            raise HTTPException(status_code=404, detail="Reader not found")
        return reader


@app.put("/readers/{reader_id}", response_model=Reader)
def update_reader(reader_id: int, reader: Reader):
    with get_session() as session:
        db = session.get(Reader, reader_id)
        if not db:
            raise HTTPException(status_code=404, detail="Reader not found")
        db.name = reader.name
        db.email = reader.email
        session.add(db)
        session.commit()
        session.refresh(db)
        return db


@app.delete("/readers/{reader_id}")
def delete_reader(reader_id: int):
    with get_session() as session:
        reader = session.get(Reader, reader_id)
        if not reader:
            raise HTTPException(status_code=404, detail="Reader not found")
        session.delete(reader)
        session.commit()
        return {"ok": True}


# --- BookReader (associations) CRUD ---


@app.post("/book-readers", response_model=BookReader)
def create_book_reader(rel: BookReader):
    with get_session() as session:
        session.add(rel)
        session.commit()
        session.refresh(rel)
        return rel


@app.get("/book-readers")
def list_book_readers():
    with get_session() as session:
        rels = session.exec(select(BookReader)).all()
        return rels


@app.get("/book-readers/{rel_id}")
def get_book_reader(rel_id: int):
    with get_session() as session:
        rel = session.get(BookReader, rel_id)
        if not rel:
            raise HTTPException(status_code=404, detail="Relation not found")
        return rel


@app.delete("/book-readers/{rel_id}")
def delete_book_reader(rel_id: int):
    with get_session() as session:
        rel = session.get(BookReader, rel_id)
        if not rel:
            raise HTTPException(status_code=404, detail="Relation not found")
        session.delete(rel)
        session.commit()
        return {"ok": True}


# --- Utility endpoints ---


@app.get("/authors/{author_id}/books")
def books_by_author(author_id: int):
    with get_session() as session:
        books = session.exec(select(Book).where(Book.author_id == author_id)).all()
        return books


@app.get("/books/{book_id}/readers")
def readers_for_book(book_id: int):
    with get_session() as session:
        rels = session.exec(select(BookReader).where(BookReader.book_id == book_id)).all()
        readers = [session.get(Reader, r.reader_id) for r in rels]
        return readers


@app.get("/readers/{reader_id}/books")
def books_for_reader(reader_id: int):
    with get_session() as session:
        rels = session.exec(select(BookReader).where(BookReader.reader_id == reader_id)).all()
        books = [session.get(Book, r.book_id) for r in rels]
        return books
