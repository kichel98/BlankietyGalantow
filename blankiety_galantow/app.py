import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


def run():
    uvicorn.run(app, host="localhost", port=80)
