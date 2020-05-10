import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from blankiety_galantow.routers import router

os.chdir(os.path.dirname(__file__))

app = FastAPI()
app.mount("/css", StaticFiles(directory="resources/css"), name="css")
app.mount("/js", StaticFiles(directory="resources/js"), name="js")
app.mount("/vendor", StaticFiles(directory="resources/vendor"), name="vendor")
app.mount("/game", StaticFiles(directory="resources/game"), name="game")
app.include_router(router)


def run():
    uvicorn.run(app, host="localhost", port=80)
