from twilio.rest import Client
import os

ACCOUNT_SID = os.environ.get("TWILIO_SID")
ACCOUNT_TOKEN = os.environ.get("TWILIO_TOKEN")
OUTGOING_NUMBER = os.environ.get("TWILIO_NUMBER")
RECEIVING_NUMBER = os.environ.get("TWILIO_CONTACT")


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
