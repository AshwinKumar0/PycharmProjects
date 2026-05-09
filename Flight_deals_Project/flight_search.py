import requests
import os
from dotenv import load_dotenv


load_dotenv()



class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.url = "https://serpapi.com/search.json"
        self.api_key = os.getenv("SERP_API")

    def flight_data(self):
        response = requests.get(self.url, params=self.params)
        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            return None

        data = response.json()
        if "error" in data:
            print(f"API error: {data['error']}")
            return None
        return data
    
    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, is_direct = True):
            self.params = {
            "engine": "google_flights",
            "departure_id": origin_city_code,
            "arrival_id": destination_city_code,
            "outbound_date": from_time.strftime("%Y-%m-%d"),
            "return_date" : to_time.strftime("%Y-%m-%d"),
            "currency": "INR",
            "hl" : "en",
            "gl" : "in",
            "adults" : "1",
            "type" : "1",          
            "api_key": self.api_key,
            "deep_search" : "true"  
        }
            if is_direct : 
                 self.params["stops"] = 1

            return self.flight_data()