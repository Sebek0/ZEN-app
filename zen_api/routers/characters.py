from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.get("/characters/{character_id}", response_model=schemas.Character, tags=['Characters'])
def read_character(character_id: int, db: Session = Depends(get_db)):
    db_character = crud.get_character(db, character_id=character_id)
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found!")
    return db_character

@router.get("/characters/", response_model=list[schemas.Character], tags=['Characters'])
def read_characters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_characters = crud.get_characters(db, skip=skip, limit=limit)
    return db_characters

@router.get("/characters/class/{class_name}", response_model=list[schemas.Character], tags=['Characters'])
def read_characters_by_class(class_name: str, db: Session = Depends(get_db)):
    db_characters = crud.get_characters_by_class(db, class_name=class_name.capitalize())
    if db_characters is None:
        raise HTTPException(status_code=404, detail=f"Characters with {class_name.capitalize()} not found!")
    return db_characters

@router.get("/characters/guardian/{guardian_id}", response_model=list[schemas.Character], tags=['Characters'])
def read_characters_by_guardian_id(guardian_id: int, db: Session = Depends(get_db)):
    db_characters = crud.get_characters_by_guardian_id(db, guardian_id=guardian_id)
    if db_characters is None:
        raise HTTPException(status_code=404, detail=f"Characters for {guardian_id} not found!")
    return db_characters

@router.get("/characters/title/{title}", response_model=list[schemas.Character], tags=['Characters'])
def read_characters_by_title(title: str, db: Session = Depends(get_db)):
    db_characters = crud.get_characters_by_title(db, title=title)
    if db_characters is None:
        raise HTTPException(status_code=404, detail=f'Characters with title: {title} not found!')
    return db_characters
    
@router.get("/characters/race/{race_name}", response_model=list[schemas.Character], tags=['Characters'])
def read_characters_by_race_name(race_name: str, db: Session = Depends(get_db)):
    db_characters = crud.get_characters_by_race_name(db, race_name=race_name)
    if db_characters is None:
        raise HTTPException(status_code=404, detail=f'Characters with race: {race_name} not found!')
    return db_characters

@router.post("/guardians/{guardian_id}/", response_model=schemas.Character, tags=['Characters'])
def create_character_for_guardian(guardian_id: int, character: schemas.CharacterCreate, db: Session = Depends(get_db)):
    return crud.create_character(db=db, character=character, guardian_id=guardian_id)

# UPDATE guardian by guardian_id
@router.put("/characters/{character_id}", response_model=schemas.Character, tags=['Characters'])
def update_character(character_id: int, character: schemas.CharacterUpdate, db: Session = Depends(get_db)):
    db_character = crud.get_character(db, character_id=character_id)
    if db_character is None:
        raise HTTPException(status_code=404, detail="Guardian not found")
    for field, value in character.dict(exclude_unset=True).items():
        setattr(db_character, field, value)
    db.commit()
    db.refresh(db_character)
    return db_character 

# DELETE a character from guardian
@router.delete("/characters/{character_id}", response_model=schemas.Character, tags=['Characters'])
def delete_character(character_id: int, db: Session = Depends(get_db)):
    deleted_character = crud.delete_character(db, character_id=character_id)
    if deleted_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return deleted_character

