import random
from typing import Dict
from fastapi.websockets import WebSocketDisconnect
from fastapi.logger import logger

from .helpers import get_random_string
from .player import Player


class Room:
    """Single room that manages players inside and game state."""
    def __init__(self, name):
        self.name = name
        self.open = True
        self.number_of_seats = 6
        self.players = []
        self.admin = None

    @property
    def number_of_players(self):
        return len(self.players)

    async def add_player_and_listen(self, player: Player):
        """Add new player to the room and start listening."""
        player.id = self.generate_unique_player_id()
        self.players.append(player)

        if self.admin is None:
            self.admin = player
        await self.send_chat_message_from_system(f"Gracz '{player.name}' dołączył do pokoju.")
        await self.send_players_update()
        await self.listen_to_player(player)

    def generate_unique_player_id(self):
        player_id = get_random_string()
        players_id = [player.id for player in self.players]
        while player_id in players_id:
            player_id = get_random_string()
        return player_id

    async def listen_to_player(self, player):
        """Constantly listen to player and take actions based on messages"""
        try:
            while True:
                msg = await player.receive_json()
                await self.process_message(player, msg)
        except WebSocketDisconnect:
            self.players.remove(player)
            await self.handle_player_leaving(player)

    async def process_message(self, player: Player, data: Dict):
        """Process raw JSON message (data) from player."""
        if "type" not in data:
            logger.error(f"Received incorrect message: {data}")
            return
        if data["type"] == "ERROR" and "message" in data:
            logger.error(f"ERROR: {data}")
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
        data = {
            "type": "CHAT_MESSAGE",
            "message": {
                "log": as_system,
                "user": sender,
                "text": message
            }
        }
        await self.send_json_to_all_players(data)

    async def handle_player_leaving(self, player):
        """Does all needed operations after player leaves a room"""
        if player == self.admin:
            self.set_new_random_admin()
        await self.send_chat_message_from_system(f"Gracz '{player.name}' opuścił pokój.")
        await self.send_players_update()

    def set_new_random_admin(self):
        """Choose random player as admin"""
        if self.players:
            self.admin = random.choice(self.players)
        else:
            self.admin = None

    async def send_players_update(self):
        """Send info about players in room to all of them."""
        for player in self.players:
            players_info = self.get_players_info()
            # Add "me" field depending on player we send message to
            for player_info in players_info:
                if player_info["id"] == player.id:
                    player_info["me"] = True
            data = {
                "type": "PLAYERS",
                "players": players_info
            }
            await player.send_json(data)

    def get_players_info(self):
        """Get list of player info"""
        # TODO: Fill player info with correct state and score
        players_info = []
        for player in self.players:
            player_info = {
                "id": player.id,
                "name": player.name,
                "state": "ready",  # Needs to be changed
                "score": 0,  # Needs to be changed
                "admin": player == self.admin
            }
            players_info.append(player_info)
        return players_info

    async def send_json_to_all_players(self, json):
        """Send json (given as Python dictionary) to all players"""
        for player in self.players:
            await player.send_json(json)
