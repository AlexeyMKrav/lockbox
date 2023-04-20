import secrets
from datetime import datetime, timedelta
from typing import Optional, Annotated
from uuid import UUID

from fastapi import HTTPException, Depends, status
from fastapi.security import APIKeyQuery
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.db.repositories.account import db_certificate

auth_scheme = APIKeyQuery(name='certificate_id')

SECRET_KEY = secrets.token_hex(32)
print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + SECRET_KEY)
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(auth_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        certificate_id: UUID = payload.get("sub")
        if certificate_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db_certificate.get(db, certificate_id).user
    if user is None:
        raise credentials_exception
    return user
