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
        await self._rooms[room_id].connect_new_player_and_listen(player)
        self.delete_if_empty(room_id)

    def add_room(self, name: str, seats: int = 0):
        """Add new room with random alpha-numeric id"""
        while True:
            random_id = get_random_string(length=8)
            if random_id not in self._rooms:
                room = Room(name)
                if seats != 0:
                    room.number_of_seats = seats
                self._rooms[random_id] = room
                return random_id

    def delete_if_empty(self, room_id: int):
        if self._rooms[room_id].is_empty:
            del self._rooms[room_id]

    def get_room_list(self):
        """Prepare and return list of all rooms."""
        room_list = [
            {
                "id": key,
                "name": room.settings.name,
                "players": room.number_of_players,
                "maxPlayers": room.settings.number_of_seats,
                "open": room.settings.open,
                "password": room.settings.password != ""
            }
            for key, room in self._rooms.items()
        ]
        return room_list
