from fastapi import WebSocket


class Player:
    def __init__(self, username: str, socket: WebSocket):
        self.username = username
        self.socket = socket
    username: str
    socket: WebSocket
