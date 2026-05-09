import requests
from dotenv import load_dotenv
import os
from pprint import pprint

load_dotenv()

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheety_prices_url = "https://api.sheety.co/4b2defc783120e2f7b411657fbf138af/flightRates/prices"
        self.sheety_users_url = "https://api.sheety.co/4b2defc783120e2f7b411657fbf138af/flightRates/users"
        self.username = os.getenv("SHEETY_USERNAME")
        self.user_pass = os.getenv("SHEETY_USER_PASSWORD")

        self.sheety_apikey = os.getenv("SHEETY_API")
        self.headers = {
            "Authorization": self.sheety_apikey
        }
        self.destination_data = {}
        self.users_data = {}

    def get_customer_emails(self):
        response = requests.get(self.sheety_users_url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            self.users_data = data["users"]
            return self.users_data
        else:
            print(f"Error : {response.status_code}")


    def get_destination_data(self):
        response = requests.get(self.sheety_prices_url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            self.destination_data = data["prices"]
            return self.destination_data
           
        else:
            print(f"Error : {response.status_code}")


    def update_lowest_price(self, row_id, new_price):
        new_data = {
            "price" : {
                "lowestprice" : new_price
            }
        }
        response = requests.put(
            url= f"{self.sheety_prices_url}/{row_id}",
            json= new_data,
            headers= self.headers
        )
        print(response.status_code)
        print("data updated on sheet")