import random
from typing import Dict
from fastapi.websockets import WebSocketDisconnect
from fastapi.logger import logger

from .chat import Chat
from .helpers import get_random_string
from .player import Player, PlayerState
from .game_master import GameMaster
from .utils.observable_list import ObservableList
from .kick_exception import KickException


class Room:
    """Single room that manages players inside and game state."""
    def __init__(self, name):
        self.name = name
        self.open = True
        self.selecting_time = 60
        self.number_of_seats = 6
        self.custom_cards = 5
        self.game_type = "default"
        self.players = ObservableList()
        self.chat = Chat(self.players)
        self.game_master = GameMaster(self.players, self.chat, self.send_players_update)
        self.admin = None


    @property
    def number_of_players(self):
        return len(self.players)

    async def add_player_and_listen(self, player: Player):
        """Add new player to the room and start listening."""
        if not self.open:
            await player.kill("Pokój jest zamknięty.")
            logger.error(f"Player '{player}' tried to join a closed server '{self.name}'")
            return

        is_room_full = self.number_of_players == self.number_of_seats
        if is_room_full:
            await player.kill("Pokój jest pełny.")
            logger.error(f"Player '{player}' tried to join a full server '{self.name}'")
            return

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
            await self.players.remove(player)
            await self.handle_player_leaving(player)
        except KickException as ex:
            await self.players.remove(player)
            await self.handle_player_leaving(player, message=ex.message)

    async def process_message(self, player: Player, data: Dict):
        """Process raw JSON message (data) from player."""
        if "type" not in data:
            logger.error(f"Received incorrect message: {data}")
            return
        if data["type"] == "ERROR" and "message" in data:
            logger.error(f"ERROR: {data}")
        elif data["type"] == "SETTINGS" and "settings" in data and self.is_admin(player):
            await self.change_settings(data["settings"])
        elif data["type"] == "CHAT_MESSAGE" and "message" in data:
            await self.chat.send_message_from_player(player, data["message"])
        else:
            # Handle game_master messages
            await self.game_master.process_message(player, data)
            
        # TODO: other types of messages

    async def handle_player_leaving(self, player, message=None):
        """Does all needed operations after player leaves a room"""
        if message is None:
            message = f"Gracz '{player.name}' opuścił pokój."
        if player == self.admin:
            self.set_new_random_admin()
        await self.chat.send_message_from_system(message)
        await self.send_players_update()

    def set_new_random_admin(self):
        """Choose random player as admin"""
        if self.number_of_players>0:
            self.admin = random.choice(self.players)
        else:
            self.admin = None

    async def change_settings(self, settings):
        try:
            await self.set_open_setting(settings["open"])
            await self.set_custom_cards_setting(settings["customCards"])
            await self.set_selecting_time_setting(settings["time"])
            await self.set_game_type_setting(settings["gameType"])
            # TODO: other types of settings
            # TODO: dedicated class for managing settings instead of single functions
        except KeyError:
            logger.error(f"Received invalid settings: {settings}")
        else:
            await self.send_settings_to_players()

    async def set_open_setting(self, open_setting):
        if self.open != open_setting:
            self.open = open_setting
            if open_setting:
                msg = f"Admin {self.admin.name} otworzył pokój."
            else:
                msg = f"Admin {self.admin.name} zamknął pokój."
            await self.chat.send_message_from_system(msg)
        # FIXME: create dedicated RoomSettings class

    async def set_selecting_time_setting(self, selecting_time):
        if self.selecting_time != selecting_time:
            self.game_master.update_selecting_time(selecting_time)
            self.selecting_time = selecting_time
            await self.chat.send_message_from_system(f"Admin {self.admin.name} zmienił czas rundy na {self.selecting_time} sek. \
                Czas rundy zmieni się od następnej rundy.")

    async def set_custom_cards_setting(self, custom_cards):
        if self.custom_cards != custom_cards:
            self.custom_cards = custom_cards
            self.game_master.update_custom_cards_count(custom_cards)
            await self.chat.send_message_from_system(f"Admin {self.admin.name} zmienił liczbę własnych kart na {self.custom_cards}.")

    async def set_game_type_setting(self, game_type):
        if self.game_type != game_type:
            self.game_type = game_type
            if self.game_type == "default":
                await self.chat.send_message_from_system(f"Admin {self.admin.name} zmienił tryb gry na Standardowy.")
            elif self.game_type == "customcards":
                await self.chat.send_message_from_system(f"Admin {self.admin.name} zmienił tryb gry na Mydełko.")

    async def send_settings_to_players(self):
        settings_data = {
            "type": "SETTINGS",
            "settings": {
                "open": self.open,
                "time": self.selecting_time,
                "customCards": self.custom_cards,
                "gameType": self.game_type
            }
        }
        await self.send_json_to_all_players(settings_data)

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