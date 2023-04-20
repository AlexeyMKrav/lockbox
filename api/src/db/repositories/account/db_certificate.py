import uuid
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from src.db.models.account import DbCertificate
from src.routers.account_administrator.schemas import CertificateBase


def create(db: Session, request: CertificateBase):
    certificate = DbCertificate(
        id=uuid.uuid4(),
        publicKey=request.publicKey,
        user_id=request.user.id
    )
    db.add(certificate)
    db.commit()
    db.refresh(certificate)
    return certificate


def get(db: Session, id: UUID):
    return db.query(DbCertificate).filter(DbCertificate.id == id).first()


def get_all(db: Session):
    return db.query(DbCertificate).all()


def get_users_certificates(db: Session, user_id):
    return db.query(DbCertificate).filter(DbCertificate.user_id == user_id).all()


def delete(db: Session, id: UUID):
    certificate = db.query(DbCertificate).filter(DbCertificate.id == id).first()
    if not certificate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with username {username} not found.')
    db.delete(certificate)
    db.commit()
    return certificate
