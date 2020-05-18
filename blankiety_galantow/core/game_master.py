import json

from .deck import Deck, WhiteCard, BlackCard
from .player import Player

from typing import Dict, List

class GameMaster:
    players_hands: Dict[Player, List[WhiteCard]]
    cards_selected: Dict[Player, List[WhiteCard]]
    black_card: BlackCard
    """GameManager is responsible for handling game logic"""
    def __init__(self, white_deck: Deck, black_deck: Deck):
        self.white_deck = white_deck
        self.black_deck = black_deck
        self.players_hands = {}

    async def new_player(self, player: Player):
        self.players_hands[Player] = []
        await self.fill_players_hand(player)

    async def fill_players_hand(self, player: Player):

        message = {
            "type": "PLAYER_HAND",
            "cards": [card.__dict__ for card in self.white_deck.get_cards(8)]
        }
        await player.send_json(message)

    def process_message(self, player: Player, data: Dict):
        # if data["type"] == "CHAT_MESSAGE" and "message" in data:
          pass  
        