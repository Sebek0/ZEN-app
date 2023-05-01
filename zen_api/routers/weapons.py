from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.post("/characters/{character_id}/weapons", response_model=schemas.Weapon, tags=['Weapons'])
def create_weapon_for_guardian_character(character_id: int, weapon: schemas.WeaponCreate, db: Session = Depends(get_db) ):
    return crud.create_weapon(db=db, weapon=weapon, character_id=character_id)

@router.get("/weapons", response_model=schemas.Weapon, tags=['Weapons'])
def get_all_weapons(db: Session = Depends(get_db)):
    return crud.get_weapons(db=db)
@router.get("/weapons/{weapon_id}", response_model=schemas.Weapon, tags=['Weapons'])
def get_weapon(weapon_id: int, db: Session = Depends(get_db)):
    return crud.get_weapon_by_id(db=db, weapon_id=weapon_id)
