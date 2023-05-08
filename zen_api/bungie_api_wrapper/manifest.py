import requests
import json
import os
import logging

from dotenv import load_dotenv
from tqdm import tqdm

logger = logging.getLogger('bungie_wrapper')


class Manifest:
    def __init__(self, version_check: bool = False) -> None:
        load_dotenv()
        
        self.version_check = version_check
        self.manifest_url = os.getenv('MANIFEST_URL')
        self.api_key = os.getenv('BUNGIE_API_KEY')
        self.project_dir = os.getenv('PROJECT_DIR')
        
        if not version_check:
            # Class manifest file
            with open(rf'{self.project_dir}/ZEN-app/zen_api/bungie_api_wrapper/Manifest/DestinyClassDefinition.json') as class_man:
                self.class_manifest = json.load(class_man)
                print('Loaded Manifest1')
            # Race manifest file
            with open(rf'{self.project_dir}/ZEN-app/zen_api/bungie_api_wrapper/Manifest/DestinyRaceDefinition.json') as race_man:
                self.race_manifest = json.load(race_man)
                print('Loaded Manifest2')
            # Items manifest file
            with open(rf'{self.project_dir}/ZEN-app/zen_api/bungie_api_wrapper/Manifest/DestinyInventoryItemDefinition.json') as item_man:
                self.item_manifest = json.load(item_man)
                print('Loaded Manifest3')
            # Bucket manifest file
            with open(rf'{self.project_dir}/ZEN-app/zen_api/bungie_api_wrapper/Manifest/DestinyInventoryBucketDefinition.json') as bucket_man:
                self.bucket_manifest = json.load(bucket_man)
                print('Loaded Manifest4')
            # Item stats manifest file
            with open(rf'{self.project_dir}/ZEN-app/zen_api/bungie_api_wrapper/Manifest/DestinyStatDefinition.json') as stat_man:
                self.stat_manifest = json.load(stat_man)
                print('Loaded Manifest5')
            # Damage type manifest file
            with open(rf'{self.project_dir}/ZEN-app/zen_api/bungie_api_wrapper/Manifest/DestinyDamageTypeDefinition.json') as damage_man:
                self.damage_manifest = json.load(damage_man)
                print('Loaded Manifest6')
            # Item perks manifest file
            with open(rf'{self.project_dir}/ZEN-app/zen_api/bungie_api_wrapper/Manifest/DestinySandboxPerkDefinition.json') as perk_man:
                self.perk_manifest = json.load(perk_man) 
                print('Loaded Manifest7')
            with open(rf'{self.project_dir}/ZEN-app/zen_api/bungie_api_wrapper/Manifest/DestinyRecordDefinition.json') as record_man:
                self.record_manifest = json.load(record_man)
                print('Loaded Manifest8')
        
    def check_manifest(self):
        """Check manifest files and manifest version.
        
        Function is checking if directiory with essential manifest files exists.
        If not it will create new directory and save new files there. If directory
        already exists function will check if version saved on machine is the same
        in Bungie API. If not it will update outdated version.
        """
        
        if not os.path.isdir(rf'{self.project_dir}/ZEN-app/zen_api/bungie_api_wrapper/Manifest'):
            self.get_manifest_files()
        elif not os.path.isfile(rf'{self.project_dir}/ZEN-app/zen_api/bungie_api_wrapper/Manifest/version.json'):
            self.get_manifest_files()
        else:
            get_manifest = requests.get(self.manifest_url)
            manifest_data = get_manifest.json()
            with open(rf'{self.project_dir}/ZEN-app/zen_api/bungie_api_wrapper/Manifest/version.json') as v_file:
                version_data = json.load(v_file)
                version = version_data['version']
            if version != str(manifest_data['Response']['version']):
                logger.info('Manifest version is outdated! Fetching new version...')
                self.get_manifest_files()
                if os.path.isfile(rf'{self.project_dir}/ZEN-app/zen_api/bungie_api_wrapper/Manifest/version.json'):
                    logger.info('Downloading complete, version is up to date.')
                else:
                    logger.error('Unexpected error while downloading new version!')
            else:
                logger.info('Manifest version is up to date!')
    
    def get_manifest_files(self):
        
        def download_manifest_files():
            """Download and save manifest definition files."""
            
            headers = {'X-API-Key': str(self.api_key)}
            get_manifest = requests.get(url=self.manifest_url, headers=headers)
            
            manifest_data = get_manifest.json()
            definition_keys = ['DestinyInventoryItemDefinition',
                                'DestinyInventoryBucketDefinition',
                                'DestinyDamageTypeDefinition',
                                'DestinyStatDefinition',
                                'DestinySandboxPerkDefinition',
                                'DestinyClassDefinition',
                                'DestinyRaceDefinition',
                                'DestinyActivityDefinition',
                                'DestinyRecordDefinition']
            
            for definition in tqdm(definition_keys, desc='Fetching manifest files'):
                download_manifest_url = 'http://www.bungie.net' + \
                    manifest_data['Response']['jsonWorldComponentContentPaths']['en'] \
                        [definition]
                response = requests.get(download_manifest_url)
                json_data = json.loads(response.text)
                with open(rf'{self.project_dir}/ZEN-app/zen_api/bungie_api_wrapper/Manifest/{definition}.json', 'w') as j_file:
                    json.dump(json_data, fp=j_file)
            
            version = manifest_data['Response']['version']
            with open(rf'{self.project_dir}/ZEN-app/zen_api/bungie_api_wrapper/Manifest/version.json', 'w') as v_file:
                json.dump({'version': version}, fp=v_file)
        
        if not os.path.isdir(r'bungie_api_wrapper/Manifest'):
            os.mkdir(rf'{self.project_dir}/ZEN-app/zen_api/bungie_api_wrapper/Manifest/')
            download_manifest_files()
        else:
            download_manifest_files()
            
    def decode_characters_from_manifest(self, characters_data: dict) -> dict:
        """Decode all characters informations using manifest json files.
        
        Function is using multiple json files requested from Bungie API endpoint,
        to decode character, items, hashes and create new decoded dictionary.
        
        Args:
            characters_data (dict): Destiny2 characters hash values.
        
        Returns:
            characters (dict): Decoded hash values from characters_data.
        """
        
        characters = {}
        try:
            for character in characters_data.keys():

                class_name = self.class_manifest[str(character)]['displayProperties']['name']
                
                race_hash = characters_data[character]['raceHash']
                race_name = self.race_manifest[str(race_hash)]['displayProperties']['name']
                
                emblem_hash = characters_data[character]['emblemHash']
                emblem_name = self.item_manifest[str(emblem_hash)]['displayProperties']['name']
                
                title_hash = characters_data[character]['title']
                title_data = {
                    'name': self.record_manifest[str(title_hash)]['displayProperties']['name'],
                    'description': self.record_manifest[str(title_hash)]['displayProperties']['description'],
                    'icon': self.record_manifest[str(title_hash)]['displayProperties']['icon']
                }
                print(title_data)
                
                subclass_hash = characters_data[character]['subclass']
                subclass_data = {
                    'name': self.item_manifest[str(subclass_hash)]['displayProperties']['name'],
                    'icon': self.item_manifest[str(subclass_hash)]['displayProperties']['icon']
                }
                print(subclass_data)
                
                character_stat = {}
                for s_hash, s_value in characters_data[character]['stats'].items():
                    stat_name = self.stat_manifest[s_hash]['displayProperties']['name']
                    
                    character_stat[stat_name] = s_value
            
                items_details = {}
                for v in characters_data[character]['items'].values():
                    item_hash = str(v['common_data']['itemHash'])
                    
                    item_name = self.item_manifest[item_hash]['displayProperties']['name']
                    item_icon = self.item_manifest[item_hash]['displayProperties']['icon']
                    if not 'iconWatermark' in self.item_manifest[item_hash].keys():
                        item_watermark = None
                    else:
                        item_watermark = self.item_manifest[item_hash]['iconWatermark']
                    
                    
                    bucket_hash = str(v['common_data']['bucketHash'])
                    bucket_name = self.bucket_manifest[bucket_hash]['displayProperties']['name']
                
                    item_stats = {}
                    for stat in v['stats'].values():
                        stat_hash = str(stat['statHash'])
                        stat_value = str(stat['value'])
                        
                        if not 'icon' in self.stat_manifest[stat_hash]['displayProperties'].keys():
                            stat_name = self.stat_manifest[stat_hash]['displayProperties']['name']
                            stat_icon = None
                        else:
                            stat_name = self.stat_manifest[stat_hash]['displayProperties']['name']
                            stat_icon = self.stat_manifest[stat_hash]['displayProperties']['icon']
                        
                        item_stats[stat_name] = {
                            'value': stat_value,
                            'icon': stat_icon
                        }
                    
                    item_perks = {}
                    for perk in v['perks']:
                        perk_hash = str(perk['perkHash'])
                        perk_data = self.perk_manifest[perk_hash]
                        
                        if perk_data['damageType'] != 0:
                            dmg_type_hash = str(perk_data['damageTypeHash'])
                            dmg_type = self.damage_manifest[dmg_type_hash]
                            dmg_type_name = dmg_type['displayProperties']['name']
                            dmg_type_icon = dmg_type['displayProperties']['icon']
                            
                            item_perks['damage_type'] = {
                                'name': dmg_type_name,
                                'icon': dmg_type_icon
                            }
                        elif perk_data['isDisplayable'] is True:
                            perk_name = perk_data['displayProperties']['name']
                            perk_icon = perk_data['displayProperties']['icon']

                            item_perks[perk_name] = {
                                'name': perk_name,
                                'icon': perk_icon
                            }
                    items_details[bucket_name] = {
                        'common_data': {
                            'item_name': item_name,
                            'item_bucket': bucket_name,
                            'item_icon': item_icon,
                            'item_watermark': item_watermark
                        },
                        'perks': item_perks,
                        'stats': item_stats
                    }
                    
                char = characters_data[character]
                characters[class_name] = {
                    'dateLastPlayed': char['dateLastPlayed'],
                    'emblemBackgroundPath': char['emblemBackgroundPath'],
                    'emblemPath': char['emblemPath'],
                    'emblemName': emblem_name,
                    'light': char['light'],
                    'minutesPlayedTotal': char['minutesPlayedTotal'],
                    'raceName': race_name,
                    'title': title_data,
                    'subclass': subclass_data,
                    'stats': character_stat,
                    'items': items_details                        
                    }
                
        except KeyError as key_error:
            logger.error(f'{key_error} in characters manifest function.')
        except ValueError as value_error:
            logger.error(f'{value_error} in characters manifest function.')
            
        return characters
    
def main():
    manifest = Manifest(version_check=True)
    manifest.check_manifest()
    logger.info('Manifest has been downloaded')
    
if __name__ == '__main__':
    main()