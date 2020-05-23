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

    def __init__(self, players: ObservableList, chat: Chat, players_update_callback):
        self.players = players
        self.chat = chat
        self.white_deck = Deck(WhiteCard, "resources/game/decks/classic_white.csv")
        self.black_deck = Deck(BlackCard, "resources/game/decks/classic_black.csv")
        self.players_hands = {}
        self.cards_selected = {}
        self.black_card = self.black_deck.get_card()
        self.master = None
        self.players_update_callback = players_update_callback
        players.add_append_callback(self.handle_add_player)
        players.add_remove_callback(self.handle_player_leave)


    async def handle_add_player(self, player):
        await player.fill_player_hand(self.white_deck.get_cards(10))
        await self.send_black_card(player)
        if self.master is None:
            self.master = player
            player.set_player_state(PlayerState.master)
    
    async def handle_player_leave(self, player):
        if player is self.master:
            self.set_new_random_master()
    
    def set_new_random_master(self):
        """Choose random player as master"""
        if self.master is not None:
            self.master.set_player_state(PlayerState.choosing)
        if len(self.players)>0:
            self.master = random.choice([player for player in self.players if player is not self.master])
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
                    } for player in self.players if player is not self.master
                ]
            }
            for player in self.players:
                await player.send_json(message)
            

    async def send_empty_played_cards(self):
        message = {
            "type": "PLAYED_CARDS",
            "cards": []
        }
        for player in self.players:
            await player.send_json(message)

    async def add_points(self, cards):
        # TODO: Think if we want to validate that all winning cards are in player hand
        # Add points
        for card in cards:
            for winning_player in self.players:
                winning_card = winning_player.get_card_by_id(card["id"])
                if winning_card is not None:
                    winning_player.points += 1
                    return

    async def refill_players_hand(self, cards_number):
        # Refill players hands with n cards where n = cards_number
        for player in self.players:
            if player is not self.master:
                await player.fill_player_hand(self.white_deck.get_cards(cards_number))

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
            await self.players_update_callback()
        if data["type"] == "CHOOSE_WINNING_CARDS" and "cards" in data:
            self.add_points(data["cards"])
            
            # Select new black card
            cards_number:int = int(self.black_card.gap_count)
            self.black_card = self.black_deck.get_card()
            for player in self.players:
                await self.send_black_card(player)

            # Refill players hands
            self.refill_players_hand(cards_number)

            # Select new master
            self.set_new_random_master()

            # Sends empty played cards
            await self.send_empty_played_cards()
            await self.players_update_callback()