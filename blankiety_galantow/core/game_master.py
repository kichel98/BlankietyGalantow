from .chat import Chat
from .deck import Deck, WhiteCard, BlackCard
from .utils.observable_list import ObservableList
from .player import Player

from typing import Dict, List


class GameMaster:
    """GameManager is responsible for handling game logic"""
    white_deck: Deck
    black_deck: Deck
    black_card: BlackCard

    def __init__(self, players: ObservableList, chat: Chat):
        self.players = players
        self.chat = chat
        self.white_deck = Deck(WhiteCard, "resources/game/decks/classic_white.csv")
        self.black_deck = Deck(BlackCard, "resources/game/decks/classic_black.csv")
        self.players_hands = {}
        self.cards_selected = {}
        self.black_card = self.black_deck.get_card()
        players.add_append_callback(self.handle_add_player)

    async def handle_add_player(self, player):
        await player.fill_player_hand(self.white_deck.get_cards(10))
        await self.send_black_card(player)
    

    async def send_black_card(self, player: Player):
        message = {
            "type": "BLACK_CARD",
            "card": {
                "id": self.black_card.id,
                "text": self.black_card.text,
                "gap_count": self.black_card.gap_count
            }
        }
        await player.send_json(message)

    async def send_played_cards(self):
        everyone_selected_cards = True
        for player in self.players:
            if len(player.selected_cards) == 0:
                everyone_selected_cards = False
        if everyone_selected_cards:
            message = {
                "type": "PLAYED_CARDS",
                "cards": [
                    {
                        "playerCards": [
                            {
                                "id": card.id,
                                "text": card.text
                            } for card in player.selected_cards
                        ]
                    } for player in self.players
                ]
            }
            for player in self.players:
                await player.send_json(message)


    async def process_message(self, player: Player, data: Dict):
        if data["type"] == "CARDS_SELECT" and "cards" in data:
            for card in data["cards"]:
                player_card = player.get_card_by_id(card["id"])
                if player_card is not None:
                    player_card.selected = True
                else:
                    await player.kick("Próba oszustwa")
                    return
            # Sends played cards in this round if everybody selected their cards
            await self.send_played_cards()
