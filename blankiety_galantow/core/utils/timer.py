import asyncio


class Timer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        self.task = asyncio.ensure_future(self._job())
                

    async def _job(self):
        try:
            await asyncio.sleep(self._timeout)
            await self._callback()
        except asyncio.CancelledError:
            pass

    def cancel(self):
        self.task.cancel()
        