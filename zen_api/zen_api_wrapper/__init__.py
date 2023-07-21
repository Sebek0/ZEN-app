import aiohttp
import asyncio

from .api_zen import ZenAPI

class ZENAPI:
    def __init__(self, loop=None):
        self._loop = asyncio.get_event_loop() if loop is None else loop
        self._session = aiohttp.ClientSession(loop=self._loop)
        self.api = ZenAPI(self._session)
        
    async def close(self):
        await self._session.close()