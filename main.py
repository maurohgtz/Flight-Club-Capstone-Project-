from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from flight_data import FlightData
from datetime import datetime, timedelta
from pprint import pprint

flight_data = FlightData()
twilio_app = NotificationManager()
flight_search = FlightSearch(flight_data)
google_sheets_or_sum_idk = DataManager(flight_search)
tomorrow = datetime.now() + timedelta(days=1)
six_months_from_today = datetime.now() + timedelta(days=6 * 30)

if google_sheets_or_sum_idk.check_for_code():
    google_sheets_or_sum_idk.add_iata_code()

for city in google_sheets_or_sum_idk.cities_data["prices"]:
    lowest_price = city["lowestPrice"]
    try:
        if flight_search.search_for_flight(city, tomorrow, six_months_from_today) <= lowest_price:
            if flight_search.stopover:
                flight_data.stop_overs = 1
                flight_data.via_city = flight_search.flight_json["route"][0]["cityTo"]
            flight_data.manage(flight_search.flight_json)
            twilio_app.send_message(
                price=flight_data.price, city_from=flight_data.city_from, dep_code=flight_data.dep_airport_code,
                city_to=flight_data.city_to, des_code=flight_data.des_airport_code,
                date_from=flight_data.date_from, date_to=flight_data.date_to, stopovers=flight_data.stop_overs,
                viacity=flight_data.via_city
            )
            for email in google_sheets_or_sum_idk.list_of_users_emails:
                twilio_app.send_emails(email)

        else:
            print("Flights available but too expensive")
    except TypeError:
        pass
