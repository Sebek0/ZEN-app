import aiohttp
import asyncio

from bungie_api_wrapper.bungie_api import BungieAPI

class BAPI:
    def __init__(self, api_key, loop=None):
        self._loop = asyncio.get_event_loop() if loop is None else loop
        self._session = aiohttp.ClientSession(loop=self._loop)
        self.api = BungieAPI(api_key, self._session)
    
    async def close(self):
        await self._session.close()