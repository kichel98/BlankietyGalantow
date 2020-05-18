import csv
import random

class Deck:

    def __init__(self, CardType, path):     
        self.cards = list()
        self.CardType = CardType
        self.path = path
        self.load_from_file()
        self.shuffle_cards()

    def load_from_file(self):
        with open(self.path, mode='r', encoding='utf-8') as deck_csv:
            deck_reader = csv.DictReader(deck_csv, delimiter=';')
            
            for id, row in enumerate(deck_reader):
                new_card = self.CardType(id, row)
                self.cards.append(new_card)

    def get_card(self):
        if len(self.cards) == 0:
            self.load_from_file()
            self.shuffle_cards()
            
        return self.cards.pop(0)
    
    def get_cards(self, cards_number):
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
    def __init__(self, card_id: int, deck_reader):
        self.card_id: int = card_id
        self.text: str = deck_reader["treść"]


class BlackCard:
    def __init__(self, card_id, deck_reader):
        self.card_id = card_id
        self.text = deck_reader["treść"]
        self.gap_count = deck_reader["luki"]