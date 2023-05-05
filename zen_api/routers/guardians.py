from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db
from fastapi.security.api_key import APIKey
from ..auth import get_api_key

router = APIRouter()


@router.post("/guardians/", response_model=schemas.Guardian, tags=['Guardians'])
def create_guardian(guardian: schemas.GuardianCreate, db: Session = Depends(get_db)):
    db_guardian = crud.get_guardian_by_bungie_id(db, bungie_id=guardian.bungie_id)
    if db_guardian:
        raise HTTPException(status_code=400, detail="Bungie ID already in database")
    return crud.create_guardian(db=db, guardian=guardian)

@router.get('/guardians/{guardian_id}', response_model=schemas.Guardian, tags=['Guardians'])
def read_guardian(guardian_id: int, db: Session = Depends(get_db)):
    db_guardian = crud.get_guardian(db, guardian_id=guardian_id)
    if db_guardian is None:
        raise HTTPException(status_code=404, detail="Guardian not found")
    return db_guardian

#api_key: APIKey = Depends(get_api_key)
@router.get("/guardians/", response_model=list[schemas.Guardian], tags=['Guardians'])
def read_guardians(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_guardians = crud.get_guardians(db, skip=skip, limit=limit)
    return db_guardians

@router.get('/guardians/{bungie_id}/id/', tags=['Guardians'])
def read_guardian_id_by_bungie_id(bungie_id: str, db: Session = Depends(get_db)):
    db_id = crud.get_guardian_id_by_bungie_id(db=db, bungie_id=bungie_id)
    if db_id is None:
        raise HTTPException(status_code=404, detail='Guardian not found')
    return db_id

@router.get('/guardians/bungie_id/{bungie_id}', response_model=schemas.Guardian, tags=['Guardians'])
def read_guardian_by_bungie_id(bungie_id: int, db: Session = Depends(get_db)):
    db_guardian = crud.get_guardian_by_bungie_id(db, bungie_id=bungie_id)
    if db_guardian is None:
        raise HTTPException(status_code=404, detail="Guardian not found")   
    return db_guardian

@router.get('/guardians/name/{name}', response_model=schemas.Guardian, tags=['Guardians'])
def read_guardian_by_name(name: str, db: Session = Depends(get_db)):
    db_guardian = crud.get_guardian_by_name(db, name=name)
    print(db_guardian)
    if db_guardian is None:
        raise HTTPException(status_code=404, detail="Guardian not found")
    return db_guardian

@router.get("/guardians/character/{character_id}", response_model=schemas.Guardian, tags=['Guardians'])
def read_guardian_by_character_id(character_id: int, db: Session = Depends(get_db)):
    db_guardian = crud.get_guardian_by_character_id(db, character_id=character_id)
    if db_guardian is None:
        raise HTTPException(status_code=404, detail="Guardian not found")
    return db_guardian

@router.get('/guardians/clanmates/', tags=['Guardians'])
def read_clanmates_common_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_guardians = crud.test_guardian(db, skip=skip, limit=limit)
    return db_guardians

# UPDATE guardian by guardian_id
@router.put("/guardians/{guardian_id}", response_model=schemas.Guardian, tags=['Guardians'])
def update_guardian(guardian_id: int, guardian: schemas.GuardianUpdate, db: Session = Depends(get_db)):
    db_guardian = crud.get_guardian(db, guardian_id=guardian_id)
    if db_guardian is None:
        raise HTTPException(status_code=404, detail="Guardian not found")
    for field, value in guardian.dict(exclude_unset=True).items():
        setattr(db_guardian, field, value)
    db.commit()
    db.refresh(db_guardian)
    return db_guardian 

# DELETE a guardian with related characters by guardian_id
@router.delete("/guardians/{guardian_id}", response_model=schemas.Guardian, tags=['Guardians'])
def delete_guardian(guardian_id: int, db: Session = Depends(get_db)):
    deleted_guardian = crud.delete_guardian(db, guardian_id=guardian_id)
    if deleted_guardian is None:
        raise HTTPException(status_code=404, detail="Guardian not found")
    return deleted_guardian


