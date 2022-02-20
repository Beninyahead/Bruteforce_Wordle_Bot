from word_handler import WordHandler
from wordle_web_driver import WordleWebDriver

ATTEMPTS = 6
FILEPATH = 'word_list.txt'

word_handler = WordHandler(FILEPATH)
webdriver = WordleWebDriver(word_handler)


while webdriver.word_of_the_day == None: 
    guess = word_handler.guess_a_word()
    # check guess count is about to go over the limit: 
    if word_handler.count > ATTEMPTS and word_handler.count % ATTEMPTS == 1:
        print('reseting game instance')
        # reboot the driver, starting a new instance
        webdriver.browser.quit()
        webdriver = WordleWebDriver(word_handler)
    # Send and check data
    webdriver.send_word(guess)
    webdriver.check_letters(guess)
    word_handler.filter_word_list()


print(f"Word was {webdriver.word_of_the_day}")
webdriver.browser.quit()
