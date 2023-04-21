import uuid
from uuid import UUID

from sqlalchemy.orm.session import Session

from src.authentication.hashing import Hash
from src.db.models.account import DbUser
from src.routers.account_administrator.schemas import UserBase


def create(db: Session, request: UserBase) -> DbUser:
    user = DbUser(
        id=uuid.uuid4(),
        username=request.username,
        displayName=request.displayName,
        password=Hash.get_password_hash(request.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get(db: Session, id: UUID) -> DbUser:
    return db.query(DbUser).filter(DbUser.id == id).first()


def get_by_username(db: Session, username: str) -> DbUser:
    return db.query(DbUser).filter(DbUser.username == username).first()


def get_authenticate_user(db: Session, username: str, password: str):
    user = get_by_username(db, username)
    if not user:
        return False
    if not Hash.verify_password(password, user.password):
        return False
    return user


def get_all(db: Session) -> list[DbUser]:
    users = db.query(DbUser).all()
    return users


def update(db: Session, id: UUID, request: UserBase) -> DbUser:
    user_query = db.query(DbUser).filter(DbUser.id == id)
    user_query.update({
        'username': request.username,
        'displayName': request.displayName,
        'password': Hash.get_password_hash(request.password)
    })
    db.commit()
    return user_query.first()


def delete(db: Session, id: UUID) -> DbUser:
    user = db.query(DbUser).filter(DbUser.id == id).first()
    db.delete(user)
    db.commit()
    return user
