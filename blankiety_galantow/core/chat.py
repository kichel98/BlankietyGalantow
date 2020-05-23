from blankiety_galantow.core.player import Player


class Chat:
    def __init__(self, players):
        self.players = players

    async def send_message_from_player(self, player: Player, msg: str):
        """Send message from player to all players in this room."""
        await self._send_message(sender_name=player.name, message=msg)

    async def send_message_from_system(self, msg: str):
        """Send chat message from the system to all players."""
        await self._send_message(sender_name="Gra", message=msg, as_system=True)

    async def _send_message(self, sender_name, message, as_system=False):
        """Send chat message to all players."""
        data = {
            "type": "CHAT_MESSAGE",
            "message": {
                "log": as_system,
                "user": sender_name,
                "text": message
            }
        }
        await self._send_json_to_all_players(data)

    async def _send_json_to_all_players(self, json):
        """Send json (given as Python dictionary) to all players"""
        for player in self.players:
            await player.send_json(json)
