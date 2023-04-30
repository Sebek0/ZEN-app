from sqlalchemy.orm import Session

from . import models, schemas



# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()


# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item


# def create_user_character(db: Session, character: schemas.CharacterCreate, user_id: int):
#     db_character = models.Character(**character.dict(), owner_id=user_id)
#     db.add(db_character)
#     db.commit()
#     db.refresh(db_character)
#     return db_character
##################################################################
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

def get_guardian_id_by_bungie_id(db: Session, bungie_id: str):
    return db.query(models.Guardian).filter(models.Guardian.bungie_id == bungie_id).first().id

def get_guardian(db: Session, guardian_id: int):
    return db.query(models.Guardian).filter(models.Guardian.id == guardian_id).first()

def get_guardian_by_bungie_id(db: Session, bungie_id: str):
    return db.query(models.Guardian).filter(models.Guardian.bungie_id == bungie_id).first()

def get_guardians(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Guardian).offset(skip).limit(limit).all()

def get_guardian_by_name(db: Session, name: str):
    return db.query(models.Guardian).filter(models.Guardian.name == name).first()

def get_guardian_by_character_id(db: Session, character_id: int):
    return db.query(models.Guardian).filter(models.Character.char_id == character_id).first()

# def delete_guardian(db: Session, guardian: schemas.Guardian):
#     db_guardian = db.query(models.Guardian).get(guardian_id)
#     db.delete(db_guardian)
#     db.commit()
#     db.refresh(db_guardian)
#     return db_guardian

def delete_guardian(db: Session, guardian_id: int):
    db_guardian = db.query(models.Guardian).filter(models.Guardian.id == guardian_id).first()
    db.delete(db_guardian)
    db.commit()
    return db_guardian

# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()


def create_character(db: Session, character: schemas.CharacterCreate, guardian_id: int):
    db_character = models.Character(**character.dict(), guardian_id=guardian_id)
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character

def get_character(db: Session, character_id: int):
    return db.query(models.Character).filter(models.Character.id == character_id).first()

###########################################
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

# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()