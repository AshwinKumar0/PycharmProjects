import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_api_key = os.getenv("TWILIO_API_KEY")
twilio_api_sid = os.getenv("TWILIO_API_SID")
open_weather_api_key = os.getenv("OPEN_WEATHER_API_KEY")


api_key = open_weather_api_key
my_lat = "24.027917"
my_lng = "85.962001"    

test_lat = "51.4545"
test_lng = "-2.5879"

weather_url = "https://api.openweathermap.org/data/2.5/forecast?"
weather_params ={
    "lat": my_lat,
    "lon": my_lng,
    "cnt": "4",
    "appid": api_key,
    "units": "metric"
}


def get_weather():
    response = requests.get(weather_url, params=weather_params)
    response.raise_for_status()
    print(response.status_code)
    weather_data = response.json()
    print(weather_data["list"][0]["weather"])
    today_weather_codes = [data["weather"][0]["id"] for data in  weather_data["list"]]
    client = Client(account_sid, auth_token)
    if any(code < 600 for code in today_weather_codes):
        message = client.messages.create(
        from_= "+12182199382",    
        body= "It's going to rain today. Remember to bring an ☂️.",
        to= "+916206068272"

    )
    else:
        message = client.messages.create(
            from_= "+12182199382",
            body= "No rain today. Enjoy your day! ☀️",
            to= "+916206068272"
        )
    
    print(message.status)


get_weather()

