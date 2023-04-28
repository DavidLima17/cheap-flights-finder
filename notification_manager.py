import smtplib

from twilio.rest import Client
import os

ACCOUNT_SID = os.environ.get("TWILIO_SID")
ACCOUNT_TOKEN = os.environ.get("TWILIO_TOKEN")
OUTGOING_NUMBER = os.environ.get("TWILIO_NUMBER")
RECEIVING_NUMBER = os.environ.get("TWILIO_CONTACT")

MY_EMAIL = "david.lima17@gmail.com"
PASSWORD = "tvbalwajhpmschsu"


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(ACCOUNT_SID, ACCOUNT_TOKEN)

    def send_sms(self, message):
        """
        sends a message to user
        :param message: string message to send via sms
        :return:
        """
        message = self.client.messages.create(
            body=message,
            from_=OUTGOING_NUMBER,
            to=RECEIVING_NUMBER
        )

        # confirm message sent in console
        print(message.sid)

    def send_emails(self, emails, message):
        """
        sends the user an email alerting them of flight deals
        :param emails: string of the users email
        :param message: string of the message to send user
        :return:
        """
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, PASSWORD)
            for email in emails:
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}".encode('utf-8')
                )
