import codecs
from random import randint
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from blankiety_galantow.models.room import Room


router = APIRouter()

rooms_mockup = [
    Room("Alpha", 1, 1, 6, True, [], {}, [], []),
    Room("Beta", 2, 3, 6, False, [], {}, [], []),
    Room("Charlie", 3, 6, 6, True, [], {}, [], [])
    ]



@router.get("/", response_class=HTMLResponse)
async def root():
    return codecs.open("resources/index.html", "r", "utf-8").read()

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