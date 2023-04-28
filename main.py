# This file will need to use the DataManager,
# FlightSearch, FlightData, NotificationManager
# classes to achieve the program requirements.

from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

dm = DataManager()
fs = FlightSearch()
nm = NotificationManager()
flight_data = []
user_data = []


def check_email(email):
    """
    Confirms the users entered email
    :param email: string email entered by user
    :return: bool
    """
    confirm_email = input("Please confirm your email again to confirm: ")
    if email == confirm_email:
        return True
    print("confirmed email must match entered email, please try again")
    check_email(email)


def welcome_message():
    """
    Welcomes user and asks if they wish to create a user account
    :return:
    """
    is_new = input("Welcome to cheap flights finder!\nRegistering a new user? (Y/N): ")
    if is_new.lower() == "y":
        f_name = input("What is your first name? ")
        l_name = input("What is your last name? ")
        email = input("Please enter your email address: ")
        if check_email(email):
            dm.create_user(f_name, l_name, email)
        print(f"Welcome {email} you're now signed up")


welcome_message()
ORIGIN = fs.get_destination_code(input("What is your origin of travel? "))
trip_start = datetime.now() + timedelta(days=1)
trip_end = datetime.now() + timedelta(days=(6 * 30))
sheet_data = dm.get_destination_data()

choice = input("Send info via sms yes or no?(default is via email): ")

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = fs.get_destination_code(row["city"])

    dm.destination_data = sheet_data
    dm.update_destination_data()

for destination in sheet_data:

    flight = fs.check_flights(origin=ORIGIN,
                              destination=destination["iataCode"],
                              from_time=trip_start,
                              to_time=trip_end)
    flight_data.append(flight)

    if flight is None:
        continue

    if flight.price < destination["lowestPrice"]:
        if choice.lower()[0] == "y":
            message = f'Low price alert! Only £{flight.price} to fly from ' \
                      f'{flight.origin_city}-{flight.origin_airport} to ' \
                      f'{flight.destination_city}-{flight.destination_airport}, ' \
                      f'from {flight.out_date} to {flight.return_date}.'

            if flight.stop_overs > 0:
                message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."
                print(message)

            nm.send_sms(message)
        else:
            users = dm.get_user_emails()
            emails = [row["email"] for row in users]
            names = [row["firstName"] for row in users]

            message = f"Low price alert! Only ${flight.price} to fly from " \
                      f"{flight.origin_city}-{flight.origin_airport} " \
                      f"to {flight.destination_city}-{flight.destination_airport}, " \
                      f"from {flight.out_date} to {flight.return_date}."
            if flight.stop_overs > 0:
                message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

            nm.send_emails(emails, message)
