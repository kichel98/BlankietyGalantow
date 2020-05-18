import json

from .deck import Deck, WhiteCard, BlackCard
from .player import Player

from typing import Dict, List

class GameMaster:
    white_deck: Deck
    black_deck: Deck
    players_hands: Dict[Player, List[WhiteCard]]
    cards_selected: Dict[Player, List[WhiteCard]]
    black_card: BlackCard
    """GameManager is responsible for handling game logic"""
    def __init__(self, white_deck: Deck, black_deck: Deck):
        self.white_deck = white_deck
        self.black_deck = black_deck
        self.players_hands = {}
        self.cards_selected = {}
        self.black_card = black_deck.get_card()

    async def new_player(self, player: Player):
        self.players_hands[player] = self.white_deck.get_cards(10)
        self.cards_selected[player] = []
        await self.fill_players_hand(player)
        await self.send_black_card(player)

    async def fill_players_hand(self, player: Player):
        message = {
            "type": "PLAYER_HAND",
            "cards": [card.__dict__ for card in self.players_hands[player]]
        }
        await player.send_json(message)

    async def send_black_card(self, player: Player):
        message = {
            "type": "BLACK_CARD",
            "card": self.black_card.__dict__
        }
        await player.send_json(message)

    def process_message(self, player: Player, data: Dict):
        # if data["type"] == "CHAT_MESSAGE" and "message" in data:
          pass  
        