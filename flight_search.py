import os
from pprint import pprint

import requests

from flight_data import FlightData


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def get_destination_code(self, city):
        """
        retrieves the IATA code for the passed city
        :param city: string city name
        :return:
        a string IATA code
        """
        header = {"apikey": os.environ.get("TEQUILA_API_KEY")}
        params = {"term": city}

        response = requests.get(url=f"{os.environ.get('TEQUILA_ENDPOINT')}locations/query",
                                params=params,
                                headers=header)
        data = response.json()
        iata_code = data["locations"][0]["code"]
        return iata_code

    def check_flights(self, origin, destination, from_time, to_time):
        """
        function checks the flights available for destination in google sheet
        :param origin: string origin code
        :param destination: string destination code
        :param from_time: string trip start date
        :param to_time: string trip return date
        :return:
        an object of flight data with all information regarding the flights passed to it
        """
        header = {"apikey": os.environ.get("TEQUILA_API_KEY")}
        params = {
            "fly_from": origin,
            "fly_to": destination,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "CAD"
        }

        response = requests.get(url=f"{os.environ.get('TEQUILA_ENDPOINT')}v2/search",
                                params=params,
                                headers=header)

        try:
            data = response.json()["data"][0]
        except IndexError:
            params["max_stopovers"] = 1
            response = requests.get(url=f"{os.environ.get('TEQUILA_ENDPOINT')}v2/search",
                                    params=params,
                                    headers=header)
            try:
                data = response.json()["data"][0]
                pprint(data)
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][1]["cityTo"],
                    destination_airport=data["route"][1]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][2]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"]
                )
                return flight_data
            except IndexError:
                print(f"No flights found for {destination}.")
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            print(f"{flight_data.destination_city}: ${flight_data.price}")
            return flight_data
