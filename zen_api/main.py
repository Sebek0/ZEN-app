from fastapi import FastAPI

from . import models
from .database import engine
from .routers import weapons, armors, guardians, characters

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

## TEMPLATE
functionality	    method	    path
create a todo item	    POST	    /todo
read a todo list item	GET	        todo/{id}
update a todo item	    PUT	        /todo/{id}
delete a todo item	    DELETE	    /todo/{id}
read all todo items	    GET	        /todo
"""

app = FastAPI(openapi_tags=tags_metadata)
app = FastAPI(
    title="ZENApp API",
    description=description,
    version="0.0.1",
)

# Including routers in main app file
app.include_router(guardians.router)
app.include_router(characters.router)
app.include_router(weapons.router)
app.include_router(armors.router)