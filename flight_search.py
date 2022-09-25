import requests
import os
from flight_data import FlightData
from datetime import datetime

TEQUILA_API_KEY = os.environ["TEQ_API_KEY"]
TEQUILA_FLIGHT_API = "https://api.tequila.kiwi.com/v2/search"
TEQ_HEADER = {
            "Content-Type": "application/json",
            "apikey": TEQUILA_API_KEY
        }


class FlightSearch:
    def __init__(self, flight_data: FlightData):
        self.flight_data = flight_data
        self.flight_json = None
        self.stopover = None

    def get_iata_code(self, city):
        response = requests.get(f"https://api.tequila.kiwi.com/locations/query?term={city}", headers=TEQ_HEADER)
        response.raise_for_status()
        iata_code = response.json()["locations"][0]["code"]
        return iata_code

    def search_for_flight(self, city, tomorrow, six_months):
        self.stopover = False
        fly_to_code = city["iataCode"]
        flight_params = {
            "fly_from": "LON",
            "fly_to": fly_to_code,
            "date_from": tomorrow.strftime("%d/%m/%Y"),
            "date_to": six_months.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 30,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }
        response = requests.get(url=f"https://api.tequila.kiwi.com/v2/search", headers=TEQ_HEADER, params=flight_params)
        try:
            self.flight_json = response.json()["data"][0]
        except IndexError:
            flight_params["max_stopovers"] = 1
            response = requests.get(url=f"https://api.tequila.kiwi.com/v2/search", headers=TEQ_HEADER,
                                    params=flight_params)
            try:
                self.flight_json = response.json()["data"][0]
            except IndexError:
                print(f"No flights available for {fly_to_code}")
                return None
            else:
                lowest_price_available = self.flight_json["price"]
                self.stopover = True
                return lowest_price_available
        else:
            lowest_price_available = self.flight_json["price"]
            return lowest_price_available
