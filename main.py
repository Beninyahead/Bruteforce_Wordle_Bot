from datetime import date 
from word_handler import WordHandler
from wordle_web_driver import WordleWebDriver
from notify import send_sms_notification

ATTEMPTS = 6
FILEPATH = 'word_list.txt'

display_page = True

word_handler = WordHandler(FILEPATH)
webdriver = WordleWebDriver(word_handler,display_page)


while webdriver.word_of_the_day is None: 
    guess = word_handler.guess_a_word()
    # check guess count is about to go over the limit: 
    if word_handler.count > ATTEMPTS and word_handler.count % ATTEMPTS == 1:
        print('reseting game instance')
        # reboot the driver, starting a new instance
        webdriver.browser.quit()
        webdriver = WordleWebDriver(word_handler, display_page)
    # Send and check data
    webdriver.send_word(guess)
    webdriver.check_letters(guess)
    word_handler.filter_word_list()

webdriver.browser.quit()

message = f'Wordle for {date.today()} is "{webdriver.word_of_the_day.upper()}", '\
          f'got it on guess number {word_handler.count}, '\
          f'number of available words remaining were {len(word_handler.available_words)}.'
# print(message)
send_sms_notification(message)
