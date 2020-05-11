import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from blankiety_galantow.routers import router

os.chdir(os.path.dirname(__file__))

app = FastAPI()
app.mount("/css", StaticFiles(directory="resources/css"), name="css")
app.mount("/js", StaticFiles(directory="resources/js"), name="js")
app.mount("/vendor", StaticFiles(directory="resources/vendor"), name="vendor")
app.mount("/game", StaticFiles(directory="resources/game"), name="game")
app.include_router(router)

@app.get("/game/{game_id}")
async def connect_to_game(game_id):
    f = codecs.open('./docs/prototype/game-vue/index.html','r', 'utf-8')
    return HTMLResponse(f.read())


@app.websocket("/connect/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: int, username: str):
    await websocket.accept()
    if game_id in server.tables:
        server.tables[game_id].append(User(username, websocket))
    else:
        server.tables[game_id] = [User(username, websocket)]
    while True:
        data = await websocket.receive_text()
        
        for user in server.tables[game_id]:
            message = {
                "user": username,
                "message": data
            }
            await user.socket.send_text(json.dumps(message))
        