import codecs
import json
from fastapi import APIRouter, FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import blankiety_galantow.app as app
from fastapi.staticfiles import StaticFiles
# Importing classes
from .classes.User import User
from .classes.Server import Server

connect_router = APIRouter()

@connect_router.get("/game/{game_id}")
async def connect_to_game(game_id):
    f = codecs.open('resources/game/index.html','r', 'utf-8')
    return HTMLResponse(f.read())


@connect_router.websocket("/connect/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: int, username: str):
    await websocket.accept()
    if game_id in app.server.tables:
        app.server.tables[game_id].append(User(username, websocket))
    else:
        app.server.tables[game_id] = [User(username, websocket)]
    while True:
        data = await websocket.receive_text()
        
        for user in app.server.tables[game_id]:
            message = {
                "user": username,
                "message": data
            }
            await user.socket.send_text(json.dumps(message))