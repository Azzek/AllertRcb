import requests
from weather_codes import weather_codes
import json
from smtplib import SMTP
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

open_weather_api_key = os.getenv('OPEN_WEATHER_API_KEY')

def run_rcb():
    
    with open("data.json", 'r') as users_data:
        users = json.load(users_data)

    for user in users:
        
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={user["adress"]["lat"].split(' ')[2][:-2]}&lon={user["adress"]["lon"].split(' ')[2][:-2]}&appid={open_weather_api_key}")
        weather_data = response.json()
        
        email = "testspython69@gmail.com"
        password = "yjyzgkpbneabfhxc"
        recipient_email = user["email_address"]
        message = weather_codes[weather_data["weather"][0]["main"]][weather_data["weather"][0]["id"]]
        msg = MIMEText(message)
        msg['Subject'] = "Weather allert"
        msg['From'] = email
        msg['To'] = recipient_email
        
        with SMTP('smtp.gmail.com', 587) as smtp_server:
            
            smtp_server.starttls()
            smtp_server.login(email, password)
            smtp_server.sendmail(email, recipient_email, msg.as_string())
        
    print("Emails was sended")