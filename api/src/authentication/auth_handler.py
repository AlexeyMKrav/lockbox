import secrets
from datetime import datetime, timedelta
from typing import Annotated
from uuid import UUID

from fastapi import HTTPException, Depends, status, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.db.models.account import DbUser
from src.db.repositories.account import db_certificate, db_user

auth_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = secrets.token_hex(32)
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class AuthData:
    user: DbUser
    certificate_id: str | None = None

    def __init__(self, user: DbUser, certificate_id: str | None = None) -> None:
        super().__init__()
        self.user = user
        self.certificate_id = certificate_id


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_username_from_jwt(token: Annotated[str, Depends(auth_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: UUID = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username


def get_current_user(token: Annotated[str, Depends(auth_scheme)],
                     db: Annotated[Session, Depends(get_db)]) -> DbUser:
    username = get_username_from_jwt(token)
    user = db_user.get_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user


def get_current_auth(token: str = Depends(auth_scheme),
                     certificate_id: str = Header(),
                     db: Session = Depends(get_db)) -> AuthData:
    username = get_username_from_jwt(token)
    certificate = db_certificate.get(db, certificate_id)
    if certificate is None:
        raise credentials_exception
    if username != certificate.user.username:
        raise credentials_exception
    return AuthData(
        user=certificate.user,
        certificate_id=certificate.id
    )
