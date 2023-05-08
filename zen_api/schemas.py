from pydantic import BaseModel
from typing import Literal


class WeaponBase(BaseModel):
    weapon_instance_id: int
    name: str
    slot: Literal['kinetic', 'energy', 'power']
    state: int
    stats: dict = {}
    damage_type: Literal['kinetic', 'arc', 'solar', 'void', 'stasis', 'strand']
    perks: dict = {}
    damage_type: str


class WeaponCreate(WeaponBase):
    pass


class Weapon(WeaponBase):
    id: int
    character_id: int

    class Config:
        orm_mode = True


class ArmorBase(BaseModel):
    armor_instance_id: str
    name: str
    inventory_slot: str
    state: int
    stats: dict = {}


class ArmorCreate(ArmorBase):
    pass
   
        
class Armor(ArmorBase):
    id: int
    character_id: int

    class Config:
        orm_mode = True


class CharacterBase(BaseModel):
    char_class: str
    last_login: str
    stats: dict = {}
    items: dict = {}
    emblemBackgroundPath: str
    emblem_name: str
    emblem_path: str
    light: int
    minutesPlayedTotal: str
    race_name: str
    title: dict = {}
    subclass: dict = {}


class CharacterUpdate(CharacterBase):
    pass


class CharacterCreate(CharacterBase):
    pass


class Character(CharacterBase):
    id: int
    guardian_id: int
    weapons: list[Weapon] = []
    armors: list[Armor] = []

    class Config:
        orm_mode = True


class GuardianBase(BaseModel):
    bungie_id: str 
    name: str
    platform: int = 3


class GuardianUpdate(BaseModel):
    name: str
    platform: int


class GuardianCreate(GuardianBase):
    pass
   
        
class Guardian(GuardianBase):
    id: int
    characters: list[Character] = []

    class Config:
        orm_mode = True