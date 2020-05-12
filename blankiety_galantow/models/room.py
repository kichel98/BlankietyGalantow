class Room:
    def __init__(self, name: str, room_id: int, room_address: str, number_of_players: int, number_of_seats: int, players: list, settings: dict, white_deck: list, black_deck: list):
        self.name = name
        self.room_id = room_id
        self.room_address = room_address
        self.number_of_players = number_of_players
        self.number_of_seats = number_of_seats
        self.players = players
        self.settings = settings
        self.white_deck = white_deck
        self.black_deck = black_deck

    name: str
    room_id: int
    room_address: str
    number_of_players: int
    number_of_seats: int
    players: list
    settings: dict
    white_deck: list
    black_deck: list