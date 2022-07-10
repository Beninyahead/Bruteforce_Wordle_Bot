import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

logger = logging.getLogger(__name__)

# Module constants
DRIVER_PATH = "C:/Development/chromedriver.exe" # Check out the Selenium documentation for the app.
URL_ENDPOINT ='https://www.nytimes.com/games/wordle/index.html'  

class WordleWebDriver:
    """Selenium Webdriver to interact with Wordle.
    * Each method has a 2sec delay after interacting with the site.
    * Session must be quit manually by using browser.quit().
    """
    
    def __init__(self, display_page=True) -> None:
        """ Initialization a browser session is initialized. 

        Args:
            display_page (bool): True to show the browser instance, False to hide. defaults to True.
        """
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

    def send_word(self, word:str) -> None:
        """Sends keys for guessed word to Wordle.

        Args:
            word (str): The guessed word.
        """
        # Delete the previous word if it wasn't in the word list
        self.page_element.send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACK_SPACE)
        logger.info(f"Sending word: {word}")
        self.page_element.send_keys(word + Keys.ENTER)
        time.sleep(2)

    def extract_word_row_data(self, word:str) -> dict[int, tuple[str, str]]:
        """* Find all game row elements
        * Locate row for word just sent
        * iterate ove the row for each key index, extract is data-state
        * Return a Dictionary containing the results  

        Args:
            word (str): word just sent to wordle

        Returns:
            dict[int, tuple[str, str]]: indexed results of word eg: `{0 : (letter, data-state)}` 
        """
        word_index_pair = {}
        rows = self.browser.find_elements(By.CLASS_NAME, 'Row-module_row__dEHfN')
        for row in rows:
            letters = row.find_elements(By.CLASS_NAME, 'Tile-module_tile__3ayIZ')
            row_word = ''.join([row.text for row in letters])
            if row_word.upper() == word.upper():
                for index, letter in enumerate(letters):
                    state = str(letter.get_attribute('data-state'))
                    word_index_pair[index] = (letter.text.lower(), state)
        return word_index_pair


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

