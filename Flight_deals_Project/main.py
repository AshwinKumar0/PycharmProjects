#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import requests_cache
import requests
import json
from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from flight_data import find_cheapest_flight
from pprint import pprint
from notification_manager import NotificationManager

requests_cache.install_cache("flight_cache", urls_expire_after={
        "*.sheety.co*": requests_cache.DO_NOT_CACHE,
        "*": 3600,
    })

data_manager = DataManager()
sheet_data = data_manager.get_destination_data() or []

notification_manager = NotificationManager()
flight_search = FlightSearch()

ORIGIN_CITY_IATA = "LHR"

todays_date = datetime.now() + timedelta(days=1)
date_after_month = datetime.now() + timedelta(days=30)




     # ==================== Get users email for the sheets ====================
users = data_manager.get_customer_emails() or []
email_list = [u.get("email") for u in users if "email" in u]




     # ==================== Search for direct flight ====================

for destination in sheet_data:
    pprint(f"Getting flights for {destination['city']}...")
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=todays_date,
        to_time=date_after_month,
        is_direct = True
    )

    cheapest_flight = find_cheapest_flight(flights, return_date=date_after_month.strftime("%Y-%m-%d"))
    pprint(f"{destination['city']}: INR {cheapest_flight.price}")
    




     # ==================== Search for indirect flight if N/A ====================

    if cheapest_flight.price == "N/A":
        print(f"No direct flight to {destination['city']}. Looking for indirect flights...")
        stopover_flights = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=todays_date,
            to_time=date_after_month,
            is_direct=False
        )

        cheapest_flight = find_cheapest_flight(stopover_flights, return_date=date_after_month.strftime("%Y-%m-%d"))
        print(f"Cheapest indirect flight price is: INR {cheapest_flight.price}")



   
   
    # ==================== Send mails ====================

    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestprice"]:
        # Customise the message depending on the number of stops
        if cheapest_flight.stops == 0:
            message = f"Low price alert! Only INR {cheapest_flight.price} to fly direct "\
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
                      f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        else:
            message = f"Low price alert! Only INR {cheapest_flight.price} to fly "\
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
                      f"with {cheapest_flight.stops} stop(s) "\
                      f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."
        
        notification_manager.send_emails(email_list, message=message)

        print(f"Check your email. Lower price flight found to {destination['city']}!")









    # ==================== Send sms ====================
    #     notification_manager.send_sms(
    #         message_body=f"Low price alert! Only INR {cheapest_flight.price} to fly "
    #                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
    #                      f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
    #     )