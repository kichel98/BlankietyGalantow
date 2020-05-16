from .helpers import get_random_string
from .player import Player
from .room import Room


class Server:
    """Server that manages all rooms in the app."""
    def __init__(self):
        self._rooms = {}

    def room_exists(self, room_id: int):
        """Check if room with given id exists on the server."""
        if room_id in self._rooms:
            return True
        else:
            return False

    async def add_player_to_room(self, room_id: int, player: Player):
        """Add new player to existing room."""
        await self._rooms[room_id].add_player_and_listen(player)

    def add_room(self, name: str):
        """Add new room with random alpha-numeric id"""
        while True:
            random_id = get_random_string(length=8)
            if random_id not in self._rooms:
                self._rooms[random_id] = Room(name)
                break

    def get_room_list(self):
        """Prepare and return list of all rooms."""
        room_list = [
            {
                "id": key,
                "name": room.name,
                "players": room.number_of_players,
                "maxPlayers": room.number_of_seats,
                "open": room.open
            }
            for key, room in self._rooms.items()
        ]
        return room_list

    def generate_unique_player_id(self, room_id):
        room = self._rooms[room_id]
        id = get_random_string()
        players_id = [player.id for player in room.players]
        while id in players_id:
            id = get_random_string()
        return id
