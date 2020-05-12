from typing import Dict
from starlette.websockets import WebSocketDisconnect

from .player import Player


class Room:
    """Single room that manages players inside and game state."""
    def __init__(self):
        self.players = []

    async def add_player_and_listen(self, player: Player):
        """Add new player to the room and start listening."""
        self.players.append(player)
        await self.send_chat_log(f"Gracz '{player.name}' dołączył do pokoju.")
        await self.listen_to_player(player)

    async def listen_to_player(self, player):
        """Constantly listen to player and take actions based on messages"""
        try:
            while True:
                msg = await player.receive_json()
                await self.process_message(player, msg)
        except WebSocketDisconnect:
            self.players.remove(player)
            await self.send_chat_log(f"Gracz '{player.name}' opuścił pokój.")

    async def process_message(self, player: Player, data: Dict):
        """Process raw JSON message (data) from player."""
        if "type" not in data:
            print(f"Received incorrect message: '{data}'")
            return
        if data["type"] == "ERROR" and "message" in data:
            print(f"ERROR: {data['message']}")
        if data["type"] == "CHAT_MESSAGE" and "message" in data:
            await self.send_chat_message(player.name, data["message"])

        # TODO: other types of messages

    async def send_chat_message(self, sender_name: str, msg: str):
        """Send message to all players in this room."""
        for player in self.players:
            data = {
                "log": False,
                "user": sender_name,
                "message": msg
            }
            await player.send_json(data)

    async def send_chat_log(self, msg: str):
        """Send chat log from the game to all players."""
        for player in self.players:
            data = {
                "log": True,
                "user": "Gra",
                "message": msg
            }
            await player.send_json(data)