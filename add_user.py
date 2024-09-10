import re
import os
import json
import requests
from dotenv import load_dotenv
 
load_dotenv()

open_cage_api_key = os.getenv("OPENCAGE_API_KEY")

def validate_email(email):
    # Sprawdza, czy adres e-mail jest poprawny.
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def validate_non_empty(value, field_name):
    #Sprawdza, czy wartość nie jest pusta.
    if not value.strip():
        print(f"Pole {field_name} nie może być puste.")
        return False
    return True

def add_user():  
    # Pobranie danych od użytkownika
    name = input("Choose name: ")
    email_address = input("Add e-mail address: ")
    country = input("Type your country: ")
    city = input("Type your city: ")
    street = input("Type your street (optional): ")

    # Walidacja danych
    if not validate_non_empty(name, "name") or not validate_non_empty(email_address, "e-mail address") or not validate_email(email_address) or not validate_non_empty(country, "country") or not validate_non_empty(city, "city"):
        add_user()
        
    #zdobycie koordynatow na podstawie miasta 
    response = requests.get(f"https://api.opencagedata.com/geocode/v1/json?q={street}%2C+99423+{city}%2C+{country}&key={open_cage_api_key}")
    
 
    data = response.json()
    if len(data["results"]) > 0:
        lat_lng = data['results'][0]['annotations']['DMS']
    else:
        print("an error occurred while adding the user, please check if Town name is correct")
        add_user()
        
    #Tworzenie nowego wpisu
    new_data = {
        "name": name,
        "email_address": email_address,
        "adress": {
            "country": country,
            "city": city,
            "street": street,
            "lat": lat_lng["lat"],
            "lon": lat_lng["lng"]
        }
    }

    # Wczytanie istniejących danych lub inicjalizacja pustej listy
    if os.path.getsize("data.json") > 0:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
    else:
        data = []
    
    # Dodanie nowego wpisu
    data.append(new_data)
    
    with open("data.json", 'w') as data_file:
        json.dump(data, data_file, indent=4)
        print('User is added! :D')  