from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get('/')
def root():
    return HTMLResponse('Api available at <a href="/docs">here</a>.', status.HTTP_200_OK, media_type='text/html')

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
