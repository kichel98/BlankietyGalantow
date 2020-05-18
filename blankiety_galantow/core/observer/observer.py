
from typing import List

class Observer:
    def __init__(self):
        self.callbacks = []

    def add_callback(self, callback):
        self.callbacks.append(callback)

    async def notify_change(self, *argv):
        for callback in self.callbacks:
            await callback(*argv)