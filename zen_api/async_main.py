import asyncio
import os
import urllib
import json
import time

import aiohttp  # pip install aiohttp aiodns

from dotenv import load_dotenv

load_dotenv()

bungie_key = os.getenv('BUNGIE_API_KEY')

async def get(
    session: aiohttp.ClientSession,
    bungie_id: int,
    membershipType: int,
    **kwargs
) -> dict:
    ################### GET PROFILE FROM BUNGIE ##################################
    url = f"https://www.bungie.net/Platform/Destiny2/{membershipType}/Profile/{bungie_id}/?components=100"
    headers = {'X-API-Key': str(bungie_key)}
    encoded_url = urllib.parse.quote(url, safe=':/?&=,.')
    
    print(f"Requesting {url}")
    response = await session.get(url=encoded_url, headers=headers, **kwargs)
    data = await response.json()
    print(f"Received data for {url}")
    
    ##################  GET CHARACTER FROM BUNGIE #############################
    characterId = data['Response']['profile']['data']['characterIds']
    characters = {}
    characters_coro = []
    
    for char in characterId:
        character_url = f"https://www.bungie.net/Platform/Destiny2/{membershipType}/Profile/{bungie_id}/Character/{char}/?components=200"
        encoded_url = urllib.parse.quote(character_url, safe=':/?&=,.')
        character_response = await session.get(url=encoded_url, headers=headers, **kwargs)
        character = await character_response.json()
        characters_coro.append(character)
        print(character["Response"]["character"]["data"]["characterId"])
        
        characters[char] = {
            'characterId': character['Response']['character']['data']['characterId'],
            'dateLastPlayed': character['Response']['character']['data']['dateLastPlayed']
        }
        
    print(characters)
    return characters_coro


async def main(bungie_ids, **kwargs):
    # Asynchronous context manager.  Prefer this rather
    # than using a different session for each GET request
    async with aiohttp.ClientSession() as session:
        profiles = []
        for bungie_id in bungie_ids:
            profiles.append(get(session=session, bungie_id=bungie_id, membershipType=3,
                                **kwargs))
        # asyncio.gather() will wait on the entire task set to be
        # completed.  If you want to process results greedily as they come in,
        # loop over asyncio.as_completed()
        htmls = await asyncio.gather(*profiles, return_exceptions=True)
        return htmls


if __name__ == '__main__':
    colors = [4611686018468563973, 4611686018468563973, 4611686018468563973,
              4611686018468563973, 4611686018468563973, 4611686018468563973,
              4611686018468563973, 4611686018468563973, 4611686018468563973]  # ...
    # Either take colors from stdin or make some default here
    start_time = time.time()
    asyncio.run(main(colors))  # Python 3.7+
    print("--- %s seconds ---" % (time.time() - start_time))
