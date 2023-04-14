from fastapi import APIRouter, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm, OAuth2PasswordRequestFormStrict
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from src.db.database import get_db
from src.routers.account_administrator.schemas import UserBase
from src.db.repositories import db_account

router = APIRouter(
    prefix='/account_admin',
    tags=['account administration']
)


@router.post('/')
def create(request: UserBase, db: Session = Depends(get_db)):
    return db_account.create(db, request)


@router.get('/{id}')
def get(id: int, db: Session = Depends(get_db)):
    pass


@router.get('/all')
def get_all(db: Session = Depends(get_db)):
    pass


@router.put('/{id}')
def update(id: int, request: 'UserBase', db: Session = Depends(get_db)):
    pass


@router.delete('/{id}')
def delete(id: int, db: Session = Depends(get_db)):
    pass
