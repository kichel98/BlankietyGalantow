import codecs
from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse

import blankiety_galantow.app as app
from .core.player import Player

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root():
    return codecs.open("resources/index.html", "r", "utf-8").read()


@router.get("/game/{game_id}")
async def connect_to_game(game_id):
    f = codecs.open('resources/game/index.html', 'r', 'utf-8')
    return HTMLResponse(f.read())


@router.websocket("/connect/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, username: str):
    await websocket.accept()

    if app.server.room_exists(room_id):
        player = Player(websocket, username)
        await app.server.add_player(room_id, player)
    else:
        print(f"Connection to nonexistent room id = {room_id}")
        await websocket.send_json({
            "type": "ERROR",
            "error": "Invalid server id"
        })
        await websocket.close(code=1000)
