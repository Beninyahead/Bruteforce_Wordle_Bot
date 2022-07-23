import logging
import requests
from twilio.rest import Client

from .configs.config import TWILLO_FROM, TO_NUMBER, ACCOUNT_SID, AUTH_TOKEN

logger = logging.getLogger(__name__)


def send_twillo_sms_notification(content:str):
    """Sends a sms to default number with a provided message
    * Twillo account required - will use Twillo credit. 
    * See [Twillo SMS](https://www.twilio.com/docs/sms) for more information.
    """
    logger.info('Sending text message')
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages \
                    .create(
                        body = content,
                        from_ = TWILLO_FROM,
                        to = TO_NUMBER
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
            'phone': TO_NUMBER,
            'message': content,
            'key': 'textbelt',
        }
    )
    logger.info(resp.json())