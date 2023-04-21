from typing import Annotated

import uvicorn
from fastapi import FastAPI, status, Depends, Header, Form
from fastapi.responses import HTMLResponse

from src.authentication.auth import get_current_user
from src.db.database import engine
from src.db.models.account import Base
from src.db.repositories.account import db_certificate
from src.routers.account_administrator import user, certificate
from src.routers.account_administrator.schemas import UserDisplay
from src.routers.common import auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(certificate.router)


@app.get('/')
def root():
    return HTMLResponse('Api documentation available at <a href="/docs">here</a>.',
                        status.HTTP_200_OK,
                        media_type='text/html'
                        )


@app.get('/whoami')
def whoami(current_user: UserDisplay = Depends(get_current_user),
           certificate_id: Annotated[str | None, Header()] = None):
    return {
        'user': current_user,
        'certificate_id': certificate_id
    }


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
