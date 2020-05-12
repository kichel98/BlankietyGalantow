class Room:
    def __init__(self, name: str, id: int, number_of_players: int, number_of_seats: int, open: bool, players: list, settings: dict, white_deck: list, black_deck: list):
        self.name = name
        self.id = id
        self.number_of_players = number_of_players
        self.number_of_seats = number_of_seats
        self.open = open
        self.players = players
        self.settings = settings
        self.white_deck = white_deck
        self.black_deck = black_deck


    name: str
    room_id: int
    number_of_players: int
    number_of_seats: int
    open: bool
    players: list
    settings: dict
    white_deck: list
    black_deck: list