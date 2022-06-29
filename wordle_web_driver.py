import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

logger = logging.getLogger(__name__)

from word_handler import WordHandler
# Module constants
DRIVER_PATH = "C:/Development/chromedriver.exe" # Check out the Selenium documentation for the app.
URL_ENDPOINT ='https://www.nytimes.com/games/wordle/index.html'  

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
        self.page_element = self.browser.find_element(By.TAG_NAME, 'html')
        print(self.page_element)

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

    def __extract_keyboard_data(self, data_state:str) -> list[str]:
        """* Find keyboard browser instance
        * Extact keyboard button data for given data-state as a list 
        
        Args:
            data_state (str): The data-state of the keyboard key value (`correct`, `present`, `absent`).
        
        Returns:
            list[str]: List of letters matching the given data-state 
        """
        keyboard = self.browser.find_element(By.CLASS_NAME, 'Keyboard-module_keyboard__1HSnn')
        keys = keyboard.find_elements(By.TAG_NAME, 'button')
        return [key.get_attribute('data-key') for key in keys if key.get_attribute('data-state') == data_state]


    def check_win(self, word) -> bool:
        """* Use selenium `find_element` `By.CLASS_NAME` to check if a game row has been won

        Args:
            word (str): the word just sent across to wordle.

        Returns:
            Bool: True if game has been won, else False
        """
        logger.debug("checking if game has been won")
        board = self.browser.find_element(By.CLASS_NAME, 'Board-module_board__lbzlf')
        try:
            board.find_element(By.CLASS_NAME, 'Row-module_win__NF7uy')
        except NoSuchElementException:
            logger.debug("Game still active")
            return False
        logger.info(f"Game Won. Word {word}")
        self.word_of_the_day = word
        # keep screen open for win
        time.sleep(1)
        return True

    def __update_known_letters(self, word:str, correct_letters:list) -> None:
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
            if letter_count >= 2:
                if letter not in self.word_handler.present_letters:
                    self.word_handler.present_letters.append(letter)
            else:
                try:
                    letter_position = word.index(letter)
                except ValueError:
                    pass
                else:
                    if letter not in self.word_handler.known_letters:
                        self.word_handler.known_letters[letter] = letter_position
        logger.info(f"Correct Letters {self.word_handler.known_letters}.")
    
    def check_letters(self, word:str) -> None:
        """* Compares the keyboard data to the word. Updates `word_handler`
        
        Args:
            word (str): The word sent to Wordle in self.send_word(word).

        Updates: 
            self.word_handler: known_letters, present_letters and absent_letter lists are updated.
        """
        logger.info("Extracting and checking keyboard data")
        self.__update_known_letters(word, self.__extract_keyboard_data(data_state='correct'))       
        
        # update present and unavailable letters
        for letter in self.__extract_keyboard_data(data_state='present'):
            if letter not in self.word_handler.present_letters:
                self.word_handler.present_letters.append(letter) 
        logger.info(f"Present Letters {self.word_handler.present_letters}.")
        
        for letter in self.__extract_keyboard_data(data_state='absent'):
            if letter not in self.word_handler.absent_letters:
                self.word_handler.absent_letters.append(letter) 
        logger.info(f"Absent letters {self.word_handler.absent_letters}")
    

