from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

from src.config import DB_URL


class Base(DeclarativeBase):
    pass


engine = create_engine(DB_URL)
Session = sessionmaker(engine)


def get_db():
    with Session() as db:
        yield db
