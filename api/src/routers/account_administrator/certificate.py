from uuid import UUID
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from src.db.database import get_db
from src.db.repositories.account import db_certificate
from src.routers.account_administrator.schemas import CertificateBase, CertificateDisplay

router = APIRouter(
    prefix='/account_admin/certificate',
    tags=['account administration']
)


@router.post('/', response_model=CertificateDisplay)
def create(request: CertificateBase, db: Session = Depends(get_db)):
    return db_certificate.create(db, request)


@router.get('/all', response_model=list[CertificateDisplay])
def get_all(db: Session = Depends(get_db)):
    return db_certificate.get_all(db)


@router.get('/{id}', response_model=CertificateDisplay)
def get(id: UUID, db: Session = Depends(get_db)):
    return db_certificate.get(db, id)


@router.get('/all/user/{id}', response_model=list[CertificateBase])
def get_users_certificates(id: UUID, db: Session = Depends(get_db)):
    return db_certificate.get_users_certificates(db, id)


@router.delete('/{id}', response_model=CertificateBase)
def delete(id: UUID, db: Session = Depends(get_db)):
    return db_certificate.delete(db, id)
