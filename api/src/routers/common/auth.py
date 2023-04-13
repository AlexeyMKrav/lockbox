from fastapi import APIRouter, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from src.db.database import get_db
from src.db.models.account import DbUser

router = APIRouter(
    tags=['authentication']
)


@router.get('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(DbUser).first(DbUser.username == request.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    return {
        'access_token': 'access_token_test',
        'token_tipe': 'bearer',
        'user_id': user.id,
        'username': user.username
    }
