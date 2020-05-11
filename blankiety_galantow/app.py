import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from blankiety_galantow.routers import router

from .classes.Server import Server

os.chdir(os.path.dirname(__file__))

# Creating FastApi instance and mounting static files
app = FastAPI()
app.mount("/css", StaticFiles(directory="resources/css"), name="css")
app.mount("/js", StaticFiles(directory="resources/js"), name="js")
app.mount("/vendor", StaticFiles(directory="resources/vendor"), name="vendor")
app.mount("/game/css", StaticFiles(directory="resources/game/css"), name="game/css")
app.mount("/game/js", StaticFiles(directory="resources/game/js"), name="game/js")
# Attaching router to app
app.include_router(router)

# Creating server object
server = Server()


# Starting server using uvicorn
def run():
    uvicorn.run(app, host="localhost", port=80)
