class ObservableList(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.append_callbacks = []
        self.remove_callbacks = []

    async def append(self, item):
        super().append(item)
        for callback in self.append_callbacks:
            await callback(item)

    async def remove(self, item):
        super().remove(item)
        for callback in self.remove_callbacks:
            await callback(item)

    def add_append_callback(self, callback):
        self.append_callbacks.append(callback)

    def add_remove_callback(self, callback):
        self.remove_callbacks.append(callback)
