from fastapi import WebSocket

class User:
    def __init__(self, username:str, socket:WebSocket):
        self.username = username
        self.socket = socket
    username:str
    socket:WebSocket