from .observable import Observable
from .observer import Observer

class ObservableList(Observable):
    def __init__(self):
        super().__init__()
        self.list = []

    async def add_item(self, item):
        self.list.append(item)
        await self.notify_change("ADD", item)

    async def remove_item(self, item):
        self.list.remove(item)
        await self.notify_change("REMOVE", item)

    async def update_item(self, old_item, new_item):
        self.list[self.list.index(old_item)]=new_item
        await self.notify_change("UPDATE", old_item, new_item)