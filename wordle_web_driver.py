import logging
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

logger = logging.getLogger(__name__)

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
    
    def __init__(self, word_handler:WordHandler, display_page=True) -> None:
        """ Initialization a browser session is initialized. 

        Args:
            word_handler (WordHandler): WordHandler instance.
        """
        self.word_handler: WordHandler = word_handler
        self.word_of_the_day: str = None 
        
        # Set up driver
        options = webdriver.ChromeOptions()
        if not display_page:
            options.headless = True
        self.browser = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
        
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
        # Delete the previous word if it wasn't in the word list
        self.page_element.send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACK_SPACE)
        logger.info(f"Sending word: {word}")
        self.page_element.send_keys(word + Keys.ENTER)
        time.sleep(2)

    def __extract_keyboard_data(self):
        """Find and extract keyboard data from browser instance

        Returns:
            selenium html attribute: keyboard data 
        """
        # Select Keyboard data
        game_app = self.browser.find_element_by_tag_name("game-app")
        game = self.browser.execute_script("return arguments[0].shadowRoot.getElementById('game')", game_app)
        keyboard = game.find_element_by_tag_name("game-keyboard")
        keys = self.browser.execute_script("return arguments[0].shadowRoot.getElementById('keyboard')", keyboard)
        
        time.sleep(2)
        
        return self.browser.execute_script("return arguments[0].innerHTML;",keys)

    def check_win(self, word):
        """Extract Game Board data as html, use REGEX to check if 'win' exists.
        if 'win' exists, then game is won

        Args:
            word (str): the word just sent across to wordle.

        Returns:
            Bool: True if game has been won, else False
        """
        logger.debug("checking if game has been won")
        game_app = self.browser.find_element_by_tag_name("game-app")
        game = self.browser.execute_script("return arguments[0].shadowRoot.getElementById('game')", game_app)
        board_container = game.find_element_by_id('board-container')
        board = board_container.find_element_by_id('board')
        # extract inner html of board for regex
        game_row_data = self.browser.execute_script("return arguments[0].innerHTML;",board)
        check_win = [key[-3:] for key in WIN_REGEX.findall(game_row_data)]
        if check_win:
            logger.info(f"Game Won. Word {word}")
            self.word_of_the_day = word
            # keep screen open for win
            time.sleep(1)
            return True
        logger.debug("Game still active")
        return False

    def __update_known_letters(self, word:str, correct_letters:list):
        """Update known letter index positions. 
        Does not handle duplicate letters in word.

        Args:
            word (str): the word just sent across to wordle.
            correct_letters (list): list of keyboard correct letters
        """
        # Update known indexes, do not overwrite existing, does not handle duplicate letters in word:
        logger.info(f"Check for new known indexes for word: {word}")
        for letter in correct_letters:
            letter_count = word.count(letter)
            if letter_count > 1:
                self.word_handler.present_letters.append(letter)
            else:
                try:
                    letter_position = word.index(letter)
                except ValueError:
                    pass
                else:
                    if letter not in self.word_handler.known_letters:
                        self.word_handler.known_letters[letter] = letter_position
    
    def check_letters(self, word:str):
        """Compares the keyboard data to the word using regex to select data. 
        if all letters int the word are marked as correct, it is assumed the game is over.
        Args:
            word (str): The word sent to Wordle in self.send_word(word).

        Updates: 
            self.word_handler: known_letters, present_letters and absent_letter lists are updated.
        """
        logger.info("Extracting and checking keyboard data")
        keyboard_data = self.__extract_keyboard_data()
        correct_letters = [key[0] for key in CORRECT_REGEX.findall(keyboard_data)]
        self.__update_known_letters(word, correct_letters)       
        # update present and unavailable letters
        for key in PRESENT_REGEX.findall(keyboard_data):
            if key[0] not in self.word_handler.present_letters:
                self.word_handler.present_letters.append(key[0]) 

        for key in ABSENT_REGEX.findall(keyboard_data):
            if key[0] not in self.word_handler.absent_letters:
                self.word_handler.absent_letters.append(key[0]) 

        logger.info(f"Correct Letters {self.word_handler.known_letters}\nPresent Letters {self.word_handler.present_letters}.\nAbsent letters{self.word_handler.absent_letters}")
    

