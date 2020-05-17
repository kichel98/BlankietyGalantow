import codecs

from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse

import blankiety_galantow.app as app
from .core.player import Player

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root():
    return codecs.open("resources/index.html", "r", "utf-8").read()


@router.get("/game/{game_id}", response_class=HTMLResponse)
async def connect_to_game(game_id):
    return codecs.open("resources/game/index.html", "r", "utf-8").read()


@router.websocket("/connect/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, username: str):
    await websocket.accept()

    if app.server.room_exists(room_id):
        player_id = app.server.generate_unique_player_id(room_id)
        player = Player(websocket, username, player_id)
        await app.server.add_player_to_room(room_id, player)
    else:
        print(f"Connection to nonexistent room id = {room_id}")
        await websocket.send_json({
            "type": "ERROR",
            "error": "Invalid server id"
        })
        await websocket.close(code=1000)


@router.get("/api/rooms")
async def rooms():
    room_list = app.server.get_room_list()
    return {"rooms": room_list}

@router.get("/api/create")
async def create_room(name: str, seats: int = 0):
    room_id = app.server.add_room(name, seats)
    return {"room_id": room_id}

