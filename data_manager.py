import os
import requests


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}
        self.user_data = {}

    def get_destination_data(self):
        """
        calls Sheety api to retrieve google sheet data
        :return: returns prices data from Google sheet
        """
        response = requests.get(url=os.environ.get("SHEETY_ENDPOINT"))
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_data(self):
        """
        updates the iata codes for each city in the Google sheet
        :return:
        """
        for row in self.destination_data:
            update = {
                "price": {
                    "iataCode": row["iataCode"]
                }
            }
            requests.put(url=f"{os.environ.get('SHEETY_ENDPOINT')}/{row['id']}", json=update)

    def create_user(self, f_name, l_name, email):
        """
        creates a new user in google sheet based on passed values
        :param f_name: string first name
        :param l_name: string last name
        :param email: string email
        """
        params = {
            "user": {
                "firstName": f_name,
                "lastName": l_name,
                "email": email
            }
        }
        requests.post(url=os.environ.get("SHEETY_USER_ENDPOINT"), json=params)

    def get_user_emails(self):
        """
        Grabs all the emails from the Google sheet for registered users
        :return: a collection of user information
        """
        response = requests.get(url=os.environ.get("SHEETY_USER_ENDPOINT"))
        data = response.json()
        self.user_data = data["users"]
        return self.user_data
