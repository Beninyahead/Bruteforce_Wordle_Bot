from datetime import date
import argparse
import logging

from .word_handler import WordHandler
from .wordle_web_driver import WordleWebDriver
from .notify import send_twillo_sms_notification, send_textbelt_sms_notification
from .configs.config import WORD_FILE_PATH, ATTEMPTS


logger = logging.getLogger(__name__)
logger.info(f"Starting Wordle for today {date.today()}")

def _game_solved_message(is_solved, word_of_the_day:str, guess_number:int, words_remaining:int ) -> str:
    if is_solved:
        message = f'Wordle for {date.today()} is "{word_of_the_day.upper()}", '\
                f'got it on guess number {guess_number}, '\
                f'number of available words remaining were {words_remaining}.'
    else:
        message = f'Could not solve Worlde for {date.today()}. Word either not in File: {WORD_FILE_PATH}, or something went wrong with filtering.'

    logger.info(f"Message: {message}")

    return message

def _send_sms(message:str, option:str):
    """Send SMS Controller function

    Args:
        message (str): Message to send
        option (str): 'textbelt' or `twillo`
    """
    if option.lower() == 'textbelt':
        send_textbelt_sms_notification(message)
    if option.lower() == 'twillo': 
        send_twillo_sms_notification(message)
    if option.lower() not in ['textbelt', 'twillo']:
        logger.error('Cannot sent SMS. option must be `textbelt` or `twillo`')

def _solve_wordle_using_webdriver(sms_option:str= None, display_page:bool=False):
    """Solve Function. Orchestration integration of WordHandler and Webdriver.

    Args:
        sms_option (str, optional): Send SMS to your .env Number, Options: `textbelt` or `twillo` . Defaults to None.
        display_page (bool, optional): Display the browser instance. Defaults to False.
    """
    # Process variables
    word_handler = WordHandler(WORD_FILE_PATH)
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

    message = _game_solved_message(is_solved, webdriver.word_of_the_day, word_handler.count, len(word_handler.available_words)+1 )
    if sms_option is not None:
        _send_sms(message, sms_option)


def main():
    """Main Argument Caller Method
    """
    parser = argparse.ArgumentParser(description='Optional argument for solving the Wordle Game')
    parser.add_argument('--display', '-d', type=bool, help='Display the browser instance', required=False, default=False)
    parser.add_argument('--sms', '-s', type=str, help='Send SMS with results. Options:[`twillo` or `textbelt`]', required=False, default=None)

    display = parser.parse_args().display
    sms = parser.parse_args().sms

    _solve_wordle_using_webdriver(sms, display)



if __name__ == '__main__':
    main()