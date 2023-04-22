from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Guardians",
        "description": "Operations with guardians.",
    },
    {
        "name": "Characters",
        "description": "Manage characters for guardians.",
    },
]

description = """
ZENApp API helps you maintain ZEN clan data.

## Guardians

You will be able to:

* **Create Guardians**.
* **Read Guardains**.
* **Manage Guardians** (_not implemented_).
* **Delete Guardians**.
* **Update Guardians** (_not implemented_).

## Characters

You will be able to:

* **Create Characters**.
* **Read Characters** (_not implemented_).
* **Manage Characters** (_not implemented_).
* **Delete Characters** (_not implemented_).
* **Update Characters** (_not implemented_).
"""
app = FastAPI(openapi_tags=tags_metadata)
app = FastAPI(
    title="ZENApp API",
    description=description,
    version="0.0.1",
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items

# @app.post("/users/{user_id}/characters/", response_model=schemas.Character)
# def create_character_for_user(
#     user_id: int, character: schemas.CharacterCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_character(db=db, character=character, user_id=user_id)

###########################################################################
@app.post("/guardians/", response_model=schemas.Guardian, tags=['Guardians'])
def create_guardian(guardian: schemas.GuardianCreate, db: Session = Depends(get_db)):
    db_guardian = crud.get_guardian_by_bungie_id(db, bungie_id=guardian.bungie_id)
    if db_guardian:
        raise HTTPException(status_code=400, detail="Bungie ID already in database")
    return crud.create_guardian(db=db, guardian=guardian)

@app.get('/guardians/{guardian_id}', response_model=schemas.Guardian, tags=['Guardians'])
def read_guardian(guardian_id: int, db: Session = Depends(get_db)):
    db_guardian = crud.get_guardian(db, guardian_id=guardian_id)
    if db_guardian is None:
        raise HTTPException(status_code=404, detail="Guardian not found")
    return db_guardian

@app.get('/guardians/bungieid/{bungie_id}', response_model=schemas.Guardian, tags=['Guardians'])
def read_guardian_by_bungie_id(bungie_id: int, db: Session = Depends(get_db)):
    db_guardian = crud.get_guardian_by_bungie_id(db, bungie_id=bungie_id)
    if db_guardian is None:
        raise HTTPException(status_code=404, detail="Guardian not found")   
    return db_guardian

@app.get('/guardians/name/{name}', response_model=schemas.Guardian, tags=['Guardians'])
def read_guardian_by_name(name: str, db: Session = Depends(get_db)):
    db_guardian = crud.get_guardian_by_name(db, name=name)
    print(db_guardian)
    if db_guardian is None:
        raise HTTPException(status_code=404, detail="Guardian not found")
    return db_guardian

@app.get("/guardians/", response_model=list[schemas.Guardian], tags=['Guardians'])
def read_guardians(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    guardians = crud.get_guardians(db, skip=skip, limit=limit)
    return guardians

@app.get("/guardians/character/{character_id}", response_model=schemas.Guardian, tags=['Guardians'])
def read_guardian_by_character_id(character_id: int, db: Session = Depends(get_db)):
    db_guardian = crud.get_guardian_by_character_id(db, character_id=character_id)
    if db_guardian is None:
        raise HTTPException(status_code=404, detail="Guardian not found")
    return db_guardian

@app.delete("/guardians/{guardian_id}", tags=['Guardians'])
def delete_user(guardian_id: int, db: Session = Depends(get_db)):
    deleted_guardian = crud.delete_guardian(db, guardian_id=guardian_id)
    if deleted_guardian is None:
        raise HTTPException(status_code=404, detail="Guardian not found")
    return deleted_guardian



# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users

@app.post("/guardians/{guardian_id}/", response_model=schemas.Character, tags=['Characters'])
def create_character_for_guardian(
    guardian_id: int, character: schemas.CharacterCreate, db: Session = Depends(get_db)
):
    return crud.create_character(db=db, character=character, guardian_id=guardian_id)

@app.get("/characters/{character_id}", response_model=schemas.Character, tags=['Characters'])
def read_character(character_id: int, db: Session = Depends(get_db)):
    db_character = crud.get_character(db, character_id=character_id)
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return db_character


@app.get('/guardians/{guardian_id}', response_model=schemas.Guardian, tags=['Guardians'])
def read_guardian(guardian_id: int, db: Session = Depends(get_db)):
    db_guardian = crud.get_guardian(db, guardian_id=guardian_id)
    if db_guardian is None:
        raise HTTPException(status_code=404, detail="Guardian not found")
    return db_guardian

###################################################################
@app.post("/characters/{character_id}/armors/", response_model=schemas.Armor, tags=['Armors'])
def create_armor_for_character(
    character_id: int, armor: schemas.ArmorCreate, db: Session = Depends(get_db)   
):
    return crud.create_armor(db=db, armor=armor, character_id=character_id)

@app.get("/armors/{armor_id}", response_model=schemas.Armor, tags=['Armors'])
def read_armor_by_id(armor_id: int, db: Session = Depends(get_db)):
    db_armor = crud.get_armor(db, armor_id=armor_id)
    if db_armor is None:
        raise HTTPException(status_code=404, detail="Armor not found")
    return db_armor

"""functionality	    method	    path
create a todo item	    POST	    /todo
read a todo list item	GET	        todo/{id}
update a todo item	    PUT	        /todo/{id}
delete a todo item	    DELETE	    /todo/{id}
read all todo items	    GET	        /todo"""