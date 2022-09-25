import os
from twilio.rest import Client
import smtplib

TWILIO_ACCOUNT_SID = os.environ["TW_ACC_SID"]
TWILIO_AUTH_TOKEN = os.environ["TW_TOKEN"]
TWILIO_PHONE_NUMBER = os.environ["TW_PHN"]
MY_PHONE_NUMBER = os.environ["MY_PHN"]
MY_EMAIL = os.environ["MY_EMAIL"]
MY_PASSWORD = os.environ["MY_PASSWORD"]


class NotificationManager:
    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        self.message = None
        self.from_loc = None
        self.to_loc = None
        self.from_date = None
        self.to_date = None

    def send_message(self, price, city_from, dep_code, city_to, des_code, date_from, date_to, stopovers=0, viacity=""):
        self.from_loc = dep_code
        self.to_loc = des_code
        self.from_date = date_from
        self.to_date = date_to
        if stopovers != 0:
            self.message = f"Low price alert! Only ${price} " \
                      f"to fly from {city_from}-{dep_code} to {city_to}-{des_code}, " \
                      f"from {date_from} to {date_to}.\n\n" \
                      f"Flight has {stopovers} stop over, via {viacity}."
        else:
            self.message = f"Low price alert! Only ${price} " \
                      f"to fly from {city_from}-{dep_code} to {city_to}-{des_code}, " \
                      f"from {date_from} to {date_to}."
        sent_message = self.client.messages.create(body=self.message, from_=TWILIO_PHONE_NUMBER, to=MY_PHONE_NUMBER)
        print(sent_message.status)

    def send_emails(self, to_email):
        flight_link = f"https://www.google.co.uk/flights?hl=en#flt={self.from_loc}.{self.to_loc}.{self.from_date}*{self.to_loc}.{self.from_loc}.{self.to_date} "
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=to_email,
                msg=f"{self.message}\n{flight_link}"
            )
