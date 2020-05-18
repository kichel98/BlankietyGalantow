import csv
import random


class Deck:
    def __init__(self, card_type, path: str):
        self.cards = list()
        self.card_type = card_type
        self.path = path
        self.load_from_file()
        self.shuffle_cards()

    def load_from_file(self):
        with open(self.path, mode='r', encoding='utf-8') as deck_csv:
            deck_reader = csv.DictReader(deck_csv, delimiter=';')
            
            for counter, row in enumerate(deck_reader):
                new_card = self.card_type(counter, row)
                self.cards.append(new_card)

    def get_card(self):
        if len(self.cards) == 0:
            self.load_from_file()
            self.shuffle_cards()
            
        return self.cards.pop(0)
    
    def shuffle_cards(self):
        random.shuffle(self.cards)

    def get_cards_amount(self):
        return len(self.cards)


class WhiteCard:
    def __init__(self, card_id: int, data):
        self.id: int = card_id
        self.text: str = data["treść"]


class BlackCard:
    def __init__(self, card_id: int, data):
        self.id: int = card_id
        self.text: str = data["treść"]
        self.gap_count: int = data["luki"]
