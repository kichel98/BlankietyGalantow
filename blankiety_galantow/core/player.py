from json import JSONDecodeError
from fastapi import WebSocket
from fastapi.websockets import WebSocketDisconnect
from .kick_exception import KickException
from enum import Enum

from typing import List


class PlayerState(Enum):
    master = 1
    choosing = 2
    ready = 3


class Player:
    def __init__(self, socket: WebSocket, username: str):
        self.name = username
        self.socket = socket
        self.id = None
        self.state = PlayerState.choosing
        self.hand = []
        self.points = 0

    def __str__(self):
        return f"id: {self.id}, name: {self.name}"

    @property
    def selected_cards(self):
        selected_cards = []
        for card in self.hand:
            if card.selected:
                selected_cards.append(card)
        return selected_cards

    def get_card_by_id(self, card_id: int):
        for card in self.hand:
            if card.id == card_id:
                return card
        return None

    def has_card_with_id(self, card_id: int):
        return self.get_card_by_id(card_id) is not None

    async def add_cards(self, cards: List):
        self.hand = [card for card in self.hand if not card.selected]
        self.hand = self.hand + cards
        await self.send_player_hand()

    async def send_player_hand(self):
        message = {
            "type": "PLAYER_HAND",
            "cards": [
                card.__dict__ for card in self.hand
            ]
        }
        await self.send_json(message)
        
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

    async def kill(self, error_msg: str):
        """Disconnect player with an error message"""
        error_data = {
            "type": "ERROR",
            "message": error_msg
        }
        await self.send_json(error_data)
        await self.socket.close()
