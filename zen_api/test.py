import requests
import random
import time

def create_guardian(payload): 
    response = requests.post('http://127.0.0.1:8000/guardians', json=payload)
    print(response)
    
def create_character(guardian_id, payload):
    response = requests.post(f'http://127.0.0.1:8000/guardians/{guardian_id}/character/', json=payload)
    print(f"Char: {response}")

def create_weapon(character_id, payload):
    response = requests.post(f'http: //127.0.0.1: 8000/guardians/{guardian_id}/character/{character_id}/weapons', json=payload)
    
names = ['andrzej', 'filip', 'piotr']
for i in range(1, 250):
    #time.sleep(0.5)
    payload = {'bungie_id': i, 'name': f'{str(random.choice(names))}#{str(random.randrange(1000, 9999))}'}
    create_guardian(payload=payload)
    for x in range(1, 4):
        payload = {"char_id": random.randrange(1, 9999),
                    "char_class": "Warlock",
                    "stats": {'Recovery': 100, 'Dexterity': 200},
                    "emblem": "Testemblem",
                    "title": "Reckoner",
                    "last_login": "22/04/2023"}
        create_character(guardian_id=i, payload=payload)
    

