from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy import PickleType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList, MutableDict

from .database import Base

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
    title = Column(String)

    weapons = relationship("Weapon", back_populates='character')
    armors = relationship("Armor", back_populates='character')
    guardian = relationship("Guardian", back_populates="characters")


class Weapon(Base):
    __tablename__ = 'weapons'
    
    id = Column(Integer, primary_key=True, index=True)
    weapon_instance_id = Column(Integer, unique=True)
    character_id = Column(Integer, ForeignKey('characters.id'))
    name = Column(String)
    slot = Column(String)
    state = Column(String)
    stats = Column(MutableDict.as_mutable(PickleType), default={})
    damage_type = Column(String)
    perks = Column(MutableDict.as_mutable(PickleType), default={})
    
    character = relationship("Character", back_populates='weapons')


class Armor(Base):
    __tablename__ = 'armors'

    id = Column(Integer, primary_key=True, index=True)
    armor_instance_id = Column(String, unique=True, index=True)
    character_id = Column(Integer, ForeignKey('characters.id'))
    name = Column(String)
    inventory_slot = Column(String)
    state = Column(Integer)
    stats = Column(MutableDict.as_mutable(PickleType), default={})

    character = relationship("Character", back_populates='armors')
    

    


    

