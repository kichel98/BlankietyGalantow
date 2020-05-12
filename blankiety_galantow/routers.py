import codecs
from fastapi import APIRouter, WebSocket
from random import randint
from fastapi.responses import HTMLResponse
from blankiety_galantow.models.room import Room

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

@router.get("/api/rooms")
async def rooms():
    rooms_dict = {i: vars(Room("room" + str(i), i, "addr" + str(i), randint(0, i), randint(0, i), [], {}, [], [])) for i in range(10)}
    return {"rooms": rooms_dict}