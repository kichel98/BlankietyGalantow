from json import JSONDecodeError
from fastapi import WebSocket
from fastapi.websockets import WebSocketDisconnect
from .kick_exception import KickException
from enum import Enum

class Player:
    def __init__(self, socket: WebSocket, username: str):
        self.name = username
        self.socket = socket
        self.id = None
        self.player_state = PlayerState.choosing

    def set_player_state(self, state: PlayerState):
        self.player_state = state

    @property
    def state(self):
        return self.state.name
        
    async def kick(self, reason: str):
        kick_reason = {
            "type": "KICK",
            "message": f"Zostałeś wyrzucony z pokoju. Powód: {reason}"
        }
        await self.send_json(kick_reason)
        await self.socket.close()
        raise KickException(f"Gracz '{self.name}'' został wyrzucony z pokoju. Powód: {reason}")

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

class PlayerState(Enum):
    master = 1
    choosing = 2
    ready = 3