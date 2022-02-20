from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re

from word_handler import WordHandler
# Module constants
DRIVER_PATH = "C:/Development/chromedriver.exe" # Check out the Selenium documentation for the app.
URL_ENDPOINT ='https://www.nytimes.com/games/wordle/index.html'  
CORRECT_REGEX = re.compile('...............correct', re.VERBOSE)
PRESENT_REGEX = re.compile('...............present', re.VERBOSE)
ABSENT_REGEX = re.compile('...............absent', re.VERBOSE)
WIN_REGEX = re.compile('...............win', re.VERBOSE)

class WordleWebDriver:
    """Selenium Webdriver to interact with Wordle.
    * Each method has a 2sec delay after interacting with the site.
    * Session must be quit manually by using browser.quit().
    """
    def __init__(self, word_handler:WordHandler) -> None:
        """ Initialization a browser session is initialized. 

        Args:
            word_handler (WordHandler): WordHandler instance.
        """
        self.word_handler: WordHandler = word_handler
        self.browser = webdriver.Chrome(executable_path=DRIVER_PATH)
        self.word_of_the_day: str = None 
        self.browser.get(URL_ENDPOINT)
    
        time.sleep(1)
        self.page_element = self.browser.find_element_by_tag_name('html')

        self.page_element.click()

        time.sleep(1)

    def send_word(self, word:str):
        """Sends keys for guessed word to Wordle.

        Args:
            word (str): The guessed word.
        """
        self.page_element.send_keys(word + Keys.ENTER)
        time.sleep(2)

    def check_letters(self, word:str):
        """Compares the keyboard data to the word using regex to select data. 
        if all letters int the word are marked as correct, it is assumed the game is over.
        Args:
            word (str): The word sent to Wordle in self.send_word(word).

        Updates: 
            self.word_handler: known_letters, present_letters and absent_letter lists are updated.
        """
        # Select Keyboard data
        game_app = self.browser.find_element_by_tag_name("game-app")
        game = self.browser.execute_script("return arguments[0].shadowRoot.getElementById('game')", game_app)
        keyboard = game.find_element_by_tag_name("game-keyboard")
        keys = self.browser.execute_script("return arguments[0].shadowRoot.getElementById('keyboard')", keyboard)
        
        time.sleep(2)
        
        keyboard_data = self.browser.execute_script("return arguments[0].innerHTML;",keys)
        correct_letters = [key[0] for key in CORRECT_REGEX.findall(keyboard_data)]

        #check if word is correct
        correct_letters_count = 0
        for letter in word:
            # check if each letter in the word is in the keyboard as correct.
            # this is to handle duplicate letters in a word. There is a small chance that this could be incorrect.
            if letter in correct_letters:
                correct_letters_count = correct_letters_count + 1   
        if correct_letters_count == 5:
            self.word_of_the_day = word
            time.sleep(3) # Keep screen active for displaying win
        else:
            # Update known indexes, do not overwrite existing, does not handle duplicate letters in word:
            for letter in correct_letters:
                try:
                    letter_position = word.index(letter)
                except ValueError:
                    pass
                if letter not in self.word_handler.known_letters:
                    self.word_handler.known_letters[letter] = letter_position
            # update present and unavailable letters
            self.word_handler.present_letters = [key[0] for key in PRESENT_REGEX.findall(keyboard_data)]
            self.word_handler.absent_letters = [key[0] for key in ABSENT_REGEX.findall(keyboard_data)]

            print(f"Correct Letter {correct_letters}, Present Letters {self.word_handler.present_letters}, Absent letters{self.word_handler.absent_letters}")
    