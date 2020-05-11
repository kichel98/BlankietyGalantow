import os

import uvicorn
import codecs
import json
from typing import List, Dict
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from blankiety_galantow.routers import router
from blankiety_galantow.connect_router import connect_router
# Importing classes
from .classes.User import User
from .classes.Server import Server

os.chdir(os.path.dirname(__file__))

# Creating FastApi instantion and mounting static files
app = FastAPI()
app.mount("/css", StaticFiles(directory="resources/css"), name="css")
app.mount("/js", StaticFiles(directory="resources/js"), name="js")
app.mount("/vendor", StaticFiles(directory="resources/vendor"), name="vendor")
app.mount("/game/css", StaticFiles(directory="resources/game/css"), name="game/css")
app.mount("/game/js", StaticFiles(directory="resources/game/js"), name="game/js")
# Attaching routers to app
app.include_router(router)
app.include_router(connect_router)

# Starting server using uvicorn
def run():
    uvicorn.run(app, host="localhost", port=80)

# Creating server object
server = Server()
