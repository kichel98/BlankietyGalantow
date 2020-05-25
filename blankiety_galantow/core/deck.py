import csv
import random


class Deck:
    def __init__(self, card_type, path: str):
        self.cards = list()
        self.card_id = 1
        self.card_type = card_type
        self.path = path
        self.load_from_file()
        self.shuffle_cards()
        

    def load_from_file(self):
        with open(self.path, mode='r', encoding='utf-8') as deck_csv:
            deck_reader = csv.DictReader(deck_csv, delimiter=';')
            
            for _, row in enumerate(deck_reader):
                new_card = self.card_type(self.card_id, row)
                self.card_id = self.card_id + 1
                self.cards.append(new_card)

    def get_card(self):
        if len(self.cards) == 0:
            self.load_from_file()
            self.shuffle_cards()
            
        return self.cards.pop(0)
    
    def get_cards(self, cards_number: int):
        if len(self.cards) < cards_number:
            self.load_from_file()
            self.shuffle_cards()
        
        cards_to_return = self.cards[0:cards_number]
        self.cards = self.cards[cards_number:]
        return cards_to_return

    def shuffle_cards(self):
        random.shuffle(self.cards)

    def get_cards_amount(self):
        return len(self.cards)


class WhiteCard:
    def __init__(self, card_id: int, data):
        self.id: int = card_id
        self.text: str = data["treść"]
        self.selected: bool = False


class BlackCard:
    def __init__(self, card_id: int, data):
        self.id: int = card_id
        self.text: str = data["treść"]
        self.gap_count: int = data["luki"]
