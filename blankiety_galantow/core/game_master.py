import random

from .chat import Chat
from .deck import Deck, WhiteCard, BlackCard
from .utils.observable_list import ObservableList
from .player import Player, PlayerState

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
        self.master = None
        players.add_append_callback(self.handle_add_player)
        players.add_remove_callback(self.handle_player_leave)


    async def handle_add_player(self, player):
        await player.fill_player_hand(self.white_deck.get_cards(10))
        await self.send_black_card(player)
        if self.master is None:
            self.master = player
            player.set_player_state(PlayerState.master)
    
    async def handle_player_leave(self, player):
        if self.master is player:
            self.set_new_random_master()
    
    def set_new_random_master(self):
        """Choose random player as master"""
        if len(self.players)>0:
            self.master = random.choice(self.players)
            self.master.set_player_state(PlayerState.master)
        else:
            self.master = None

    async def send_black_card(self, player: Player):
        message = {
            "type": "BLACK_CARD",
            "card": self.black_card.__dict__
        }
        await player.send_json(message)

    async def send_played_cards(self):
        everyone_selected_cards = True
        for player in self.players:
            if player.state == PlayerState.choosing:
                everyone_selected_cards = False
        if everyone_selected_cards:
            message = {
                "type": "PLAYED_CARDS",
                "cards": [
                    {
                        "playerCards":[
                            card.__dict__ for card in player.selected_cards
                        ]
                    } for player in self.players
                ]
            }
            for player in self.players:
                await player.send_json(message)


    async def process_message(self, player: Player, data: Dict):
        if data["type"] == "CARDS_SELECT" and "cards" in data:
            for card in data["cards"]:
                card = player.get_card_by_id(card["id"])
                if card in player.hand:
                    card.selected = True
                else:
                    await player.kick("Próba oszustwa")
                    return
            # Sends played cards in this round if everybody selected their cards
            player.set_player_state(PlayerState.ready)
            await self.send_played_cards()
            return "PLAYER_UPDATE"