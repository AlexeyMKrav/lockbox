from uuid import UUID
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from src.db.database import get_db
from src.db.models.account import DbUser
from src.db.repositories.account import db_user
from src.routers.account_administrator.schemas import UserBase, UserDisplay

router = APIRouter(
    prefix='/account_admin/user',
    tags=['account administration']
)


@router.post('/')
def create(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create(db, request)


@router.get('/all', response_model=list[UserDisplay])
def get_all(db: Session = Depends(get_db)):
    users: list[DbUser] = db_user.get_all(db)
    return users


@router.get('/{id}', response_model=UserDisplay)
def get(id: UUID, db: Session = Depends(get_db)):
    return db_user.get(db, id)


@router.put('/{id}')
def update(id: UUID, request: 'UserBase', db: Session = Depends(get_db)):
    return db_user.update(db, id, request)


@router.delete('/{id}')
def delete(id: UUID, db: Session = Depends(get_db)):
    db_user.delete(db, id)
