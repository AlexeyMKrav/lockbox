from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.params import Depends
from sqlalchemy.orm.session import Session

from src.authentication import auth_handler
from src.db.database import get_db
from src.db.repositories.account import db_user

router = APIRouter(
    tags=['authentication']
)


@router.post('/token')
def login(request: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = db_user.get_authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_handler.create_access_token(
        data={"sub": user.username},
    )
    return {
        'access_token': access_token,
        'token_type': 'bearer',
    }
