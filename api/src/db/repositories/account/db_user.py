import uuid
from uuid import UUID
from sqlalchemy.orm.session import Session

from src.db.models.account import DbUser
from src.routers.account_administrator.schemas import UserBase


def create(db: Session, request: UserBase) -> DbUser:
    user = DbUser(
        id=uuid.uuid4(),
        username=request.username,
        displayName=request.displayName,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get(db: Session, id: UUID) -> DbUser:
    return db.query(DbUser).filter(DbUser.id == id).first()


def get_all(db: Session) -> list[DbUser]:
    users = db.query(DbUser).all()
    return users


def update(db: Session, id: UUID, request: UserBase) -> DbUser:
    user_query = db.query(DbUser).filter(DbUser.id == id)
    user_query.update({
        'username': request.username,
        'displayName': request.displayName,
    })
    db.commit()
    return user_query.first()


def delete(db: Session, id: UUID) -> DbUser:
    user = db.query(DbUser).filter(DbUser.id == id).first()
    db.delete(user)
    db.commit()
    return user
