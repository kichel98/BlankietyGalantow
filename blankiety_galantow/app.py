import uvicorn
from fastapi import FastAPI
from random import randint
from fastapi.staticfiles import StaticFiles
from blankiety_galantow.routers import router


class Server:
    def __init__(self, name: str, server_id: int, server_address: str, number_of_players: int, number_of_seats: int):
        self.name = name
        self.server_id = server_id
        self.server_address = server_address
        self.number_of_players = number_of_players
        self.number_of_seats = number_of_seats

    name: str
    server_id: int
    server_address: str
    number_of_players: int
    number_of_seats: int


app = FastAPI()

app.mount("/css", StaticFiles(directory="resources/css"), name="css")
app.mount("/js", StaticFiles(directory="resources/js"), name="js")
app.mount("/vendor", StaticFiles(directory="resources/vendor"), name="vendor")
app.mount("/game", StaticFiles(directory="resources/game"), name="game")
app.include_router(router)


@app.get("/servers")
async def servers():
    servers_dict = {i: vars(Server("server" + str(i), i, "addr" + str(i), randint(0, i), randint(0, i))) for i in range(10)}
    return {"servers": servers_dict}



def run():
    uvicorn.run(app, host="localhost", port=80)
