import pytest
import sqlalchemy as sa
import json
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..database import get_db
from ..main import app
from ..models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Set up the database once
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


# These two event listeners are only needed for sqlite for proper
# SAVEPOINT / nested transaction support. Other databases like postgres
# don't need them. 
# From: https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#serializable-isolation-savepoints-transactional-ddl
@sa.event.listens_for(engine, "connect")
def do_connect(dbapi_connection, connection_record):
    # disable pysqlite's emitting of the BEGIN statement entirely.
    # also stops it from emitting COMMIT before any DDL.
    dbapi_connection.isolation_level = None

@sa.event.listens_for(engine, "begin")
def do_begin(conn):
    # emit our own BEGIN
    conn.exec_driver_sql("BEGIN")
    
# This fixture is the main difference to before. It creates a nested
# transaction, recreates it when the application code calls session.commit
# and rolls it back at the end.
# Based on: https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
@pytest.fixture()
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    # Begin a nested transaction (using SAVEPOINT).
    nested = connection.begin_nested()

    # If the application code calls session.commit, it will end the nested
    # transaction. Need to start a new one when that happens.
    @sa.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    # Rollback the overall transaction, restoring the state before the test ran.
    session.close()
    transaction.rollback()
    connection.close()


# A fixture for the fastapi test client which depends on the
# previous session fixture. Instead of creating a new session in the
# dependency override as before, it uses the one provided by the
# session fixture.
@pytest.fixture()
def client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]


