# Flight Deals Project

A Python script that searches for cheaper round-trip flights and emails subscribed users when a fare drops below the target price stored in a Google Sheet.

## What It Does

- Reads destination cities, IATA codes, and target prices from a Sheety-powered Google Sheet.
- Searches Google Flights data through SerpApi for trips from `ORIGIN_AIRPORT` over the next 30 days.
- Checks direct flights first, then searches indirect flights when no direct flight is found.
- Finds the cheapest available fare from the returned flight data.
- Sends email alerts through Gmail when a lower price is found.
- Includes Twilio SMS support, currently commented out in `main.py`.

## Tech Stack

- Python
- SerpApi Google Flights API
- Sheety API
- Gmail SMTP through `yagmail`
- Twilio
- `requests-cache` for local API response caching

## Setup

1. Create and activate a virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies.

```bash
pip install requests requests-cache python-dotenv twilio yagmail
```

3. Create a `.env` file in the project root.

```env
SERP_API=your_serpapi_key
SHEETY_API=your_sheety_authorization_header
SHEETY_USERNAME=your_sheety_username
SHEETY_USER_PASSWORD=your_sheety_password
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
GMAIL_APP_PASSWORD=your_gmail_app_password
```

Keep `.env` private and do not commit it to GitHub.

## Configuration

- Update the Sheety API URLs in `data_manager.py` if you use a different Google Sheet.
- Update `ORIGIN_CITY_IATA` in `main.py` to change the departure airport.
- Update the Gmail sender and Twilio phone numbers in `notification_manager.py` before using alerts in production.

## Run

```bash
python main.py
```

The app creates a local `flight_cache.sqlite` cache file and may use stored flight response data while developing.

## Project Files

- `main.py` - coordinates destination lookup, flight searches, and notifications.
- `data_manager.py` - reads destination and user data from Sheety.
- `flight_search.py` - calls SerpApi's Google Flights endpoint.
- `flight_data.py` - structures and selects the cheapest flight result.
- `notification_manager.py` - sends email alerts and supports Twilio SMS.
- `flight_details.json` - sample SerpApi flight response data.
