from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

from src.config import DB_URL


class Base(DeclarativeBase):
    pass


engine = create_engine(DB_URL)
# engine.connect().execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
Session = sessionmaker(engine)


def get_db():
    with Session() as db:
        yield db
