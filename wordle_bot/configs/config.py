import os

CONFIG_DIR  = os.path.dirname(__file__)
ATTEMPTS = 6
WORD_FILE_PATH = os.path.join(CONFIG_DIR, 'word_list.txt')

# Check out the Selenium documentation for the app.
DRIVER_PATH = os.getenv('CHROME_DRIVER')
URL_ENDPOINT ='https://www.nytimes.com/games/wordle/index.html'  

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILLO_FROM = os.getenv('TWILLO_FROM')
TO_NUMBER = os.getenv('TO_NUMBER')
