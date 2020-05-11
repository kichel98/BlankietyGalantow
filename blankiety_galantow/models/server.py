class Server:
    def __init__(self, name: str, server_id: int, server_address: str, number_of_players: int, number_of_seats: int):
        self.name = name
        self.server_id = server_id
        self.server_address = server_address
        self.number_of_players = number_of_players
        self.number_of_seats = number_of_seats

    name: str
    server_id: int
    server_address: str
    number_of_players: int
    number_of_seats: int