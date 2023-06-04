from twilio.rest import Client
from .config import *

class SMSHandler:
    _instance = None

    def __new__(cls, account_sid = ACCOUNT_SID, auth_token = AUTH_TOKEN, from_number = TWILIO_NUMBER):
        if not cls._instance:
            cls._instance = super(SMSHandler, cls).__new__(cls)
            cls._instance.client = Client(account_sid, auth_token)
            cls._instance.from_number = from_number
        return cls._instance

    def send_sms(self, to_number, message):
        try:
            self.client.messages.create(
                body = message,
                from_= self.from_number,
                to = to_number
            )
            print("SMS sent successfully")
        except Exception as e:
            print(f"Error sending SMS: {str(e)}")
            
    def send_warning(self, camera_name, to_number):
        self.send_sms(to_number, f'ALERTĂ A-EYE: Acțiune cu potential violent detectată pe camera: {camera_name}.')