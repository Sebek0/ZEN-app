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
    char_id: int
    char_class: str
    stats: dict = {}
    emblem: str
    title: str
    last_login: str 


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
    bungie_id: int 
    name: str
    platform: int = 3


class GuardianCreate(GuardianBase):
    pass
   
        
class Guardian(GuardianBase):
    id: int
    characters: list[Character] = []

    class Config:
        orm_mode = True