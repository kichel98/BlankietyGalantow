import codecs
from random import randint
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from blankiety_galantow.models.room import Room


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root():
    return codecs.open("resources/index.html", "r", "utf-8").read()

@router.get("/api/rooms")
async def rooms():
    rooms_dict = {i: take(4, iteritems(vars(Room("server" + str(i), i, "addr" + str(i), randint(0, i), randint(0, i), [], {}, {})))) for i in range(10)}
    return {"rooms": rooms_dict}