import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse

from src.db.models.account import Base, DbUser
from src.db.database import engine
from src.routers.common import auth
from src.routers.account_administrator import user

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)


@app.get('/')
def root():
    return HTMLResponse('Api documentation available at <a href="/docs">here</a>.',
                        status.HTTP_200_OK,
                        media_type='text/html'
                        )


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
