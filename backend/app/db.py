import os
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

# create_engine handles both postgres and sqlite URLs
engine = create_engine(DATABASE_URL, echo=False)


def init_db():
    try:
        SQLModel.metadata.create_all(engine)
    except OperationalError:
        # If DB isn't available, skip here. App will surface errors on requests.
        pass


def seed_data():
    """Seed the database with authors, books, readers and relationships if empty."""
    from .models import Author, Book, Reader, BookReader
    from sqlmodel import select

    with Session(engine) as session:
        # only seed if there are no authors
        authors_count = session.exec(select(Author)).first()
        if authors_count:
            return

        # create authors
        authors = [
            Author(name="Ada Lovelace", bio="Pioneer of computing."),
            Author(name="Isaac Asimov", bio="Science fiction writer."),
            Author(name="Ursula K. Le Guin", bio="Speculative fiction author."),
            Author(name="Octavia Butler", bio="Science fiction and fantasy author."),
        ]
        for a in authors:
            session.add(a)
        session.commit()

        # refresh to get ids
        for a in authors:
            session.refresh(a)

        # create books (15 total distributed)
        books = []
        books_data = [
            ("Notes on the Analytical Engine", "Early thoughts about computation", 1843, authors[0].id),
            ("I, Robot", "Robot short stories", 1950, authors[1].id),
            ("Foundation", "Galactic empire saga", 1951, authors[1].id),
            ("The Left Hand of Darkness", "Ambitious science fiction", 1969, authors[2].id),
            ("The Dispossessed", "Utopian/dystopian novel", 1974, authors[2].id),
            ("Kindred", "Time travel and history", 1979, authors[3].id),
            ("Parable of the Sower", "Dystopian novel", 1993, authors[3].id),
            ("AI: A Modern Approach", "Fictional placeholder book", 2000, authors[1].id),
            ("Computing Dreams", "Speculative essays", 2005, authors[0].id),
            ("Galactic Tales", "Collected sci-fi", 2010, authors[1].id),
            ("Strange Horizons", "Short speculative pieces", 2012, authors[2].id),
            ("Echoes", "A novel of ideas", 2015, authors[3].id),
            ("Machines and Musings", "Essays on machines", 2018, authors[0].id),
            ("New Foundations", "Sequel collection", 2020, authors[1].id),
            ("Last Light", "Final speculative story", 2022, authors[2].id),
        ]

        for title, summary, year, aid in books_data:
            b = Book(title=title, summary=summary, published_year=year, author_id=aid)
            session.add(b)
            books.append(b)
        session.commit()
        for b in books:
            session.refresh(b)

        # create readers
        readers = [
            Reader(name="Alice Reader", email="alice@example.com"),
            Reader(name="Bob Reader", email="bob@example.com"),
            Reader(name="Carol Reader", email="carol@example.com"),
            Reader(name="Dave Reader", email="dave@example.com"),
            Reader(name="Eve Reader", email="eve@example.com"),
        ]
        for r in readers:
            session.add(r)
        session.commit()
        for r in readers:
            session.refresh(r)

        # create relations: each reader reads several books
        relations = []
        pairs = [
            (0, [0,1,2,3]),
            (1, [1,4,5,6]),
            (2, [2,7,8,9,10]),
            (3, [3,11,12]),
            (4, [4,13,14]),
        ]
        for ridx, book_idxs in pairs:
            for bi in book_idxs:
                br = BookReader(book_id=books[bi].id, reader_id=readers[ridx].id)
                session.add(br)
                relations.append(br)
        session.commit()




def get_session():
    return Session(engine)
