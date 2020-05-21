from json import JSONDecodeError
from fastapi import WebSocket
from fastapi.websockets import WebSocketDisconnect


class Player:
    def __init__(self, socket: WebSocket, username: str):
        self.name = username
        self.socket = socket
        self.id = None

    async def kick(self, message: str):
        kick_message = {
            "type": "KICK",
            "message": message
        }
        await self.send_json(kick_message)
        await self.socket.close()
        raise WebSocketDisconnect()

    async def receive_json(self):
        """Await for incoming message from the player."""
        try:
            data = await self.socket.receive_json()
        except JSONDecodeError:
            data = {
                "type": "ERROR",
                "message": "Incorrect JSON format"
            }
        return data

    async def send_json(self, data):
        """Send JSON data to the player via socket."""
        await self.socket.send_json(data)
