from pydantic import BaseModel
from typing import Literal


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