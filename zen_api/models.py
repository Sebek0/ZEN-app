from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy import PickleType
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.mutable import MutableList, MutableDict

Base = declarative_base()

class Guardian(Base):
    __tablename__ = 'guardians'
    
    id = Column(Integer, primary_key=True, index=True)
    bungie_id = Column(String, unique=True)
    name = Column(String, unique=True)
    platform = Column(Integer, default=3)
    
    characters = relationship('Character', back_populates='guardian')
    
    
class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    guardian_id = Column(Integer, ForeignKey("guardians.id"))
    char_class = Column(String)
    last_login = Column(String)
    stats = Column(MutableDict.as_mutable(PickleType), default={})
    items = Column(MutableDict.as_mutable(PickleType), default={})
    emblemBackgroundPath = Column(String)
    emblem_name = Column(String)
    emblem_path = Column(String)
    light = Column(Integer)
    minutesPlayedTotal = Column(String)
    race_name = Column(String)
    title = Column(MutableDict.as_mutable(PickleType), default={})
    subclass = Column(MutableDict.as_mutable(PickleType), default={})

    guardian = relationship("Guardian", back_populates="characters")


class DestinyStatDefinition(Base):
    __tablename__ = 'DestinyStatDefinition'

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(Integer)
    displayProperties = Column(MutableDict.as_mutable(PickleType), default={})
    aggregationType = Column(Integer)
    hasComputedBlock = Column(String)
    statCategory = Column(Integer)
    interpolate = Column(String)
    index = Column(Integer)
    redacted = Column(String)
    blacklisted = Column(String)


class DestinySandboxPerkDefinition(Base):
    __tablename__ = 'DestinySandboxPerkDefinition'

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(Integer)
    displayProperties = Column(MutableDict.as_mutable(PickleType), default={})
    isDisplayable = Column(String)
    damageType = Column(Integer)
    index = Column(Integer)
    redacted = Column(String)
    blacklisted = Column(String)


class DestinyRecordDefinition(Base):
    __tablename__ = 'DestinyRecordDefinition'

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(Integer)
    displayProperties = Column(MutableDict.as_mutable(PickleType), default={})
    scope = Column(Integer)
    objectiveHashes = Column(MutableList.as_mutable(PickleType), default=[])
    recordValueStyle = Column(Integer)
    forTitleGilding = Column(String)
    shouldShowLargeIcons = Column(String)
    titleInfo = Column(MutableDict.as_mutable(PickleType), default={})
    completionInfo = Column(MutableDict.as_mutable(PickleType), default={})
    stateInfo = Column(MutableDict.as_mutable(PickleType), default={})
    requirements = Column(MutableDict.as_mutable(PickleType), default={})
    expirationInfo = Column(MutableDict.as_mutable(PickleType), default={})
    intervalInfo = Column(MutableDict.as_mutable(PickleType), default={})
    rewardItems = Column(MutableList.as_mutable(PickleType), default=[])
    anyRewardHasConditionalVisibility = Column(String)
    recordTypeName = Column(String)
    presentationNodeType = Column(Integer)
    traitIds = Column(MutableList.as_mutable(PickleType), default=[])
    traitHashes = Column(MutableList.as_mutable(PickleType), default=[])
    parentNodeHashes = Column(MutableList.as_mutable(PickleType), default=[])
    index = Column(Integer)
    redacted = Column(String)
    blacklisted = Column(String)


class DestinyRaceDefinition(Base):
    __tablename__ = 'DestinyRaceDefinition'

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(Integer)
    displayProperties = Column(MutableDict.as_mutable(PickleType), default={})
    raceType = Column(Integer)
    genderedRaceNames = Column(MutableDict.as_mutable(PickleType), default={})
    genderedRaceNamesByGenderHash = Column(MutableDict.as_mutable(PickleType), default={})
    index = Column(Integer)
    redacted = Column(String)
    blacklisted = Column(String)


