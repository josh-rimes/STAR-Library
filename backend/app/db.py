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


def get_session():
    return Session(engine)
