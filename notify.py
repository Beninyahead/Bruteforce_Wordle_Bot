import os
import logging
from twilio.rest import Client
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILLO_FROM = os.getenv('TWILLO_FROM')
TWILLO_TO = os.getenv('TWILLO_TO')

def send_sms_notification(content:str):
    """
    Sends a sms to default number with a provided message
    """
    logger.info('Sending text message')
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages \
                    .create(
                        body = content,
                        from_ = TWILLO_FROM,
                        to = TWILLO_TO
                    )
    logger.info(f"Message Status: {message.status}")           