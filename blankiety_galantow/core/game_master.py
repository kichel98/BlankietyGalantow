import json

from .deck import Deck, WhiteCard, BlackCard
from .player import Player
from .observer.observer import Observer

from typing import Dict, List

class GameMaster(Observer):
    white_deck: Deck
    black_deck: Deck
    players_hands: Dict[Player, List[WhiteCard]]
    cards_selected: Dict[Player, List[WhiteCard]]
    black_card: BlackCard
    """GameManager is responsible for handling game logic"""
    def __init__(self):
        super().__init__()
        self.white_deck = Deck(WhiteCard, "resources/game/decks/classic_white.csv")
        self.black_deck = Deck(BlackCard, "resources/game/decks/classic_black.csv")
        self.players_hands = {}
        self.cards_selected = {}
        self.black_card = self.black_deck.get_card()
        self.add_callback(self.handle_players)

    async def handle_players(self, *argv):
        if argv[0] == "ADD":
            await self.handle_new_player(argv[1])
        if argv[0] == "REMOVE":
            await self.handle_player_exit(argv[1])

    async def handle_new_player(self, player):
        self.players_hands[player] = self.white_deck.get_cards(10)
        self.cards_selected[player] = []
        await self.fill_player_hand(player)
        await self.send_black_card(player)
    
    async def handle_player_exit(self, player):
        del self.players_hands[player]
        del self.cards_selected[player]

    async def fill_player_hand(self, player: Player):
        message = {
            "type": "PLAYER_HAND",
            "cards": [{"id": card.card_id, "text": card.text} for card in self.players_hands[player]]
        }
        await player.send_json(message)

    async def send_black_card(self, player: Player):
        message = {
            "type": "BLACK_CARD",
            "card": {"id": self.black_card.card_id, "text": self.black_card.text, "gap_count": self.black_card.gap_count}
        }
        await player.send_json(message)

    def process_message(self, player: Player, data: Dict):
        pass  
        