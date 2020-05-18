
from .observer import Observer

class Observable:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer: Observer):
        self.observers.append(observer)

    async def notify_change(self, *argv):
        for observer in self.observers:
            await observer.notify_change(*argv)