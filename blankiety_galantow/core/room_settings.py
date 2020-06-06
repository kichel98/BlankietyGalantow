from blankiety_galantow.core.chat import Chat
from fastapi.logger import logger


class RoomSettings:
    def __init__(self, chat: Chat):
        self.chat = chat
        self.name: str = ""
        self.open: bool = True
        self.number_of_seats: int = 6
        self.selecting_time: int = 60
        self.game_type: str = "default"
        self.custom_cards: int = 5
        self.password: str = ""

    async def update(self, who: str, data: dict):
        try:
            await self.set_name(who, data["roomName"])
            await self.set_open(who, data["open"])
            await self.set_custom_cards(who, data["customCards"])
            await self.set_selecting_time(who, data["time"])
            await self.set_game_type(who, data["gameType"])
            self.set_room_password(data["password"])
        except KeyError:
            logger.error(f"Received invalid settings: {data}")

    async def set_name(self, who: str, new_name):
        if self.name != new_name:
            self.name = new_name
            msg = f"Admin {who} zmienił nazwę pokoju na: '{new_name}'"
            await self.chat.send_message_from_system(msg)

    async def set_open(self, who: str, open_setting):
        if self.open != open_setting:
            self.open = open_setting
            if open_setting:
                msg = f"Admin {who} otworzył pokój."
            else:
                msg = f"Admin {who} zamknął pokój."
            await self.chat.send_message_from_system(msg)

    async def set_selecting_time(self, who: str, selecting_time):
        if self.selecting_time != selecting_time:
            self.selecting_time = selecting_time
            await self.chat.send_message_from_system(f"Admin {who} zmienił czas rundy na {selecting_time} sek. \
                Czas rundy zmieni się od następnej rundy.")

    async def set_custom_cards(self, who: str, custom_cards):
        if self.custom_cards != custom_cards:
            self.custom_cards = custom_cards
            await self.chat.send_message_from_system(f"Admin {who} zmienił liczbę własnych kart na {custom_cards}.")

    async def set_game_type(self, who: str, game_type):
        if self.game_type != game_type:
            self.game_type = game_type
            if self.game_type == "default":
                await self.chat.send_message_from_system(f"Admin {who} zmienił tryb gry na Standardowy.")
            elif self.game_type == "customcards":
                await self.chat.send_message_from_system(f"Admin {who} zmienił tryb gry na Mydełko.")

    def set_room_password(self, password):
        self.password = password
