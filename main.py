# This file will need to use the DataManager,
# FlightSearch, FlightData, NotificationManager
# classes to achieve the program requirements.

from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import datetime, timedelta

dm = DataManager()
fs = FlightSearch()
nm = NotificationManager()
flight_data = []
user_data = []
ORIGIN = fs.get_destination_code(input("What is your origin of travel? "))
trip_start = datetime.now() + timedelta(days=1)
trip_end = datetime.now() + timedelta(days=(6 * 30))

sheet_data = dm.get_destination_data()

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

    try:

        if flight.price < destination["lowestPrice"]:
            nm.send_sms(message=f"Low price alert! Only £{flight.price} to fly from "
                                f"{flight.origin_city}-{flight.origin_airport} to "
                                f"{flight.destination_city}-{flight.destination_airport}, "
                                f"from {flight.out_date} to {flight.return_date}."
                        )

    # If no flights found the api returns None resulting in an exception
    except AttributeError:
        pass
