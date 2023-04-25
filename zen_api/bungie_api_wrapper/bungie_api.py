import urllib
import os

import aiohttp

from dotenv import load_dotenv

# Will load configuration variables from .env file
load_dotenv()

DESTINY2_URL = os.getenv('DESTINY2_URL')
USER_URL = os.getenv('USER_URL')
GROUP_URL = os.getenv('GROUP_URL')


class BungieAPI:
    """Main API class contains async requests for Destiny2 and Bungie API.
    Small documentation about requests in docstrings below, but it's preferable
    to use offical Bungie API documentation here:
    https://bungie-net.github.io/multi/index.html.
    """
    
    def __init__(self, api_key, session):
        self.api_key = api_key
        self.session = session
        
    async def _get_request(self, url):
        """Make an asnyc GET request and return json.
        
        Args:
            url (str): Bungie API GET endpoint url.
            
        Returns:
            json: request Response.
        """

        headers = {'X-API-Key': str(self.api_key)}
        encoded_url = urllib.parse.quote(url, safe=':/?&=,.')
        try:
            async with self.session.get(encoded_url, headers=headers) as r:
                json_response = await r.json()
        except aiohttp.ClientResponseError:
            raise Exception('Could not connect to Bungie API')
        
        return json_response
    
    async def _post_request(self, url, payload):
        """Make an async POST request and return json.
        
        Args:
            url (str): Bungie API POST endpoint url.
            payload (json): POST request body.
            
        Returns:
            json: request Response.
        """
        
        headers = {'X-API-Key': str(self.api_key)}
        encoded_url = urllib.parse.quote(url, safe=':/?&=,.')
        try:
            async with self.session.post(encoded_url, headers=headers, json=payload) as r:
                json_response = await r.json()
        except aiohttp.ClientResponseError:
            raise Exception('Could not connect to Bungie API')
        
        return json_response
    
    async def get_connection_status(self, platform, payload):
        """Checks the connection with Bungie API.
        
        Args:
            platform (int): Destiny2 membershipType.
            payload (json): POST request body
                displayName (str): Destiny2 User displayName.
                displayNameCode (int): Destiny2 User Code (number after #).
                
        Returns:
            json: request Response.
        """
        
        url = DESTINY2_URL + 'SearchDestinyPlayerByBungieName/{}/'
        url = url.format(platform)
        
        return await self._post_request(url, payload)
    
    async def get_destiny_profile(self, destiny_membership_id, platform,
                                  components):
        """Returns Destiny2 Player Profile.
        
        Args:
            destiny_membership_id (int): Bungie destinyMembershipId.
            platform (int): Destiny2 membershipType.
            components (list): List containing components to include in requests.
                At least one component is required to receive results.
                Can use either ints or strings.
        
        Returns:
            json: request Response.
        """
        
        url = DESTINY2_URL + '{}/Profile/{}/?components={}'
        url = url.format(platform, destiny_membership_id, ','.join(
            [str(i) for i in components]))
        
        return await self._get_request(url)
    
    async def get_bungienet_user(self, bungie_id):
        """Returns Bungie.net User
        
        Args:
            bungie_id (int): Bungie.net membershipId.
            
        Returns:
            json: request Response.
        """
        
        url = USER_URL + 'GetBungieNetUserById/{}/'
        url = url.format(bungie_id)
        
        return await self._get_request(url)
    
    async def post_search_destiny_player(self, platform, payload):
        """Returns a list of Destiny memberships.
        
        Args:
            platform (int): Destiny2 membershipType.
            payload (dict): POST request body.
                displayName (str): Bungie username.
                displayNameCode (int): Bungie user code.
        
        Returns:
            json: request Response.
        """
        
        url = DESTINY2_URL + 'SearchDestinyPlayerByBungieName/{}/'
        url = url.format(platform)
        
        return await self._post_request(url, payload)
        
    async def get_search_destiny_player(self, display_name_prefix, page):
        """Search Destiny2 Player with global name prefix.
        
        For example: global name prefix: 'Test' when global name: 'Test#1234'.
        It's not the best option to find user, but can come handy when someone
        is using unusual name.
        
        Note:
            Page starts from 0.
        
        Args:
            display_name_prefix (str): Global name prefix, everything before '#'.
            page (int): Determine which page to display. If name is popular,
                request may return multiple pages of users with this name.
                
        Returns:
            json: request Response.
        """
        
        url = USER_URL + 'Search/Prefix/{}/{}/'
        url = url.format(display_name_prefix, page)
        
        return await self._get_request(url)
    
    async def get_destiny_player(self, global_name, platform):
        """Returns a list of Destiny memberships.
        
        This method will hide overridden memberships due to cross save.
        This is an exact match lookup.
        
        Args:
            global_name (str): Global Bungie displayName.
            platform (int): Destiny2 membershipType
            
        Returns:
            json: request Response.
        """
        
        url = DESTINY2_URL + 'SearchDestinyPlayer/{}/{}/'
        url = url.format(platform, global_name)
        
        return await self._get_request(url)
    
    async def get_characters_id(self, destiny_membership_id, platform,
                             components):
        """Returns a list of Users characters ids.
        
        Args:
            destiny_membership_id (str): Destiny membershipId.
            platform (int): Destiny2 membershipType.
            components (list): List of components to include in response.
                See the DestinyComponentType enum for valid components to request here,
                "https://bungie-net.github.io/multi/index.html". You must request at
                least one component to receive results. It should be either int or
                string. You must request at least one component to receive results.
        
        Returns:
            json: request Response.
        """
        
        url = DESTINY2_URL + '{}/Profile/{}/?components={}'
        url = url.format(platform, destiny_membership_id,
                         ','.join([str(i) for i in components]))
        
        return await self._get_request(url)
    
    async def get_item(self, destiny_membership_id, item_instance_id, platform,
                       components: list):
        """Retrieve the details of an instanced Destiny item.
        
        An instanced Destiny item is one with and ItemInstancedId.
        Materials don't have ItemInstancedId so thet are not queryable with
        this endpoint.
        
        Args:
            destiny_membership_id (str): Destiny membership ID.
            item_instance_id (int): Instance ID of destiny item.
            platform (int): Destiny 2 membershipType.
            components (list): List of components to include in response.
                See the DestinyComponentType enum for valid components to request here,
                "https://bungie-net.github.io/multi/index.html". You must request at
                least one component to receive results. It should be either int or
                string. You must request at least one component to receive results.
                
        Returns:
            json: request Response.  
        """
        
        url = DESTINY2_URL + '{}/Profile/{}/Item/{}/?components={}'
        url = url.format(platform, destiny_membership_id, item_instance_id,
                         ','.join([str(i) for i in components]))
        
        return await self._get_request(url)
    
    async def get_activity_history(self, destiny_membership_id, character_id,
                                   platform, count=1, mode=None, page=0):
        """Returns specific character activity history.
        
        Args:
            destiny_membership_id (str): Destiny membershipId.
            character_id (int): Destiny characterId.
            platform (int): Destiny2 membershipType.
            count (int, optional): Number of rows to return. Default will return
                one last activity.
            mode (int, optional): A filter for the activity mode to be returned.
                None return all activities. See the documentation for
                'DestinyActivityModeType' for valid values.
            page (int, optional): Page number to return, starting with 0.
            
        Returns:
            json: request Response.
        """
        
        url = DESTINY2_URL + '{}/Account/{}/Character/{}/Stats/Activities/' \
                            '?count={}&mode={}&page={}'
        url = url.format(platform, destiny_membership_id, character_id, count,
                         mode, page)
        
        return await self._get_request(url)
    
    async def get_character_info(self, character_id, destiny_membership_id,
                                 platform, components: list):
        """Returns character information for the supplied character.
        
        Args:
            character_id (int): Destiny characterId.
            destiny_membership_id (int): Destiny membershipId.
            platform (int): Destiny2 membershipType.
            components (list): List of components to include in response.
                See the DestinyComponentType enum for valid components to request here,
                "https://bungie-net.github.io/multi/index.html". You must request at
                least one component to receive results. It should be either int or
                string. You must request at least one component to receive results.
                
        Returns:
            json: request Response.
        """
        
        url = DESTINY2_URL + '{}/Profile/{}/Character/{}/?components={}'
        url = url.format(platform, destiny_membership_id, character_id,
                         ','.join([str(i) for i in components]))
        
        return await self._get_request(url)
    
    async def get_destiny_clan_members(self, group_id):
        """Get Destiny2 clan members.
        
        Args:
            group_id (int): Group ID of the clan.
            member_type (int): Filter out other member types. Ex: Only Admins.
                Use None for all members.
        
        Returns:
            json: request Response.
        """
        
        url = GROUP_URL + '{}/Members/?memberType=None'
        url = url.format(group_id)
        
        return await self._get_request(url)
    
    async def get_clan_leaderboard(self, group_id, maxtop, modes, stat_id):
        """Get clan leaderboard.
        
        Args:
            group_id (int): Group ID of the clan.
            maxtop (int): Maximum number of top players to return.
                Use a large number to get entire leaderboard.
            modes (str): List of game modes for which to get leaderboars.
            stat_id (str): ID of stat to return rather than returning all
                leaderboard stats.
        
        Returns:
            json: request Response.
        """
        
        url = DESTINY2_URL + 'Stats/Leaderboards/Clans/{}/?maxtop={}&modes={}' \
            '&statid={}'
        url = url.format(group_id, maxtop, modes, stat_id)
        
        return await self._get_request(url)
    
    async def get_clan(self, group_id):
        """Get clan data.
        
        Args:
            group_id (int): Group's id.
        
        Returns:
            _get_request (json): request Response.
        """
        
        url = GROUP_URL + '{}/'
        url = url.format(group_id)

        return await self._get_request(url)
    
    async def get_clan_weekly_reward(self, group_id):
        """Get clan weekly rewards.
        
        Args:
            group_id (int): Group's id.
        
        Returns:
            _get_request (json): request Response.
        """
        
        url = DESTINY2_URL + 'Clan/{}/WeeklyRewardState/'
        url = url.format(group_id)
        
        return await self._get_request(url)
    
    async def get_activity_history(self, platform, destiny_membership_id,
                                   character_id, count, mode, page):
        """Get activity history for one character.
        
        Args:
            platform (int): Destiny2 membershipType.
            destiny_membership_id (int): Destiny membershipId.
            character_id (int): Destiny characterId.
            count (int): Number of rows to return.
            mode (int): A filter for the activity mode to be returned.
                None returns all activities. See the documentation for
                DestinyActivityModeType for valid values, and pass in string
                representation.
            page (int): Page number to return, starting with 0.
            
        Returns:
            _get_request (json): request Response.
        """

        url = DESTINY2_URL + '{}/Account/{}/Character/{}/Stats/Activities/' \
            '?count={}&mode={}&page={}'
        url = url.format(platform, destiny_membership_id, character_id, count,
                         mode, page)
        
        return await self._get_request(url)