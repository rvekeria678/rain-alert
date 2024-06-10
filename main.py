import requests
import geocoder
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

API_KEY = os.environ['OWM_API_KEY']
API_URL = f'http://api.openweathermap.org/data/2.5/forecast'

location = geocoder.ip('me')

latitude = location.latlng[0]
longitude = location.latlng[1]

paramaters = {
    "lat": latitude,
    "lon": longitude,
    "cnt": 4,
    "appid": API_KEY
    }

def rain_imminent():
    response = requests.get(API_URL, params=paramaters, timeout=120)
    response.raise_for_status()
    weather_data = response.json()
    
    for data in weather_data['list']:
        weather_code = data['weather'][0]['id']
        if weather_code < 700:
            return True
    return False

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

msg = "Err"

if rain_imminent(): msg = "Bring an umbrella!"
else: msg = "Enjoy the weather."

message = client.messages \
                .create(
                    body=f'{msg} Do not Reply.',
                    from_='+18447397772',
                    to='+19787293654'
                )
print(message.sid)