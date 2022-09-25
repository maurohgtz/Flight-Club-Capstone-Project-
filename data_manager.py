import os
import requests
from flight_search import FlightSearch

FLIGHT_CLUB_SHEETS_PROJECT_TOKEN = os.environ["FCP_TOKEN"]
FLIGHT_CLUB_PRICES_SHEETS_API = os.environ["FCP_API"]
FLIGHT_CLUB_USERS_SHEETS_API = os.environ["FB_USERS_SHEET_API"]
SHEETY_TOKEN_HEADER = {
            "Authorization": FLIGHT_CLUB_SHEETS_PROJECT_TOKEN,
            "Content-Type": "application/json"
        }


class DataManager:
    def __init__(self, flight_search: FlightSearch):
        self.flight = flight_search
        self.cities_in_google_sheets = requests.get(url=FLIGHT_CLUB_PRICES_SHEETS_API, headers=SHEETY_TOKEN_HEADER)
        self.cities_data = self.cities_in_google_sheets.json()
        users_in_sheets = requests.get(url=FLIGHT_CLUB_USERS_SHEETS_API, headers=SHEETY_TOKEN_HEADER)
        users = users_in_sheets.json()
        self.list_of_users_emails = [user["email"] for user in users["users"]]

    def add_iata_code(self):
        for city in self.cities_data["prices"]:
            city_from_sheets = city["city"]
            id_from_sheets = city["id"]
            add_parameters = {
                "price": {
                    "iataCode": self.flight.get_iata_code(city_from_sheets)
                }
            }
            response = requests.put(
                url=f"{FLIGHT_CLUB_PRICES_SHEETS_API}/{id_from_sheets}",
                headers=SHEETY_TOKEN_HEADER,
                json=add_parameters
            )
        self.cities_in_google_sheets = requests.get(url=FLIGHT_CLUB_PRICES_SHEETS_API, headers=SHEETY_TOKEN_HEADER)
        self.cities_data = self.cities_in_google_sheets.json()

    def check_for_code(self):
        if self.cities_data["prices"][0]["iataCode"] == "":
            return True
        else:
            return False
