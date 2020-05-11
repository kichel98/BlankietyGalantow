import codecs
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from blankiety_galantow.models.server import Server


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root():
    return codecs.open("resources/index.html", "r", "utf-8").read()

@router.get("/servers")
async def servers():
    servers_dict = {i: vars(Server("server" + str(i), i, "addr" + str(i), randint(0, i), randint(0, i))) for i in range(10)}
    return {"servers": servers_dict}