def test_create_guardian(client):
    response = client.post(
        "/guardians/",
        json={"bungie_id": "112233", "name": "testguardian#1111", "platform": 3}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['bungie_id'] == '112233'
    assert 'id' in data
    guardian_id = data['id']
    
    response = client.get(f"/guardians/{guardian_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['bungie_id'] == '112233'
    assert data['name'] == 'testguardian#1111'
    assert data['platform'] == 3
    assert data['id'] == guardian_id
    
def test_read_guardian(client):
    response = client.post(
        "/guardians",
        json={"bungie_id": "112233", "name": "testguardian#1111", "platform": 3}
    )
    data = response.json()
    guardian_id = data['id']
    
    response = client.get(f"/guardians/{guardian_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['bungie_id'] == '112233'
    assert data['name'] == 'testguardian#1111'
    assert data['platform'] == 3
    assert data['id'] == guardian_id
    
def test_read_guardians(client):
    response = client.post(
        "/guardians",
        json={"bungie_id": "112233", "name": "testguardian#1111", "platform": 3}
    )
    assert response.status_code == 200, response.text
    response = client.post(
        "/guardians",
        json={"bungie_id": "332211", "name": "testguardian#2222", "platform": 2}
    )
    assert response.status_code == 200, response.text
    response = client.get(
        "/guardians/",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    # Guardian 1
    assert data[0]['bungie_id'] == "112233"
    assert 'id' in data[0]
    assert data[0]['name'] == "testguardian#1111"
    assert data[0]['platform'] == 3
    # Guardian 2
    assert data[1]['bungie_id'] == "332211"
    assert 'id' in data[1]
    assert data[1]['name'] == "testguardian#2222"
    assert data[1]['platform'] == 2
    
def test_read_id_by_bungie_id(client):
    response = client.post(
        "/guardians",
        json={"bungie_id": "112233", "name": "testguardian#1111", "platform": 3}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    bungie_id = data['bungie_id']
    guardian_id = data['id']
    
    response = client.get(
        f'/guardians/{bungie_id}/id/'
    )
    assert response.status_code == 200, response.text
    assert response.text == str(guardian_id)
    
def test_read_guardian_by_bungie_id(client):
    response = client.post(
        "/guardians",
        json={"bungie_id": "112233", "name": "testguardian#1111", "platform": 3}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    bungie_id = data['bungie_id']
    
    response = client.get(
        f"/guardians/bungie_id/{bungie_id}"
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['bungie_id'] == '112233'
    assert data['name'] == 'testguardian#1111'
    assert data['platform'] == 3

def test_read_guardian_by_name(client):
    response = client.post(
        "/guardians",
        json={"bungie_id": "112233", "name": "testguardian#1111", "platform": 3}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    name = data['name']
    
    response = client.get(
        f"/guardians/name/testguardian%231111"
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['bungie_id'] == '112233'
    assert data['name'] == 'testguardian#1111'
    assert data['platform'] == 3
    
def test_read_clanmates_common_data(client):
    response = client.post(
        "/guardians",
        json={"bungie_id": "123", "name": "testguardian#1111", "platform": 3}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert 'id' in data
    guardian1_id = data['id']
    response = client.post(
        "/guardians",
        json={"bungie_id": "321", "name": "testguardian#2222", "platform": 2}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert 'id' in data
    guardian2_id = data['id']
    response = client.get(
        "/guardians/clanmates/"
    )
    assert response.status_code == 200, response.text
    data = response.json()
    
    # Guardian 1
    assert data[0]['name'] == "testguardian#1111"
    assert data[0]['guardian_id'] == guardian1_id
    assert data[0]['characters_info'] == []
    
    # Guardian 2
    assert data[1]['name'] == "testguardian#2222"
    assert data[1]['guardian_id'] == guardian2_id
    assert data[1]['characters_info'] == []

def test_update_guardian(client):
    response = client.post(
        "/guardians",
        json={"bungie_id": "123", "name": "testguardian#1111", "platform": 3}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert 'id' in data
    guardian_id = data['id']
    
    assert data['name'] == "testguardian#1111"
    assert data['id'] == guardian_id
    assert data['bungie_id'] == "123"
    assert data['platform'] == 3
    
    response = client.put(
        f"/guardians/{guardian_id}",
        json={"name": "testguardian#2222", "platform": 2}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert 'id' in data
    guardian_id = data['id']
    
    assert data['name'] == "testguardian#2222"
    assert data['id'] == guardian_id
    assert data['bungie_id'] == "123"
    assert data['platform'] == 2
    

def test_delete_guardian(client):
    response = client.post(
        "/guardians",
        json={"bungie_id": "123", "name": "testguardian#1111", "platform": 3}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert 'id' in data
    guardian_id = data['id']
    
    assert data['name'] == "testguardian#1111"
    assert data['id'] == guardian_id
    assert data['bungie_id'] == "123"
    assert data['platform'] == 3
    
    response = client.delete(
        f"/guardians/{guardian_id}"
    )
    assert response.status_code == 200, response.text
    
    response = client.get(
        f"/guardians/{guardian_id}"
    )
    assert response.status_code == 404, response.text
    
def test_create_character(client):
    response = client.post(
        "/guardians/",
        json={"bungie_id": "112233", "name": "testguardian#1111", "platform": 3}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert 'id' in data
    assert data['bungie_id'] == "112233"
    assert data['name'] == "testguardian#1111"
    assert data['platform'] == 3
    guardian_id = data['id']
    
    
    with open("zen_api/tests/test_character_payload.json", "r") as f:
        data = json.load(f)
    test_character = data
    response = client.post(
        f"/guardians/{guardian_id}/",
        json=test_character
    )
    assert response.status_code == 200, response.text

def test_read_character(client):
    response = client.post(
        "/guardians/",
        json={"bungie_id": "112233", "name": "testguardian#1111", "platform": 3}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert 'id' in data
    assert data['bungie_id'] == "112233"
    assert data['name'] == "testguardian#1111"
    assert data['platform'] == 3
    guardian_id = data['id']
    
    
    with open("zen_api/tests/test_character_payload.json", "r") as f:
        data = json.load(f)
    test_character = data
    response = client.post(
        f"/guardians/{guardian_id}/",
        json=test_character
    )
    assert response.status_code == 200, response.text
    data = response.json()
    
    # Character common data
    assert data['char_class'] == "Warlock"
    assert "Recovery" in data['stats'].keys()
    assert data['emblem_name'] == 'Ferrous Ferocity'
    assert data['light'] == 1832
    assert data['race_name'] == "Exo"
    assert data['title'] != None or {}
    assert data['subclass'] != None or {}
    
    # Items
    assert data['items']['Kinetic Weapons']['common_data']['item_name'] == "Bite of the Fox"
    assert data['items']['Kinetic Weapons']['common_data']['item_icon'] != ''
    assert data['items']['Kinetic Weapons']['perks'] != None or {}
    assert data['items']['Kinetic Weapons']['stats'] != None or {}
    assert data['items']['Energy Weapons']['common_data']['item_name'] == "Mechabre"
    assert data['items']['Energy Weapons']['common_data']['item_icon'] != ''
    assert data['items']['Energy Weapons']['perks'] != None or {}
    assert data['items']['Energy Weapons']['stats'] != None or {}
    assert data['items']['Power Weapons']['common_data']['item_name'] == "Bad Omens"
    assert data['items']['Power Weapons']['common_data']['item_icon'] != ''
    assert data['items']['Power Weapons']['perks'] != None or {}
    assert data['items']['Power Weapons']['stats'] != None or {}
    
def test_read_character_by_guardian_id(client):
    response = client.post(
        "/guardians/",
        json={"bungie_id": "112233", "name": "testguardian#1111", "platform": 3}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert 'id' in data
    assert data['bungie_id'] == "112233"
    assert data['name'] == "testguardian#1111"
    assert data['platform'] == 3
    guardian_id = data['id']
    
    
    with open("zen_api/tests/test_character_payload.json", "r") as f:
        data = json.load(f)
    test_character = data
    response = client.post(
        f"/guardians/{guardian_id}/",
        json=test_character
    )
    assert response.status_code == 200, response.text
    data = response.json()
    
    response = client.get(
        f"/characters/guardian/{guardian_id}"
    )
    assert response.status_code == 200, response.text
    
def test_update_character(client):
    response = client.post(
        "/guardians/",
        json={"bungie_id": "112233", "name": "testguardian#1111", "platform": 3}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert 'id' in data
    assert data['bungie_id'] == "112233"
    assert data['name'] == "testguardian#1111"
    assert data['platform'] == 3
    guardian_id = data['id']
    
    
    with open("zen_api/tests/test_character_payload.json", "r") as f:
        data = json.load(f)
    test_character = data
    response = client.post(
        f"/guardians/{guardian_id}/",
        json=test_character
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert 'id' in data
    character_id = data['id']
    
    # Character common data
    assert data['char_class'] == "Warlock"
    assert "Recovery" in data['stats'].keys()
    assert data['emblem_name'] == 'Ferrous Ferocity'
    assert data['light'] == 1832
    assert data['race_name'] == "Exo"
    assert data['title'] != None or {}
    assert data['subclass'] != None or {}
    
    payload = {
        "char_class": "Titan",
        "last_login": "2023-05-08T15:12:40Z",
        "stats": {
            "Power": 1832,
            "Mobility": 23,
            "Resilience": 100,
            "Recovery": 100,
            "Discipline": 100,
            "Intellect": 60,
            "Strength": 22
        },
        "items": {},
        "emblemBackgroundPath": "string",
        "emblem_name": "Flawless Emblem",
        "emblem_path": "string",
        "light": 1840,
        "minutesPlayedTotal": "string",
        "race_name": "Human",
        "title": {
            "name": "Crucible",
            "description": "Complete all Crucible Triumphs.\n\nComplete this Title to unlock Seasonal gilding.",
            "icon": "/common/destiny2_content/icons/17e32d11b0f3ce7f15b2c9aac69bedd9.png"
        },
        "subclass": {
            "name": "Dawnblade",
            "icon": "/common/destiny2_content/icons/fedcb91b7ab0584c12f0e9fec730702b.png"
        }
    }
    
    response = client.put(
        f"/characters/{character_id}/",
        json=payload
    )
    assert response.status_code == 200, response.text
    data = response.json()
    
    # Character common data
    assert data['char_class'] == "Titan"
    assert "Recovery" in data['stats'].keys()
    assert data['emblem_name'] == 'Flawless Emblem'
    assert data['light'] == 1840
    assert data['race_name'] == "Human"
    assert data['title'] != None or {}
    assert data['subclass'] != None or {}
    
def test_delete_character(client):
    response = client.post(
        "/guardians/",
        json={"bungie_id": "112233", "name": "testguardian#1111", "platform": 3}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert 'id' in data
    assert data['bungie_id'] == "112233"
    assert data['name'] == "testguardian#1111"
    assert data['platform'] == 3
    guardian_id = data['id']
    
    
    with open("zen_api/tests/test_character_payload.json", "r") as f:
        data = json.load(f)
    test_character = data
    response = client.post(
        f"/guardians/{guardian_id}/",
        json=test_character
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert 'id' in data
    character_id = data['id']
    
    # Character common data
    assert data['char_class'] == "Warlock"
    assert "Recovery" in data['stats'].keys()
    assert data['emblem_name'] == 'Ferrous Ferocity'
    assert data['light'] == 1832
    assert data['race_name'] == "Exo"
    assert data['title'] != None or {}
    assert data['subclass'] != None or {}
    
    response = client.delete(
        f"/characters/{character_id}"
    )
    assert response.status_code == 200, response.text
    
    response = client.get(
        f"/characters/{character_id}"
    )
    assert response.status_code == 404, response.text