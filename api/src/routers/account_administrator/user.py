from uuid import UUID
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from src.db.database import get_db
from src.routers.account_administrator.schemas import UserBase

router = APIRouter(
    prefix='/account_admin',
    tags=['account administration']
)


@router.post('/')
def create(request: UserBase, db: Session = Depends(get_db)):
    return db_account.create(db, request)


@router.get('/{id}')
def get(id: UUID, db: Session = Depends(get_db)):
    return db_account.get(db, id)


@router.get('/all')
def get_all(db: Session = Depends(get_db)):
    return db_account.get_all(db)


@router.put('/{id}')
def update(id: UUID, request: 'UserBase', db: Session = Depends(get_db)):
    return db_account.update(db, id, request)


@router.delete('/{id}')
def delete(id: UUID, db: Session = Depends(get_db)):
    db_account.delete(db, id)
