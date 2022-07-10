from datetime import date
import logging
import set_up_logging  
from word_handler import WordHandler
from wordle_web_driver import WordleWebDriver
from notify import send_twillo_sms_notification, send_textbelt_sms_notification

# Process constants
ATTEMPTS = 6
FILEPATH = 'word_list.txt'

logger = logging.getLogger("Wordle Main")
logger.info(f"Starting Wordle for today {date.today()}")

# Process variables
display_page = False
word_handler = WordHandler(FILEPATH)
webdriver = WordleWebDriver(display_page)
is_solved = False

while not is_solved: 
    guess = word_handler.guess_a_word()
    if not guess: # if guess is None, end of list, algorithm failed
        break
    # check if guess count is about to go over the limit: 
    if word_handler.count > ATTEMPTS and word_handler.count % ATTEMPTS == 1:
        logger.info('Gone over attempts, reseting game instance')
        # reboot the driver, starting a new instance
        webdriver.browser.quit()
        webdriver = WordleWebDriver(display_page)
    # Send and check data
    webdriver.send_word(guess)
    if webdriver.check_win(guess):
        is_solved = True
        break
    # Extract data and update word handler.
    data = webdriver.extract_word_row_data(guess)
    word_handler.update_indexes(data)
    word_handler.filter_word_list()

webdriver.browser.quit()

if is_solved:
    message = f'Wordle for {date.today()} is "{webdriver.word_of_the_day.upper()}", '\
            f'got it on guess number {word_handler.count}, '\
            f'number of available words remaining were {len(word_handler.available_words)+1}.'
else:
    message = f'Could not solve Worlde for {date.today()}. Word either not in File: {FILEPATH}, or something went wrong with filtering.'

logger.info(f"Message: {message}")

# Uncomment the option you want to run for text notifications
# send_twillo_sms_notification(message)
# send_textbelt_sms_notification(message)