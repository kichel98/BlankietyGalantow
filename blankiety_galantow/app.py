import uvicorn
import codecs
from typing import List, Dict
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

def run():
    uvicorn.run(app, host="localhost", port=8000)

app.mount("/vendor", StaticFiles(directory="./docs/prototype/vendor"), name="vendor")
app.mount("/js", StaticFiles(directory="./docs/prototype/servers-vue/js"), name="js")
app.mount("/css", StaticFiles(directory="./docs/prototype/servers-vue/css"), name="css")
app.mount("/game/js", StaticFiles(directory="./docs/prototype/game-vue/js"), name="game/js")
app.mount("/game/css", StaticFiles(directory="./docs/prototype/game-vue/css"), name="game/css")

class Server:
    def __init__(self):
        self.tables = {}
    tables: Dict[int, List[WebSocket]]

server = Server()

@app.get("/")
async def get():
    f = codecs.open('./docs/prototype/servers-vue/index.html','r', 'utf-8')
    return HTMLResponse(f.read())

@app.get("/game/{game_id}")
async def connect_to_game(game_id):
    f = codecs.open('./docs/prototype/game-vue/index.html','r', 'utf-8')
    return HTMLResponse(f.read())


@app.websocket("/connect/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: int):
    await websocket.accept()
    if game_id in server.tables:
        server.tables[game_id].append(websocket)
    else:
        server.tables[game_id] = [websocket]
    while True:
        data = await websocket.receive_text()
        for socket in server.tables[game_id]:
            await socket.send_text(f"[Game {game_id}] Message text was: {data}")
        