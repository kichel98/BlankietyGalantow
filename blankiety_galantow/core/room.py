import random

from typing import Dict
from fastapi.websockets import WebSocketDisconnect
from fastapi.logger import logger

from .chat import Chat
from .helpers import get_random_string
from .player import Player
from .game_master import GameMaster
from .room_settings import RoomSettings
from .utils.observable_list import ObservableList


class Room:
    """Single room that manages players inside and game state."""
    def __init__(self, name):
        self.players = ObservableList()
        self.chat = Chat(self.players)
        self.settings = RoomSettings(self.chat)
        self.game_master = GameMaster(self)
        self.settings.name = name
        self.admin = None

    @property
    def number_of_players(self):
        return len(self.players)

    @property
    def is_empty(self):
        return self.number_of_players == 0

    async def connect_new_player_and_listen(self, player: Player):
        """Add new player to the room and start listening."""
        if not self.settings.open:
            await player.kill("Pokój jest zamknięty.")
            logger.error(f"Player '{player}' tried to join a closed server '{self.settings.name}'")
            return

        is_room_full = self.number_of_players == self.settings.number_of_seats
        if is_room_full:
            await player.kill("Pokój jest pełny.")
            logger.error(f"Player '{player}' tried to join a full server '{self.settings.name}'")
            return

        if self.settings.password != "":
            await self.listen_to_waiting_player(player)
        else:
            await self.add_player_and_listen(player)

    async def listen_to_waiting_player(self, player: Player):
        try:
            message = {
                "type": "PASSWORD"
            }
            await player.send_json(message)
            player_valid = False
            while True:
                msg = await player.receive_json()
                if msg["type"] == "PASSWORD" and "password" in msg:
                    if msg["password"] == self.settings.password:
                        player_valid = True
                    break
            
            if player_valid:
                await self.add_player_and_listen(player)
            else:
                await player.kill("Nieprawidłowe hasło!")
        except WebSocketDisconnect:
            pass

    async def add_player_and_listen(self, player: Player):
        player.id = self.generate_unique_player_id()
        await self.players.append(player)

        if self.admin is None:
            self.admin = player
        await self.send_settings_to_players()
        await self.chat.send_message_from_system(f"Gracz '{player.name}' dołączył do pokoju.")
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
            await self.handle_player_leaving(player)

    async def process_message(self, player: Player, data: Dict):
        """Process raw JSON message (data) from player."""
        if "type" not in data:
            logger.error(f"Received incorrect message: {data}")
            return
        if data["type"] == "ERROR" and "message" in data:
            logger.error(f"ERROR: {data}")
        elif data["type"] == "SETTINGS" and "settings" in data and self.is_admin(player):
            await self.settings.update(player.name, data["settings"])
            await self.send_settings_to_players()
            if not self.game_master.is_timer_set():
                await self.game_master.timer_start()
        elif data["type"] == "CHAT_MESSAGE" and "message" in data:
            await self.chat.send_message_from_player(player, data["message"])
        else:
            # Handle game_master messages
            await self.game_master.process_message(player, data)

    async def handle_player_leaving(self, player):
        """Does all needed operations after player leaves a room"""
        if player in self.players:
            await self.players.remove(player)
            message = f"Gracz {player.name} opuścił pokój."
            await self.chat.send_message_from_system(message)
        if player == self.admin:
            self.set_new_random_admin()
        await self.send_players_update()

    async def kick_player(self, player: Player, reason: str):
        kick_reason = {
            "type": "KICK",
            "message": f"Zostałeś wyrzucony z pokoju. Powód: {reason}"
        }
        await player.send_json(kick_reason)
        msg = f"Gracz {player.name} został wyrzucony z pokoju. Powód: {reason}"
        await self.chat.send_message_from_system(msg)
        await self.players.remove(player)
        await player.socket.close()

    def set_new_random_admin(self):
        """Choose random player as admin"""
        if self.number_of_players > 0:
            self.admin = random.choice(self.players)
        else:
            self.admin = None

    async def send_settings_to_players(self):
        settings_data = {
            "type": "SETTINGS",
            "settings": {
                "roomName": self.settings.name,
                "open": self.settings.open,
                "time": self.settings.selecting_time,
                "customCards": self.settings.custom_cards,
                "gameType": self.settings.game_type,
                "password": "",
                "paused": self.settings.paused
            }
        }
        await self.send_json_to_all_players(settings_data)
        settings_data["settings"]["password"] = self.settings.password
        await self.admin.send_json(settings_data)

    def is_admin(self, player: Player):
        return self.admin == player

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
        players_info = []
        for player in self.players:
            player_info = {
                "id": player.id,
                "name": player.name,
                "state": player.state.name,
                "score": player.points,
                "admin": player == self.admin
            }
            players_info.append(player_info)
        return players_info

    async def send_json_to_all_players(self, json):
        """Send json (given as Python dictionary) to all players"""
        for player in self.players:
            await player.send_json(json)

