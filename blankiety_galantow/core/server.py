from typing import Dict
from .player import Player
from .room import Room


class Server:
    """Server that manages all rooms in the app."""
    def __init__(self):
        self._rooms = {
            1: Room()
        }

    def room_exists(self, room_id):
        """Check if room with given id exists on the server."""
        if room_id in self._rooms:
            return True
        else:
            return False

    async def add_player(self, room_id: int, player: Player):
        """Add new player to existing room."""
        await self._rooms[room_id].add_player_and_listen(player)

    _rooms: Dict[int, Room]
