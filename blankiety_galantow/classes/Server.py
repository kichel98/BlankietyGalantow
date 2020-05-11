from typing import List, Dict
from .User import User

class Server:
    def __init__(self):
        self.tables = {}
    tables: Dict[int, List[User]]