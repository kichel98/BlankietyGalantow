import json

from .deck import Deck, WhiteCard, BlackCard
from .utils.observable_list import ObservableList
from .player import Player

from typing import Dict, List


class GameMaster:
    white_deck: Deck
    black_deck: Deck
    players_hands: Dict[Player, List[WhiteCard]]
    cards_selected: Dict[Player, List[WhiteCard]]
    black_card: BlackCard
    """GameManager is responsible for handling game logic"""
    def __init__(self, players: ObservableList):
        super().__init__()
        self.white_deck = Deck(WhiteCard, "resources/game/decks/classic_white.csv")
        self.black_deck = Deck(BlackCard, "resources/game/decks/classic_black.csv")
        self.players_hands = {}
        self.cards_selected = {}
        self.black_card = self.black_deck.get_card()
        self.players = players
        players.add_append_callback(self.handle_add_player)
        players.add_remove_callback(self.handle_remove_player)

    async def handle_add_player(self, player):
        self.players_hands[player] = self.white_deck.get_cards(10)
        self.cards_selected[player] = []
        await self.fill_player_hand(player)
        await self.send_black_card(player)
    
    async def handle_remove_player(self, player):
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

    async def send_played_cards(self):
        everyone_selected_cards = True
        for cards in self.cards_selected.values():
            if len(cards) == 0:
                everyone_selected_cards = False
        if everyone_selected_cards:
            message = {
                "type": "PLAYED_CARDS",
                "cards": [{"playerCards": [{"id": card.card_id, "text": card.text} for card in self.cards_selected[player]]} for player in self.players]
            }
            for player in self.players:
                await player.send_json(message)

    def get_player_card_by_id(self, player: Player, card_id: int):
        for card in self.players_hands[player]:
            if card.card_id == card_id:
                return card
        return None

    async def process_message(self, player: Player, data: Dict):
        if data["type"] == "CARDS_SELECT" and "cards" in data:
            for card in data["cards"]:
                player_card = self.get_player_card_by_id(player, card["id"])
                if player_card != None:
                    self.cards_selected[player].append(player_card)
                else:
                    await player.kick("Próba oszustwa")
                    return
            # Sends played cards in this round if everybody selected their cards
            await self.send_played_cards()
