class FlightData:
    def __init__(self):
        self.flight_details = None
        self.price = None
        self.city_from = None
        self.dep_airport_code = None
        self.city_to = None
        self.des_airport_code = None
        self.date_from = None
        self.date_to = None
        self.stop_overs = 0
        self.via_city = ""

    def manage(self, flight):
        self.price = flight["price"]
        self.city_from = flight["route"][0]["cityFrom"]
        self.dep_airport_code = flight["route"][0]["flyFrom"]
        self.city_to = flight["route"][0]["cityTo"]
        self.des_airport_code = flight["route"][0]["flyTo"]
        self.date_to = flight["route"][1]["local_departure"][0:10]
        self.date_from = flight["route"][0]["local_departure"][0:10]
