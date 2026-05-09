import os
from dotenv import load_dotenv
from twilio.rest import Client
import yagmail
load_dotenv()
class NotificationManager:

    def __init__(self):
        self.client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv("TWILIO_AUTH_TOKEN"))
        self.app_password = os.getenv("GMAIL_APP_PASSWORD")

    def send_sms(self, message_body):
        message = self.client.messages.create(
            from_= "+12182199382",
            body=message_body,
            to= "+916206068272"
        )
        # Prints if successfully sent.
        print(message.sid)

    def send_emails(self, client_email_list, message):
        yag = yagmail.SMTP("ak1380042@gmail.com", self.app_password)

        for email in client_email_list:
            yag.send(to=email,
                  subject="Flight Deals",
                  contents=message
                  )


