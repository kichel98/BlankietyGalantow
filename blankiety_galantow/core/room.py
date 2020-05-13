from typing import Dict
from fastapi.websockets import WebSocketDisconnect

from .player import Player


class Room:
    """Single room that manages players inside and game state."""
    def __init__(self, name):
        self.name = name
        self.open = True
        self.number_of_seats = 6
        self.players = []

    @property
    def number_of_players(self):
        return len(self.players)

    async def add_player_and_listen(self, player: Player):
        """Add new player to the room and start listening."""
        self.players.append(player)
        await self.send_chat_message_from_system(f"Gracz '{player.name}' dołączył do pokoju.")
        await self.listen_to_player(player)

    async def listen_to_player(self, player):
        """Constantly listen to player and take actions based on messages"""
        try:
            while True:
                msg = await player.receive_json()
                await self.process_message(player, msg)
        except WebSocketDisconnect:
            self.players.remove(player)
            await self.send_chat_message_from_system(f"Gracz '{player.name}' opuścił pokój.")

    async def process_message(self, player: Player, data: Dict):
        """Process raw JSON message (data) from player."""
        if "type" not in data:
            print(f"Received incorrect message: '{data}'")
            return
        if data["type"] == "ERROR" and "message" in data:
            print(f"ERROR: {data['message']}")
        if data["type"] == "CHAT_MESSAGE" and "message" in data:
            await self.send_chat_message_from_user(player.name, data["message"])
        # TODO: other types of messages

    async def send_chat_message_from_user(self, sender_name: str, msg: str):
        """Send message from player to all players in this room."""
        await self.send_chat_message(sender=sender_name, message=msg)

    async def send_chat_message_from_system(self, msg: str):
        """Send chat message from the system to all players."""
        await self.send_chat_message(sender="Gra", message=msg, as_system=True)

    async def send_chat_message(self, sender, message, as_system=False):
        """Send chat message to all players."""
        for player in self.players:
            data = {
                "type": "CHAT_MESSAGE",
                "message": {
                    "log": as_system,
                    "user": sender,
                    "text": message
                }
            }
            await player.send_json(data)
