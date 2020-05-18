import argparse
import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from blankiety_galantow.routers import router

from .core.server import Server

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

# Create mockup servers (TEMPORARY)
server.add_room("Alpha")
server.add_room("Beta")
server.add_room("Gamma")


# Starting server using uvicorn
def run():
    parser = argparse.ArgumentParser(prog="blankiety_galantow", description="Run the app")
    parser.add_argument("--port", default=80, type=int, help="Set port (default: 80)")
    parser.add_argument("--host", default="localhost", help="Set host (default: localhost)")
    parser.add_argument("--reload", default=False, type=bool, help="Enable auto reload (default: False)")
    parser.add_argument("--log-level", default="info", help="Set log level: [info|debug|...] (default: info)")

    args = vars(parser.parse_args())
    uvicorn.run("blankiety_galantow.app:app", **args)

