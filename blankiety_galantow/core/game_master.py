import random

from .chat import Chat
from .deck import Deck, WhiteCard, BlackCard
from .utils.observable_list import ObservableList
from .player import Player, PlayerState

from typing import Dict


class GameMaster:
    """GameMaster is responsible for handling game logic"""
    white_deck: Deck
    black_deck: Deck
    black_card: BlackCard

    # FIXME: Zrezygnować z callbacku na rzecz czegoś "ładniejszego"
    def __init__(self, players: ObservableList, chat: Chat, players_update_callback):
        self.players = players
        self.chat = chat
        self.white_deck = Deck(WhiteCard, "resources/game/decks/classic_white.csv")
        self.black_deck = Deck(BlackCard, "resources/game/decks/classic_black.csv")
        self.players_hands = {}
        self.cards_selected = {}
        self.black_card = self.black_deck.get_card()
        self.master = None
        self.selecting_time = 60
        self.players_update_callback = players_update_callback
        players.add_append_callback(self.handle_add_player)
        players.add_remove_callback(self.handle_player_leave)

    async def handle_add_player(self, player):
        await player.add_cards(self.white_deck.get_cards(10))
        await self.send_black_card(player)
        if self.master is None:
            self.master = player
            player.state = PlayerState.master
    
    async def handle_player_leave(self, player):
        if player is self.master:
            self.set_new_random_master()
            await self.chat.send_message_from_system(f"Gracz '{self.master.name}' zostaje Mistrzem Kart.")

    async def process_message(self, player: Player, data: Dict):
        if data["type"] == "CARDS_SELECT" and "cards" in data:
            await self.handle_selecting_cards(player, data)
        if data["type"] == "CHOOSE_WINNING_CARDS" and "cards" in data:
            await self.handle_choosing_winner(data)

    def update_selecting_time(self, new_selecting_time: int):
        self.selecting_time = new_selecting_time
        
    async def handle_selecting_cards(self, player, data):
        """
        Method for handling CARDS_SELECT message
        """
        if not self.player_owns_cards(player, data["cards"]):
            await player.kick("Próba oszustwa")
            return
        self.select_cards(player, data["cards"])
        # Sends played cards in this round if everybody selected their cards
        player.state = PlayerState.ready
        if self.all_players_ready():
            await self.send_played_cards()
        await self.players_update_callback()

    def player_owns_cards(self, player, cards):
        """Send True if player hand has all cards, send False if any card is not in player hand"""
        for card in cards:
            card = player.get_card_by_id(card["id"])
            if card not in player.hand:
                return False
        return True

    def select_cards(self, player, cards):
        """Set cards.selected = True for every card"""
        for card in cards:
            card = player.get_card_by_id(card["id"])
            # To save order of selected cards, card is removed from
            # player.hand, and then added at the end in right order
            player.hand.remove(card)
            player.hand.append(card)
            card.selected = True

    def all_players_ready(self):
        for player in self.players:
            if player.state == PlayerState.choosing:
                return False
        return True

    async def send_played_cards(self):
        message = {
            "type": "PLAYED_CARDS",
            "cards": [
                {
                    "playerCards": [
                        card.__dict__ for card in player.selected_cards
                    ]
                } for player in self.players if player is not self.master
            ]
        }
        for player in self.players:
            await player.send_json(message)

    async def handle_choosing_winner(self, data):
        """
        Method for handling CHOOSE_WINNING_CARDS message
        """
        await self.add_point_to_cards_owner(data["cards"])
        cards_number: int = int(self.black_card.gap_count)
        await self.select_new_black_card()
        await self.refill_players_hand(cards_number)
        self.set_new_master()
        await self.chat.send_message_from_system(f"Gracz '{self.master.name}' zostaje Mistrzem Kart.")
        self.reset_players_state()
        await self.send_empty_played_cards()
        await self.players_update_callback()

    async def add_point_to_cards_owner(self, cards):
        """Add points to card owner and send chat message about it"""
        winner = self.get_cards_owner(cards)
        winner.points += 1
        await self.chat.send_message_from_system(f"Gracz '{winner.name}' wygrał rundę. +1 punkt zwycięstwa.")

    def get_cards_owner(self, cards):
        """
        Get the owner of a set of cards.
        All cards must belong to the same player.
        """
        for card in cards:
            for player in self.players:
                if player.has_card_with_id(card["id"]):
                    return player
        return None

    async def select_new_black_card(self):
        """Select new black card and send it to all players"""
        self.black_card = self.black_deck.get_card()
        for player in self.players:
            await self.send_black_card(player)

    async def send_black_card(self, player: Player):
        message = {
            "type": "BLACK_CARD",
            "card": self.black_card.__dict__
        }
        await player.send_json(message)

    async def refill_players_hand(self, cards_number):
        """Refill players hands with n cards where n = cards_number"""
        for player in self.players:
            if player is not self.master:
                await player.add_cards(self.white_deck.get_cards(cards_number))

    def set_new_random_master(self):
        """Choose random player as master"""
        if len(self.players) > 0:
            self.master = random.choice(self.players)
            self.master.state = PlayerState.master
        else:
            self.master = None

    def set_new_master(self):
        """Set next player in order to be new master"""
        index = (self.players.index(self.master) + 1) % len(self.players)
        self.master = self.players[index]
        self.master.state = PlayerState.master

    def reset_players_state(self):
        """Set every player state, except master, to 'choosing'"""
        for player in self.players:
            if player is not self.master:
                player.state = PlayerState.choosing

    async def send_empty_played_cards(self):
        message = {
            "type": "PLAYED_CARDS",
            "cards": []
        }
        for player in self.players:
            await player.send_json(message)
