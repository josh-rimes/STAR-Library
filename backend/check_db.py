from app.db import engine
from app.models import Author, Book, Reader, BookReader
from sqlmodel import select, Session

with Session(engine) as s:
    authors = s.exec(select(Author)).all()
    books   = s.exec(select(Book)).all()
    readers = s.exec(select(Reader)).all()
    rels    = s.exec(select(BookReader)).all()

    print('Authors:', len(authors))
    print('Books:  ', len(books))
    print('Readers:', len(readers))
    print('Relations:', len(rels))

    # optionally print a sample:
    if authors:
        print('Sample author:', authors[0])
    if books:
        print('Sample book:', books[0])