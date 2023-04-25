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