from datetime import date 
from word_handler import WordHandler
from wordle_web_driver import WordleWebDriver
from notify import send_sms_notification

ATTEMPTS = 6
FILEPATH = 'word_list.txt'

display_page = True

word_handler = WordHandler(FILEPATH)
webdriver = WordleWebDriver(word_handler,display_page)

is_solved = False

while not is_solved: 
    guess = word_handler.guess_a_word()
    if not guess:
        break
    print(f"trying {guess}")
    # check guess count is about to go over the limit: 
    if word_handler.count > ATTEMPTS and word_handler.count % ATTEMPTS == 1:
        print('reseting game instance')
        # reboot the driver, starting a new instance
        webdriver.browser.quit()
        webdriver = WordleWebDriver(word_handler, display_page)
    # Send and check data
    webdriver.send_word(guess)
    webdriver.check_letters(guess)
    if webdriver.word_of_the_day:
        is_solved = True
        break
    word_handler.filter_word_list()

webdriver.browser.quit()

if is_solved:
    message = f'Wordle for {date.today()} is "{webdriver.word_of_the_day.upper()}", '\
            f'got it on guess number {word_handler.count}, '\
            f'number of available words remaining were {len(word_handler.available_words)+1}.'
else:
    message = f'Could not solve Worlde for {date.today()}. ' \
        f'Known Letters: "{word_handler.closet_word}". ' \
        f'Present Letters: {word_handler.present_letters}. Absent Letters: {word_handler.absent_letters}'

print(message)
# send_sms_notification(message)
