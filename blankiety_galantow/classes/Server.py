from typing import List, Dict
from .Player import Player

class Server:
    def __init__(self):
        self.tables = {}
    tables: Dict[int, List[Player]]