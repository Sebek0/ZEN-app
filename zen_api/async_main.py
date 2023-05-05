import asyncio
import os
import urllib
import json
import time

import aiohttp  

from dotenv import load_dotenv

#Bungie API
from bungie_api_wrapper import BAPI
from bungie_api_wrapper.manifest import Manifest

# ZEN API
from zen_api_wrapper import ZENAPI

man = Manifest() # When declaring Manifest() it will load all manifest files

load_dotenv() # Loads environment variables from .env

API_KEY = os.getenv('BUNGIE_API_KEY')


async def get_characters(destiny_membership_id: int, platform: int):
    """Return characters information in hash values.
    
    Function will return all information about User characters in hash values.
    Returned dictionary is ready to be decoded in Destiny manifest.
    
    Args:
        destiny_membership_id (int): Bungie destiny_membership_id.
        platform (int): Destiny2 membershipType.
        
    Returns:
        characters_informations (dict): Informations about characters in hash
        values.
    """

    destiny = BAPI(API_KEY)
    characters_informations = {}
    
    # get user profile from API request
    profile = await destiny.api.get_destiny_profile(destiny_membership_id,
                                                    platform, [100, 200, 205])
    
    characters_ids = profile['Response']['profile']['data']['characterIds']
    
    # POST guardian to database
    n = profile['Response']['profile']['data']['userInfo']['bungieGlobalDisplayName']
    c = profile['Response']['profile']['data']['userInfo']['bungieGlobalDisplayNameCode']
    name = f'{n}#{c}'
    plat = profile['Response']['profile']['data']['userInfo']['membershipType']

    async def character(profile, character_id):
        """Add character information in hash values to characters dictionary.
        
        Function will add all informations about single character in hash values,
        to characters dictionary. Using this function we can request character
        endpoint in the same time.
        
        Args:
            profile (dict): Informations about Bungie user profile.
            character_id (str): Destiny2 user Character ID.
        """
        
        char_data = profile['Response']['characters']['data'][character_id]
        items_data = profile['Response']['characterEquipment']['data'] \
            [character_id]['items']
        
        items = {}
        no_weapon_buckets = ['284967655', '1107761855', '1506418338', '2025709351',
                            '3683254069', '4023194814', '4292445962', '4274335291',
                            '3284755031']
        
        for i in range(len(items_data)):
            item = items_data
            try:
                if not str(item[i]['bucketHash']) in no_weapon_buckets:
                    item_raw_data = {}
                    item_resp = await destiny.api.get_item(destiny_membership_id,
                                                           item[i]['itemInstanceId'],
                                                           platform, [302, 304, 307])
                    
                    i_hash = item_resp['Response']['item']['data']['itemHash']
                    b_hash = item_resp['Response']['item']['data']['bucketHash']
                    
                    common_data = {
                        'itemHash': i_hash,
                        'bucketHash': b_hash
                    }
                    
                    item_stats = item_resp['Response']['stats']['data']['stats']
                    item_perks = item_resp['Response']['perks']['data']['perks']
                    
                    item_raw_data['common_data'] = common_data
                    item_raw_data['stats'] = item_stats
                    item_raw_data['perks'] = item_perks
                    
                    items[b_hash] = item_raw_data
            except KeyError as k_error:
                pass
                # logger.error(f'{k_error} Bucket: {item[i]["bucketHash"]} \
                #       Item: {item[i]["itemHash"]} Class: {char_data["classHash"]} \
                #           ItemInstanceId: {item[i]["itemInstanceId"]}')
        
        characters_informations[char_data['classHash']] = {
            'dateLastPlayed': char_data['dateLastPlayed'],
            'emblemBackgroundPath': char_data['emblemBackgroundPath'],
            'emblemHash': char_data['emblemHash'],
            'emblemPath': char_data['emblemPath'],
            'light': char_data['light'],
            'minutesPlayedTotal': char_data['minutesPlayedTotal'],
            'raceHash': char_data['raceHash'],
            'stats': char_data['stats'],
            'items': items
        }
    
    await asyncio.gather(
        *[character(profile, char_id) for char_id in characters_ids]
    )
    decoded_character = man.decode_characters_from_manifest(characters_informations)
 
    await add_guardian_to_db(destiny_membership_id, name, plat, decoded_character)
    await destiny.close()
    
    return decoded_character
    
async def add_guardian_to_db(bungie_id: str, name: str, platform: int,
                             decoded_characters_data: dict):
    zen = ZENAPI()
    
    guardian_payload = {
        'bungie_id': bungie_id,
        'name': name,
        'platform': platform
    }
    await zen.api.post_create_guardian(payload=guardian_payload) # Adding new guardian to database
    
    db_id = await zen.api.get_guardian_db_id(str(bungie_id)) # Find Id in database of newly created guardian
    
    for char, value in decoded_characters_data.items():
        char_payload = {
            'char_class': char,
            'last_login': value['dateLastPlayed'],
            'emblemBackgroundPath': value['emblemBackgroundPath'],
            'emblem_name': value['emblemName'],
            'emblem_path': value['emblemPath'],
            'light': value['light'],
            'minutesPlayedTotal': value['minutesPlayedTotal'],
            'race_name': value['raceName'],
            'stats': value['stats'],
            'items': value['items'],
            'title': 'Reckoner'
        }        
        await zen.api.post_create_character(db_id, payload=char_payload)
    await zen.close()

async def main(destiny_membership_ids: int):
    # Asynchronous context manager
    async with aiohttp.ClientSession() as session:
        profiles = []
        for destiny_membership_id in destiny_membership_ids:
            profiles.append(get_characters(
                                destiny_membership_id=destiny_membership_id,
                                platform=3
                                ))
        htmls = await asyncio.gather(*profiles, return_exceptions=True)
        return htmls

if __name__ == '__main__':
    destiny_membership_ids = [4611686018476581013, 4611686018476934649, 4611686018471751284,
4611686018468563973, 4611686018468563973, 4611686018483897586]  # ...
    start_time = time.time()
    asyncio.run(main(destiny_membership_ids))  
    print("--- %s seconds ---" % (time.time() - start_time))
