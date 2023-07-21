from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from . import models
from .database import engine
from .routers import guardians, characters, token
from zen_api.async_worker.async_main import run_update
from .manifest import run_manifest

from fastapi_utils.tasks import repeat_every

tables = [models.Character, models.Guardian]
for table in tables:
    table.__table__.create(bind=engine, checkfirst=True)

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

* **Create Guardians**
* **Read Guardains**
* **Manage Guardians** 
* **Delete Guardians**
* **Update Guardians**

## Characters

You will be able to:

* **Create Characters**
* **Read Characters**
* **Manage Characters**
* **Delete Characters**
* **Update Characters**
"""

app = FastAPI(openapi_tags=tags_metadata)
app = FastAPI(
    title="ZENApp API",
    description=description,
    version="0.0.1",
)

app.mount("/api/v1", app)
# CORS middleware
# TODO: Change for prod
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Including routers in main app file
app.include_router(token.router)
app.include_router(guardians.router)
app.include_router(characters.router)

@app.on_event("startup")
@repeat_every(seconds=60*5)
def update_guardians():
    run_update()
    
@repeat_every(seconds=60*60*24*7)
def update_manifest():
    run_manifest()