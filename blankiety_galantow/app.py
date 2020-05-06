import uvicorn
import codecs
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/vendor", StaticFiles(directory="../docs/prototype/vendor"), name="vendor")
app.mount("/js", StaticFiles(directory="../docs/prototype/servers-vue/js"), name="js")
app.mount("/css", StaticFiles(directory="../docs/prototype/servers-vue/css"), name="css")
app.mount("/game/js", StaticFiles(directory="../docs/prototype/game-vue/js"), name="game/js")
app.mount("/game/css", StaticFiles(directory="../docs/prototype/game-vue/css"), name="game/css")


@app.get("/")
async def get():
    f = codecs.open('../docs/prototype/servers-vue/index.html','r', 'utf-8')
    return HTMLResponse(f.read())

@app.get("/game/{game_id}")
async def connect_to_game(game_id):
    f = codecs.open('../docs/prototype/game-vue/index.html','r', 'utf-8')
    return HTMLResponse(f.read())


@app.websocket("/connect/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: int):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"[Game {game_id}] Message text was: {data}")