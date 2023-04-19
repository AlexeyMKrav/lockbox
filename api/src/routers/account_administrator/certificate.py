from uuid import UUID
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from src.db.database import get_db
from src.db.repositories.account import db_certificate
from src.routers.account_administrator.schemas import CertificateBase

router = APIRouter(
    prefix='/account_admin/certificate',
    tags=['account administration']
)


@router.post('/')
def create(request: CertificateBase, db: Session = Depends(get_db)):
    return db_certificate.create(db, request)


@router.get('/{id}')
def get(id: UUID, db: Session = Depends(get_db)):
    return db_certificate.get(db, id)


@router.get('/all')
def get_all(db: Session = Depends(get_db)):
    return db_certificate.get_all(db)


@router.get('/all/user/{id}')
def get_users_certificates(id: UUID, db: Session = Depends(get_db)):
    return db_certificate.get_users_certificates(db, id)


@router.delete('/{id}')
def delete(id: UUID, db: Session = Depends(get_db)):
    db_certificate.delete(db, id)
