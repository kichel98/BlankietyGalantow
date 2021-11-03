import random
import time
import asyncio

from .deck import Deck, WhiteCard, BlackCard
from .utils.timer import Timer
from .player import Player, PlayerState
from .game_state import GameState
from typing import Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from blankiety_galantow.core.room import Room


class GameMaster:
    """GameMaster is responsible for handling game logic"""
    white_deck: Deck
    black_deck: Deck
    black_card: BlackCard

    def __init__(self, room: 'Room'):
        self.room = room
        self.players = room.players
        self.chat = room.chat
        self.settings = room.settings
        self.send_players_update = room.send_players_update
        self.white_deck = Deck(WhiteCard, "resources/game/decks/classic_white.csv")
        self.black_deck = Deck(BlackCard, "resources/game/decks/classic_black.csv")
        self.players_hands = {}
        self.cards_selected = {}
        self.black_card = self.black_deck.get_card()
        self.master = None
        self.selecting_time = self.settings.selecting_time  # current round time
        self.timer_start_time = 0
        self.timer = None
        self.game_state = GameState.selecting_cards
        self.players.add_append_callback(self.handle_add_player)
        self.players.add_remove_callback(self.handle_player_leave)

    async def handle_add_player(self, player):
        await player.add_cards(self.white_deck.get_cards(10))
        await self.send_black_card(player)
        if self.master is None:
            self.master = player
            player.state = PlayerState.master
        if len(self.players) == 2:
            await self.timer_start()
        await self.send_timer_message(player)
    
    async def handle_player_leave(self, player):
        if len(self.players) < 2 and self.is_timer_set():
            self.timer.cancel()
        if player is self.master:
            self.set_new_random_master()
            if len(self.players) > 1:
                await self.chat.send_message_from_system(f"Gracz '{self.master.name}' zostaje Mistrzem Kart.")
                await self.timer_start()
        if self.all_players_ready():
            await self.send_played_cards()

    async def process_message(self, player: Player, data: Dict):
        if data["type"] == "CARDS_SELECT" and "cards" in data:
            if self.game_state == GameState.selecting_cards:    
                await self.handle_selecting_cards(player, data)
        if data["type"] == "CHOOSE_WINNING_CARDS" and "cards" in data:
            if self.game_state == GameState.choosing_winner:    
                await self.handle_choosing_winner(data)
        if data["type"] == "CARDS_REVEAL" and "cards" in data:
            await self.handle_cards_reveal(player, data)
        if data["type"] == "CUSTOM_CARD" and "card" in data:
            await self.handle_custom_card(player, data)

    async def handle_custom_card(self, player, data):
        if player.custom_cards_used < self.settings.custom_cards:
            card = data["card"]
            custom_card = player.get_card_by_id(card["id"])
            custom_card.text = card["text"]

    async def handle_cards_reveal(self, player, data):
        cards_owner = self.get_cards_owner_by_id(data["cards"])
        if cards_owner is None:
            await self.room.kick_player(player, "Próba oszustwa")
            return
        message = {
            "type": "CARDS_REVEAL",
            "cards": data["cards"]
        }
        for player in self.players:
            await player.send_json(message)

    async def timer_start(self):
        if self.selecting_time != self.settings.selecting_time:
            self.selecting_time = self.settings.selecting_time
        if self.timer_start_time == 0:
            self.timer_start_time = time.time()
        if self.timer is not None:
            self.timer_start_time = time.time()
            self.timer.cancel()
            try:
                await self.timer.task
            except asyncio.CancelledError:
                pass
        self.timer = Timer(self.selecting_time, self.handle_timeout)

    def is_timer_set(self):
        return self.timer is not None

    async def handle_timeout(self):
        self.timer_start_time = 0
        if not self.settings.paused:
            if self.game_state == GameState.selecting_cards:
                await self.verify_players_activity()
            elif self.game_state == GameState.choosing_winner:
                await self.start_new_round_without_winner()
        self.timer = None

    async def verify_players_activity(self):
        for player in self.players:
            if player.state == PlayerState.choosing:
                await self.select_random_player_cards(player)
                player.rounds_without_activity = player.rounds_without_activity + 1
                if player.rounds_without_activity > 2:
                    await self.room.kick_player(player, "Brak aktywności.")
            elif player.state == PlayerState.ready:
                player.rounds_without_activity = 0

    async def select_random_player_cards(self, player):
        cards = random.choices(player.hand, k=int(self.black_card.gap_count))
        await self.send_select_random_cards_message(player, cards)
        data = {
            "cards": [
                {
                    "id": card.id
                } for card in cards
            ]
        }
        await self.handle_selecting_cards(player, data)

    async def send_select_random_cards_message(self, player, cards):
        message = {
            "type": "SELECT_RANDOM_CARDS",
            "cards": [
                card.__dict__ for card in cards
            ]
        }
        await player.send_json(message)

    async def start_new_round_without_winner(self):
        """
        Method for starting new selecting cards round without choosing winner
        """
        cards_number: int = int(self.black_card.gap_count)
        await self.select_new_black_card()
        await self.refill_players_hand(cards_number)
        self.set_new_master()
        await self.chat.send_message_from_system(f"W tej rundzie nikt nie został zwycięzcą :(")
        await self.chat.send_message_from_system(f"Gracz '{self.master.name}' zostaje Mistrzem Kart.")
        self.reset_players_state()
        await self.send_empty_played_cards()
        await self.send_players_update()
        self.game_state = GameState.selecting_cards
        await self.timer_start()

    async def send_timer_message(self, player):
        current_time = time.time()
        time_passed = int(current_time - self.timer_start_time)
        timer = self.selecting_time
        if self.timer_start_time != 0:
            timer = self.selecting_time - time_passed
        message = {
            "type": "TIMER",
            "timer": timer
        }
        await player.send_json(message)

    async def handle_selecting_cards(self, player, data):
        """
        Method for handling CARDS_SELECT message
        """
        if not self.player_owns_cards(player, data["cards"]):
            await self.room.kick_player(player, "Próba oszustwa.")
            return
        self.select_cards(player, data["cards"])
        # Sends played cards in this round if everybody selected their cards
        player.state = PlayerState.ready
        if self.all_players_ready():
            await self.send_played_cards()
            self.game_state = GameState.choosing_winner
            await self.timer_start()
        await self.send_players_update()

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
            self.select_player_card(player, card["id"])

    def select_player_card(self, player, card_id):
        card = player.get_card_by_id(card_id)
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
                } for player in self.players if player is not self.master and player.state == PlayerState.ready
            ]
        }

        random.shuffle(message["cards"])

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
        await self.send_players_update()
        self.game_state = GameState.selecting_cards
        await self.timer_start()

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

    def get_cards_owner_by_id(self, card_ids):
        for card_id in card_ids:
            for player in self.players:
                if player.has_card_with_id(card_id):
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
