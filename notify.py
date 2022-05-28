import os
import logging
import requests
from twilio.rest import Client
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILLO_FROM = os.getenv('TWILLO_FROM')
TWILLO_TO = os.getenv('TWILLO_TO')

def send_twillo_sms_notification(content:str):
    """Sends a sms to default number with a provided message
    * Twillo account required - will use Twillo credit. 
    * See [Twillo SMS](https://www.twilio.com/docs/sms) for more intonation,
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

def send_textbelt_sms_notification(content:str):
    """Sends a sms to Env variable number with a provided message
    * Textbelt api offers 1 free text a day with key = 'textbelt'
    * See [Textbelt](https://textbelt.com/) for more details.
    """
    logger.info('Sending text message')
    resp = requests.post('https://textbelt.com/text', 
        {
            'phone': TWILLO_TO,
            'message': content,
            'key': 'textbelt',
        }
    )
    logger.info(resp.json())