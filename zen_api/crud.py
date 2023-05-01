from sqlalchemy.orm import Session

from . import models, schemas

############################## GUARDIANS ##########################################
####################################################################################
def create_guardian(db: Session, guardian: schemas.GuardianCreate):
    db_guardian = models.Guardian(
        bungie_id=guardian.bungie_id,
        name=guardian.name,
        platform=guardian.platform
    )
    db.add(db_guardian)
    db.commit()
    db.refresh(db_guardian)
    return db_guardian

def get_guardian(db: Session, guardian_id: int):
    return db.query(models.Guardian).filter(models.Guardian.id == guardian_id).first()

def get_guardians(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Guardian).offset(skip).limit(limit).all()

def get_guardian_by_bungie_id(db: Session, bungie_id: str):
    return db.query(models.Guardian).filter(models.Guardian.bungie_id == bungie_id).first()

def get_guardian_by_name(db: Session, name: str):
    return db.query(models.Guardian).filter(models.Guardian.name == name).first()

def get_guardian_by_character_id(db: Session, character_id: int):
    return db.query(models.Guardian).filter(models.Character.char_id == character_id).first()

def get_guardian_id_by_bungie_id(db: Session, bungie_id: str):
    return db.query(models.Guardian).filter(models.Guardian.bungie_id == bungie_id).first().id

def get_guardians_by_platform(db: Session, platform: int):
    return db.query(models.Guardian).filter(models.Guardian.platform == platform).all()

def delete_guardian(db: Session, guardian_id: int):
    db_guardian = db.query(models.Guardian).filter(models.Guardian.id == guardian_id).first()
    db_characters = db.query(models.Character).filter(models.Character.guardian_id == guardian_id).all()
    for db_character in db_characters:
        db.delete(db_character)
        db.commit()
    db.delete(db_guardian)
    db.commit()
    return db_guardian

def delete_guardian_by_bungie_id(db: Session, bungie_id: str):
    db_guardian = db.query(models.Guardian).filter(models.Guardian.bungie_id == bungie_id).first()
    db.delete(db_guardian)
    db.commit()
    return db_guardian

def delete_guardian_by_name(db: Session, name: str):
    db_guardian = db.query(models.Guardian).filter(models.Guardian.name == name).first()
    db.delete(db_guardian)
    db.commit()
    return db_guardian

############################## CHARACTERS ##########################################
####################################################################################
def create_character(db: Session, character: schemas.CharacterCreate, guardian_id: int):
    db_character = models.Character(**character.dict(), guardian_id=guardian_id)
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character

def get_character(db: Session, character_id: int):
    return db.query(models.Character).filter(models.Character.id == character_id).first()

def get_characters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Character).offset(skip).limit(limit).all()

def get_characters_by_class(db: Session, class_name: str):
    return db.query(models.Character).filter(models.Character.char_class == class_name).all()

def get_characters_by_guardian_id(db: Session, guardian_id: int):
    return db.query(models.Character).filter(models.Character.guardian_id == guardian_id).all()

def get_characters_by_title(db: Session, title: str):
    return db.query(models.Character).filter(models.Character.title == title).all()

def get_characters_by_race_name(db: Session, race_name: str):
    return db.query(models.Character).filter(models.Character.race_name == race_name).all()

def delete_character(db: Session, character_id: int):
    db_character = db.query(models.Character).filter(models.Column.id == character_id).first()
    db.delete(db_character)
    db.commit()
    return db_character

################### NOT IN USE YET ##############################
def create_armor(db: Session, armor: schemas.Armor, character_id: int):
    db_armor = models.Armor(**armor.dict(), character_id=character_id)
    db.add(db_armor)
    db.commit()
    db.refresh(db_armor)
    return db_armor

def create_weapon(db: Session, weapon: schemas.WeaponCreate, character_id: int):
    db_weapon = models.Weapon(**weapon.dict(), character_id=character_id)
    db.add(db_weapon)
    db.commit()
    db.refresh(db_weapon)
    return db_weapon

def get_armor(db: Session, armor_id: int):
    return db.query(models.Armor).filter(models.Armor.id == armor_id).first()
def get_weapons(db: Session):
    return db.query(models.Weapon)
def get_weapon_by_id(db: Session, weapon_id: int):
    return db.query(models.Weapon).filter(models.Weapon.id == weapon_id).first()
