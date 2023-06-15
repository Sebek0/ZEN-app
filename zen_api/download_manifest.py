import requests
import json
import os

import models

from dotenv import load_dotenv
from tqdm import tqdm

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

def check_manifest_version():
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

def download_manifest_files():
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

def create_table(table_name, manifest_path):
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

def create_manifest_tables():
    """"""
    manifest_path = f'{ROOT_PATH}/ZEN-app/zen_api/bungie_api_wrapper/Manifest/'
    manifest_files_list = os.listdir(manifest_path)

    for manifest_file in tqdm(manifest_files_list, desc=f'Creating manifest tables'):
        create_table(manifest_file, manifest_path)

def remove_manifest_files():
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

def setup_manifest_definitions():
    if not check_manifest_version():
        download_manifest_files()
        create_manifest_tables()
        remove_manifest_files()
    else:
        pass

if __name__ == '__main__':
        #setup_manifest_definitions()


