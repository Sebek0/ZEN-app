from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.post("/guardians/{guardian_id}/", response_model=schemas.Character, tags=['Characters'])
def create_character_for_guardian(
    guardian_id: int, character: schemas.CharacterCreate, db: Session = Depends(get_db)
):
    return crud.create_character(db=db, character=character, guardian_id=guardian_id)

@router.get("/characters/{character_id}", response_model=schemas.Character, tags=['Characters'])
def read_character(character_id: int, db: Session = Depends(get_db)):
    db_character = crud.get_character(db, character_id=character_id)
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return db_character