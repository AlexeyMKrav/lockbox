from uuid import UUID
from sqlalchemy.orm.session import Session

from src.db.models.account import DbUser
from src.routers.account_administrator.schemas import UserBase


def create(db: Session, request: UserBase):
    user = DbUser(
        username=request.username,
        displayName=request.displayName,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all(db: Session):
    return db.query(DbUser).all()


def delete(db: Session, id: UUID):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    db.delete(user)
    db.commit()
    return user