class DestinyInventoryItemDefinition(Base):
    __tablename__ = 'DestinyInventoryItemDefinition'

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(Integer)
    displayProperties = Column(MutableDict.as_mutable(PickleType), default={})
    tooltipNotifications = Column(MutableList.as_mutable(PickleType), default=[])
    backgroundColor = Column(MutableDict.as_mutable(PickleType), default={})
    screenshot = Column(String)
    itemTypeDisplayName = Column(String)
    flavorText = Column(String)
    uiItemDisplayStyle = Column(String)
    itemTypeAndTierDisplayName = Column(String)
    displaySource = Column(String)
    action = Column(MutableDict.as_mutable(PickleType), default={})
    inventory = Column(MutableDict.as_mutable(PickleType), default={})
    stats = Column(MutableDict.as_mutable(PickleType), default={})
    equippingBlock = Column(MutableDict.as_mutable(PickleType), default={})
    translationBlock = Column(MutableDict.as_mutable(PickleType), default={})
    quality = Column(MutableDict.as_mutable(PickleType), default={})
    acquireRewardSiteHash = Column(Integer)
    acquireUnlockHash = Column(Integer)
    talentGrid = Column(MutableDict.as_mutable(PickleType), default={})
    investmentStats = Column(MutableList.as_mutable(PickleType), default=[])
    perks = Column(MutableList.as_mutable(PickleType), default=[])
    allowActions = Column(String)
    doesPostmasterPullHaveSideEffects = Column(String)
    nonTransferrable = Column(String)
    itemCategoryHashes = Column(MutableList.as_mutable(PickleType), default=[])
    specialItemType = Column(Integer)
    itemType = Column(Integer)
    itemSubType = Column(Integer)
    classType = Column(Integer)
    breakerType = Column(Integer)
    equippable = Column(String)
    defaultDamageType = Column(Integer)
    isWrapper = Column(String)
    traitIds = Column(MutableList.as_mutable(PickleType), default=[])
    traitHashes = Column(MutableList.as_mutable(PickleType), default=[])
    index = Column(Integer)
    redacted = Column(String)
    blacklisted = Column(String)


class DestinyInventoryBucketDefinition(Base):
    __tablename__ = 'DestinyInventoryBucketDefinition'

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(Integer)
    displayProperties = Column(MutableDict.as_mutable(PickleType), default={})
    scope = Column(Integer)
    category = Column(Integer)
    bucketOrder = Column(Integer)
    itemCount = Column(Integer)
    location = Column(Integer)
    hasTransferDestination = Column(String)
    enabled = Column(String)
    fifo = Column(String)
    index = Column(Integer)
    redacted = Column(String)
    blacklisted = Column(String)


class DestinyDamageTypeDefinition(Base):
    __tablename__ = 'DestinyDamageTypeDefinition'

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(Integer)
    displayProperties = Column(MutableDict.as_mutable(PickleType), default={})
    transparentIconPath = Column(String)
    showIcon = Column(String)
    enumValue = Column(Integer)
    color = Column(MutableDict.as_mutable(PickleType), default={})
    index = Column(Integer)
    redacted = Column(String)
    blacklisted = Column(String)


class DestinyClassDefinition(Base):
    __tablename__ = 'DestinyClassDefinition'

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(Integer)
    displayProperties = Column(MutableDict.as_mutable(PickleType), default={})
    classType = Column(Integer)
    genderedClassNames = Column(MutableDict.as_mutable(PickleType), default={})
    genderedClassNamesByGenderHash = Column(MutableDict.as_mutable(PickleType), default={})
    index = Column(Integer)
    redacted = Column(String)
    blacklisted = Column(String)


class DestinyActivityDefinition(Base):
    __tablename__ = 'DestinyActivityDefinition'

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(Integer)
    displayProperties = Column(MutableDict.as_mutable(PickleType), default={})
    originalDisplayProperties = Column(MutableDict.as_mutable(PickleType), default={})
    releaseIcon = Column(String)
    releaseTime = Column(Integer)
    completionUnlockHash = Column(Integer)
    activityLightLevel = Column(Integer)
    destinationHash = Column(Integer)
    placeHash = Column(Integer)
    activityTypeHash = Column(Integer)
    tier = Column(Integer)
    rewards = Column(MutableList.as_mutable(PickleType), default=[])
    modifiers = Column(MutableList.as_mutable(PickleType), default=[])
    isPlaylist = Column(String)
    challenges = Column(MutableList.as_mutable(PickleType), default=[])
    optionalUnlockStrings = Column(MutableList.as_mutable(PickleType), default=[])
    inheritFromFreeRoam = Column(String)
    suppressOtherRewards = Column(String)
    playlistItems = Column(MutableList.as_mutable(PickleType), default=[])
    matchmaking = Column(MutableDict.as_mutable(PickleType), default={})
    isPvP = Column(String)
    inserationPoints = Column(MutableList.as_mutable(PickleType), default=[])
    activityLocationMappings = Column(MutableList.as_mutable(PickleType), default=[])
    index = Column(Integer)
    redacted = Column(String)
    blacklisted = Column(String)



    


    

