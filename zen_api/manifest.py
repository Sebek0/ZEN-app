import requests
import json
import os
import logging
import time

import models

from dotenv import load_dotenv
from tqdm import tqdm

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger('bungie_wrapper')

load_dotenv()

API_KEY = os.getenv('BUNGIE_API_KEY')
MANIFEST_URL = os.getenv('MANIFEST_URL')
ROOT_PATH = os.getenv('ROOT_PATH')

engine = create_engine("sqlite:///./Manifestdb.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()

tables = [models.DestinyStatDefinition, models.DestinySandboxPerkDefinition,
          models.DestinyRaceDefinition, models.DestinyRecordDefinition,
          models.DestinyInventoryItemDefinition, models.DestinyInventoryBucketDefinition,
          models.DestinyDamageTypeDefinition, models.DestinyClassDefinition,
          models.DestinyActivityDefinition, models.ManifestVersion]
for table in tables:
    table.__table__.create(bind=engine, checkfirst=True)

class Manifest:
    def __init__(self) -> None:
        pass

    def check_manifest_version(self):
        """"""

        headers = {'X-API-Key': str(API_KEY)}
        get_manifest = requests.get(url=str(MANIFEST_URL), headers=headers)

        manifest_data = get_manifest.json()
        query = db.query(models.ManifestVersion.version).first()
        if query is not None:
            current_version = str(query.version)
        else:
            current_version = 'Undefined'

        if manifest_data['Response']['version'] == current_version:
            return True
        else:
            return False

    def download_manifest_files(self):
        """Download and save manifest definition files."""

        headers = {'X-API-Key': str(API_KEY)}
        get_manifest = requests.get(url=str(MANIFEST_URL), headers=headers)

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

        if not os.path.exists(f'{ROOT_PATH}/ZEN-app/zen_api/bungie_api_wrapper/Manifest'):
            os.mkdir(f'{ROOT_PATH}/ZEN-app/zen_api/bungie_api_wrapper/Manifest')

        for definition in tqdm(definition_keys, desc='Fetching manifest files'):
            download_manifest_url = 'http://www.bungie.net' + \
                manifest_data['Response']['jsonWorldComponentContentPaths']['en'][definition]
            response = requests.get(download_manifest_url)
            json_data = json.loads(response.text)
            with open(f'{ROOT_PATH}/ZEN-app/zen_api/bungie_api_wrapper/Manifest/{definition}.json', 'w') as file:
                json.dump(json_data, fp=file)
            
            version = manifest_data['Response']['version']
            with open(f'{ROOT_PATH}/ZEN-app/zen_api/bungie_api_wrapper/Manifest/version.json', 'w') as version_file:
                json.dump({'version': version}, fp=version_file)

    def create_table(self, table_name, manifest_path):
        """"""
        f = manifest_path+table_name
        with open(f, 'r') as file:
            data = json.load(file)

        match table_name:
            case 'DestinyStatDefinition.json':
                for value in data.values():
                    definition = models.DestinyStatDefinition(
                        hash=value.get('hash', None),
                        displayProperties=value.get('displayProperties', None),
                        aggregationType=value.get('aggregationType', None),
                        hasComputedBlock=value.get('hasComputedBlock', None),
                        statCategory=value.get('statCategory', None),
                        interpolate=value.get('interpolate', None),
                        index=value.get('index', None),
                        redacted=value.get('redacted', None),
                        blacklisted=value.get('blacklisted', None),
                    )
                    db.add(definition)
                db.commit()
            case 'DestinySandboxPerkDefinition.json':
                for value in data.values():
                    definition = models.DestinySandboxPerkDefinition(
                        hash=value.get('hash', None),
                        displayProperties=value.get('displayProperties', None),
                        isDisplayable=value.get('isDisplayable', None),
                        damageType=value.get('damageType', None),
                        damageTypeHash=value.get('damageTypeHash', None),
                        index=value.get('index', None),
                        redacted=value.get('redacted', None),
                        blacklisted=value.get('blacklisted', None),
                    )
                    db.add(definition)
                db.commit()
            case 'DestinyRecordDefinition.json':
                for value in data.values():
                    definition = models.DestinyRecordDefinition(
                        hash=value.get('hash', None),
                        displayProperties=value.get('displayProperties', None),
                        scope=value.get('scope', None),
                        objectiveHashes=value.get('objectiveHashes', None),
                        recordValueStyle=value.get('recordValueStyle', None),
                        forTitleGilding=value.get('forTitleGilding', None),
                        shouldShowLargeIcons=value.get('shouldShowLargeIcons', None),
                        titleInfo=value.get('titleInfo', None),
                        completionInfo=value.get('completionInfo', None),
                        stateInfo=value.get('stateInfo', None),
                        requirements=value.get('requirements', None),
                        expirationInfo=value.get('expirationInfo', None),
                        intervalInfo=value.get('intervalInfo', None),
                        rewardItems=value.get('rewardItems', None),
                        anyRewardHasConditionalVisibility=value.get('anyRewardHasConditionalVisibility', None),
                        recordTypeName=value.get('recordTypeName', None),
                        presentationNodeType=value.get('presentationNodeType', None),
                        traitIds=value.get('traitIds', None),
                        traitHashes=value.get('traitHashes', None),
                        parentNodeHashes=value.get('parentNodeHashes', None),
                        index=value.get('index', None),
                        redacted=value.get('redacted', None),
                        blacklisted=value.get('blacklisted', None),
                    )
                    db.add(definition)
                db.commit()
            case 'DestinyRaceDefinition.json':
                for value in data.values():
                    definition = models.DestinyRaceDefinition(
                        hash=value.get('hash', None),
                        displayProperties=value.get('displayProperties', None),
                        raceType=value.get('raceType', None),
                        genderedRaceNames=value.get('genderedRaceNames', None),
                        genderedRaceNamesByGenderHash=value.get('genderedRaceNamesByGenderHash', None),
                        index=value.get('index', None),
                        redacted=value.get('redacted', None),
                        blacklisted=value.get('blacklisted', None),
                    )
                    db.add(definition)
                db.commit()
            case 'DestinyInventoryItemDefinition.json':
                for value in data.values():
                    definition = models.DestinyInventoryItemDefinition(
                        hash=value.get('hash', None),
                        displayProperties=value.get('displayProperties', None),
                        tooltipNotifications=value.get('tooltipNotifications', None),
                        backgroundColor=value.get('backgroundColor', None),
                        screenshot=value.get('screenshot', None),
                        itemTypeDisplayName=value.get('itemTypeDisplayName', None),
                        flavorText=value.get('flavorText', None),
                        uiItemDisplayStyle=value.get('uiItemDisplayStyle', None),
                        itemTypeAndTierDisplayName=value.get('itemTypeAndTierDisplayName', None),
                        displaySource=value.get('displaySource', None),
                        action=value.get('action', None),
                        inventory=value.get('inventory', None),
                        stats=value.get('stats', None),
                        equippingBlock=value.get('equippingBlock', None),
                        translationBlock=value.get('translationBlock', None),
                        quality=value.get('quality', None),
                        iconWatermark=value.get('iconWatermark', None),
                        acquireRewardSiteHash=value.get('acquireRewardSiteHash', None),
                        acquireUnlockHash=value.get('acquireUnlockHash', None),
                        talentGrid=value.get('talentGrid', None),
                        investmentStats=value.get('investmentStats', None),
                        perks=value.get('perks', None),
                        allowActions=value.get('allowActions', None),
                        doesPostmasterPullHaveSideEffects=value.get('doesPostmasterPullHaveSideEffects', None),
                        nonTransferrable=value.get('nonTransferrable', None),
                        itemCategoryHashes=value.get('itemCategoryHashes', None),
                        specialItemType=value.get('specialItemType', None),
                        itemType=value.get('itemType', None),
                        itemSubType=value.get('itemSubType', None),
                        classType=value.get('classType', None),
                        breakerType=value.get('breakerType', None),
                        equippable=value.get('equippable', None),
                        defaultDamageType=value.get('defaultDamageType', None),
                        isWrapper=value.get('isWrapper', None),
                        traitIds=value.get('traitIds', None),
                        traitHashes=value.get('traitHashes', None),
                        index=value.get('index', None),
                        redacted=value.get('redacted', None),
                        blacklisted=value.get('blacklisted', None),
                    )
                    db.add(definition)
                db.commit()
            case 'DestinyInventoryBucketDefinition.json':
                for value in data.values():
                    definition = models.DestinyInventoryBucketDefinition(
                        hash=value.get('hash', None),
                        displayProperties=value.get('displayProperties', None),
                        scope=value.get('scope', None),
                        category=value.get('category', None),
                        bucketOrder=value.get('bucketOrder', None),
                        itemCount=value.get('itemCount', None),
                        location=value.get('location', None),
                        hasTransferDestination=value.get('hasTransferDestination', None),
                        enabled=value.get('enabled', None),
                        fifo=value.get('fifo', None),
                        index=value.get('index', None),
                        redacted=value.get('redacted', None),
                        blacklisted=value.get('blacklisted', None),
                    )
                    db.add(definition)
                db.commit()
            case 'DestinyDamageTypeDefinition.json':
                for value in data.values():
                    definition = models.DestinyDamageTypeDefinition(
                        hash=value.get('hash', None),
                        displayProperties=value.get('displayProperties', None),
                        transparentIconPath=value.get('transparentIconPath', None),
                        showIcon=value.get('showIcon', None),
                        enumValue=value.get('enumValue', None),
                        color=value.get('color', None),
                        index=value.get('index', None),
                        redacted=value.get('redacted', None),
                        blacklisted=value.get('blacklisted', None),
                    )
                    db.add(definition)
                db.commit()
            case 'DestinyClassDefinition.json':
                for value in data.values():
                    definition = models.DestinyClassDefinition(
                        hash=value.get('hash', None),
                        displayProperties=value.get('displayProperties', None),
                        classType=value.get('classType', None),
                        genderedClassNames=value.get('genderedClassNames', None),
                        genderedClassNamesByGenderHash=value.get('genderedClassNamesByGenderHash', None),
                        index=value.get('index', None),
                        redacted=value.get('redacted', None),
                        blacklisted=value.get('blacklisted', None),
                    )
                    db.add(definition)
                db.commit()
            case 'DestinyActivityDefinition.json':
                for value in data.values():
                    definition = models.DestinyActivityDefinition(
                        hash=value.get('hash', None),
                        displayProperties=value.get('displayProperties', None),
                        originalDisplayProperties=value.get('originalDisplayProperties', None),
                        releaseIcon=value.get('releaseIcon', None),
                        releaseTime=value.get('releaseTime', None),
                        completionUnlockHash=value.get('completionUnlockHash', None),
                        activityLightLevel=value.get('activityLightLevel', None),
                        destinationHash=value.get('destinationHash', None),
                        placeHash=value.get('placeHash', None),
                        activityTypeHash=value.get('activityTypeHash', None),
                        tier=value.get('tier', None),
                        rewards=value.get('rewards', None),
                        modifiers=value.get('modifiers', None),
                        isPlaylist=value.get('isPlaylist', None),
                        challenges=value.get('challenges', None),
                        optionalUnlockStrings=value.get('optionalUnlockStrings', None),
                        inheritFromFreeRoam=value.get('inheritFromFreeRoam', None),
                        suppressOtherRewards=value.get('suppressOtherRewards', None),
                        playlistItems=value.get('playlistItems', None),
                        matchmaking=value.get('matchmaking', None),
                        isPvP=value.get('isPvP', None),
                        inserationPoints=value.get('inserationPoints', None),
                        activityLocationMappings=value.get('activityLocationMappings', None),
                        index=value.get('index', None),
                        redacted=value.get('redacted', None),
                        blacklisted=value.get('blacklisted', None),
                    )
                    db.add(definition)
                db.commit()
            case 'version.json':
                version = models.ManifestVersion(
                    version=data.get('version', None)
                )
                db.add(version)
                db.commit()
            case _:
                return "Not valid manifest definition"
        db.close()

    def create_manifest_tables(self):
        """"""
        manifest_path = f'{ROOT_PATH}/ZEN-app/zen_api/bungie_api_wrapper/Manifest/'
        manifest_files_list = os.listdir(manifest_path)

        for manifest_file in tqdm(manifest_files_list, desc=f'Creating manifest tables'):
            self.create_table(manifest_file, manifest_path)

    def remove_manifest_files(self):
        definition_keys = ['DestinyInventoryItemDefinition',
                            'DestinyInventoryBucketDefinition',
                            'DestinyDamageTypeDefinition',
                            'DestinyStatDefinition',
                            'DestinySandboxPerkDefinition',
                            'DestinyClassDefinition',
                            'DestinyRaceDefinition',
                            'DestinyActivityDefinition',
                            'DestinyRecordDefinition',
                            'version']

        if os.path.exists(f'{ROOT_PATH}/ZEN-app/zen_api/bungie_api_wrapper/Manifest'):
            for definition in tqdm(definition_keys, desc='Removing manifest files'):
                os.remove(f'{ROOT_PATH}/ZEN-app/zen_api/bungie_api_wrapper/Manifest/{definition}.json')

    def setup_manifest_definitions(self):
        if not self.check_manifest_version():
            self.download_manifest_files()
            self.create_manifest_tables()
            self.remove_manifest_files()
        else:
            pass

    def decode_characters_from_manifest(self, characters_data: dict) -> dict:
        """Decode all characters informations using manifest json files.
        
        Function is using multiple json files requested from Bungie API endpoint,
        to decode character, items, hashes and create new decoded dictionary.
        
        Args:
            characters_data (dict): Destiny2 characters hash values.
        
        Returns:
            characters (dict): Decoded hash values from characters_data.
        """
        
        start_time = time.time()
        
        time.sleep(0.05)
        db = SessionLocal()
        characters = {}
        try:
            for character in characters_data.keys():

                class_query = db.query(models.DestinyClassDefinition).filter(models.DestinyClassDefinition.hash == character).first()
                class_name = class_query.displayProperties.get('name', 'No name')
                
                race_hash = characters_data[character]['raceHash']
                race_query = db.query(models.DestinyRaceDefinition).filter(models.DestinyRaceDefinition.hash == race_hash).first()
                race_name = race_query.displayProperties.get('name', 'No name')
                
                emblem_hash = characters_data[character]['emblemHash']
                emblem_query = db.query(models.DestinyInventoryItemDefinition).filter(models.DestinyInventoryItemDefinition.hash == emblem_hash).first()
                emblem_name = emblem_query.displayProperties.get('name', 'No name')
                
                if characters_data[character].get('title'):
                    title_hash = characters_data[character]['title']
                    title_query = db.query(models.DestinyRecordDefinition).filter(models.DestinyRecordDefinition.hash == title_hash).first()
                    title_data = {
                        'name': title_query.displayProperties.get('name', 'No name'),
                        'description': title_query.displayProperties.get('description', 'No description'),
                        'icon': title_query.displayProperties.get('icon', 'No icon')
                    }
                else:
                    title_data = {
                        'name': None,
                        'description': 'No description',
                        'icon': 'No icon'
                    }
            
                subclass_hash = characters_data[character]['subclass']
                subclass_query = db.query(models.DestinyInventoryItemDefinition).filter(models.DestinyInventoryItemDefinition.hash == subclass_hash).first()
                subclass_data = {
                    'name': subclass_query.displayProperties.get('name', 'No name'),
                    'icon': subclass_query.displayProperties.get('icon', 'No icon')
                }
                
                character_stat = {}
                for s_hash, s_value in characters_data[character]['stats'].items():
                    stat_query = db.query(models.DestinyStatDefinition).filter(models.DestinyStatDefinition.hash == s_hash).first()
                    stat_name = stat_query.displayProperties.get('name', 'No name')
                    stat_icon = stat_query.displayProperties.get('icon', 'No icon')

                    stat_data = {
                        'icon': stat_icon,
                        'value': s_value
                    }
                    character_stat[stat_name] = stat_data

                items_details = {}
                for v in characters_data[character]['items'].values():
                    item_hash = v['common_data']['itemHash']

                    item_query = db.query(models.DestinyInventoryItemDefinition).filter(models.DestinyInventoryItemDefinition.hash == item_hash).first()
                    item_name = item_query.displayProperties.get('name', 'No name')
                    item_icon = item_query.displayProperties.get('icon', 'No icon')

                    if not item_query.iconWatermark:
                        item_watermark = None
                    else:
                        item_watermark = item_query.iconWatermark
                    
                    bucket_hash = v['common_data']['bucketHash']
                    bucket_query = db.query(models.DestinyInventoryBucketDefinition).filter(models.DestinyInventoryBucketDefinition.hash == bucket_hash).first()
                    bucket_name = bucket_query.displayProperties.get('name', 'No name')
                
                    item_stats = {}
                    for stat in v['stats'].values():
                        stat_hash = stat['statHash']
                        stat_value = stat['value']

                        stat_query = db.query(models.DestinyStatDefinition).filter(models.DestinyStatDefinition.hash == stat_hash).first()

                        stat_name = stat_query.displayProperties.get('name', 'No name')
                        stat_icon = stat_query.displayProperties.get('icon', 'No icon')
                        
                        item_stats[stat_name] = {
                            'value': stat_value,
                            'icon': stat_icon
                        }
                    
                    item_perks = {}
                    for perk in v['perks']:
                        perk_hash = perk['perkHash']
                        
                        perk_query = db.query(models.DestinySandboxPerkDefinition).filter(models.DestinySandboxPerkDefinition.hash == perk_hash).first()
                        
                        if perk_query.damageType != 0:
                            dmg_type_hash = perk_query.damageTypeHash
                            damage_type = db.query(models.DestinyDamageTypeDefinition).filter(models.DestinyDamageTypeDefinition.hash == dmg_type_hash).first()
                            dmg_type_name = damage_type.displayProperties.get('name', 'No name')
                            dmg_type_icon = damage_type.displayProperties.get('icon', 'No icon')
                            
                            item_perks['damage_type'] = {
                                'name': dmg_type_name,
                                'icon': dmg_type_icon
                            }
                        elif perk_query.isDisplayable == '1':
                            perk_name = perk_query.displayProperties.get('name', 'No name')
                            perk_icon = perk_query.displayProperties.get('icon', 'No icon')

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
            db.close()
            print("--- %s seconds ---" % (time.time() - start_time))
        except KeyError as key_error:
            logger.error(f'{key_error} in characters manifest function.')
        except ValueError as value_error:
            logger.error(f'{value_error} in characters manifest function.')
            
        return characters

if __name__ == '__main__':
    manifest = Manifest()
    manifest.setup_manifest_definitions()