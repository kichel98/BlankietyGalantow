import codecs
from fastapi import APIRouter, WebSocket
from random import randint
from fastapi.responses import HTMLResponse
from blankiety_galantow.models.room import Room

import blankiety_galantow.app as app
from .core.player import Player

router = APIRouter()

rooms_mockup = [
    Room("Alpha", 1, 1, 6, True, [], {}, [], []),
    Room("Beta", 2, 3, 6, False, [], {}, [], []),
    Room("Charlie", 3, 6, 6, True, [], {}, [], [])
    ]



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
    rooms_list = [{
        "id": room.id,
        "name": room.name,
        "players": room.number_of_players,
        "maxPlayers": room.number_of_seats,
        "open": room.open}
        for room in rooms_mockup]
    return {"rooms": rooms_list}