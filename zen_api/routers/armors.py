from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.post("/characters/{character_id}/armors/", response_model=schemas.Armor, tags=['Armors'])
def create_armor_for_character(
    character_id: int, armor: schemas.ArmorCreate, db: Session = Depends(get_db)   
):
    return crud.create_armor(db=db, armor=armor, character_id=character_id)

@router.get("/armors/{armor_id}", response_model=schemas.Armor, tags=['Armors'])
def read_armor_by_id(armor_id: int, db: Session = Depends(get_db)):
    db_armor = crud.get_armor(db, armor_id=armor_id)
    if db_armor is None:
        raise HTTPException(status_code=404, detail="Armor not found")
    return db_armor