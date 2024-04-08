import requests
import json

url = "http://localhost:8000/characters"
headers = {"Content-Type": "application/json"}


new_character_data = {
    "name": "Gandalf",
    "level": 10,
    "role": "Wizard",
    "charisma": 15,
    "strength": 10,
    "dexterity": 10
}
response = requests.post(url=url, json=new_character_data, headers=headers)
print("POST", response.json())

response = requests.get(url=url)
print("GET /characters Response:", response.json())


params = {"role": "Archer", "level": 5, "charisma": 10}
response = requests.get(url=url, params=params)
print("GET /characters Response:", response.json())


character_id_to_update = 2
updated_character_data = {
    "charisma": 20,
    "strength": 15,
    "dexterity": 15
}
response = requests.put(f"{url}/{character_id_to_update}", json=updated_character_data, headers=headers)
print("PUT /characters/2 Response:", response.json())


character_id_to_delete = 1
response = requests.delete(f"{url}/{character_id_to_delete}")
print("DELETE /characters/1 Response:", response.json())


new_character_data = {
    "name": "Legolas",
    "level": 5,
    "role": "Archer",
    "charisma": 15,
    "strength": 10,
    "dexterity": 10
}
response = requests.post(url=url, json=new_character_data, headers=headers)
print("POST /characters Response:", response.json())

response = requests.get(url=url)
print("GET /characters Response:", response.json())
