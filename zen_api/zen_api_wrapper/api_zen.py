import urllib

import aiohttp

class ZenAPI:
    """Main API class contains async requests for ZENAPP and ZEN API."""

    def __init__(self, session):
        self.session = session
        
    async def _get_request(self, url):
        """Make an asnyc GET request and return json.
        
        Args:
            url (str): ZEN API GET endpoint url.
            
        Returns:
            json: request Response.
        """

        encoded_url = urllib.parse.quote(url, safe=':/?&=,.')
        try:
            async with self.session.get(encoded_url) as r:
                json_response = await r.json()
        except aiohttp.ClientResponseError:
            raise Exception('Could not connect to ZEN API')
        
        return json_response
    
    async def _post_request(self, url, payload):
        """Make an async POST request and return json.
        
        Args:
            url (str): ZEN API POST endpoint url.
            payload (json): POST request body.
            
        Returns:
            json: request Response.
        """
        
        encoded_url = urllib.parse.quote(url, safe=':/?&=,.')
        try:
            async with self.session.post(encoded_url, json=payload) as r:
                json_response = await r.json()
        except aiohttp.ClientResponseError:
            raise Exception('Could not connect to ZEN API')
        
        return json_response
    
    async def get_guardian_db_id(self, destiny_membership_id: str):
        url = 'http://127.0.0.1:8000/guardians/{}/id'
        url = url.format(str(destiny_membership_id))
        
        return await self._get_request(url)
    
    async def post_create_guardian(self, payload):
        url = 'http://127.0.0.1:8000/guardians/'
        
        return await self._post_request(url, payload=payload)
    
    async def post_create_character(self, guardian_id, payload):
        url = 'http://127.0.0.1:8000/guardians/{}/'
        url = url.format(guardian_id)
        
        return await self._post_request(url, payload=payload)
    
    async def post_create_weapon(self, character_id, payload):
        url = 'http://127.0.0.1:8000/characters/{}/weapons'
        url = url.format(character_id)
        
        return await self._post_request(url, payload=payload)
        