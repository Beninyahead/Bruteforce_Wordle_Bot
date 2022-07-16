import logging
import random

FIRST_GUESS_WORDS = ['notes','resin','tares','senor']
SECOND_GUESS_WORDS = ['acrid','loath','chino','ducat']

logger = logging.getLogger(__name__)

class WordHandler:
    """* WordHandler loads a list of words form a word file
    * Returns an optimized random word for the first two guesses, and a random word for the remainder.
    * Filters the available_word_list based on known_leeters, present_letters and 
    absent_letters.
    """
   
    def __init__(self, filepath:str) -> None:
        """Initialized the word list, reading the file path to self.available_words

        Args:
            filepath (str): File path to to a txt file of line seperated 5 letter words.
        """
        self.file_path = filepath
        self.known_letters: dict[str, int] = {}
        self.present_letters: dict[str, list[int]] = {}
        self.absent_letters: list[str] = []
        self.available_words: list[str] = []
        self.count = 0
        self.first_word_index: int = None 

        self.__read_words()

    def __read_words(self) -> None:
        """Read file to list"""
        logger.debug(f"reading data from {self.file_path}")
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            data = file.readlines()
            self.available_words = [word.strip().lower() for word in data] 


    def __remove_word(self, word:str) -> None:
        """Remove Word from self.available_Words
        Args:
            word (str): word to remove
        """
        try:
            self.available_words.remove(word)
        except ValueError:
            # raised if a other method has already removed the word.
            pass

    def __remove_words_containing_unavailable_letters(self, word:str) -> None:
        """Remove Words that contain letters that are not available

        Args:
            word (str): word to check
        """
        for letter in self.absent_letters:
            if letter.lower() in word.lower():
                self.__remove_word(word)

    def __remove_words_without_known_values(self, word:str) -> None:
        """Remove Words in list that do not contain a letter at the known index.
        Args:
            word (str): word to check
        """
        for letter, index in self.known_letters.items():
            if letter.lower() != word[index].lower():
                    self.__remove_word(word)

    def __remove_words_without_present_values(self, word:str) -> None:
        """Remove Words in list that do not contain a letter at the known index.
        Args:
            word (str): word to check
        """
        for letter in self.present_letters.keys():
            if letter not in word:
                self.__remove_word(word)
                break

    def __remove_words_with_present_letter_at_unaviable_index(self, word:str) -> None:
        """Remove the word if it has a present letter at a already tried index.

        Args:
            word (str): word to check
        """
        for letter, index_list in self.present_letters.items():
            for index in index_list:
                if word[index] == letter:
                    self.__remove_word(word)
                    break

    def filter_word_list(self) -> None:
        """Brute force Iterate through words, cleansing list"""
        logger.info("Filtering word list")
        for word in self.available_words[:]:
            self.__remove_words_containing_unavailable_letters(word)
            self.__remove_words_without_known_values(word)
            self.__remove_words_without_present_values(word)
            self.__remove_words_with_present_letter_at_unaviable_index(word)

    def update_indexes(self, indexed_results:dict[int, tuple[str, str]]) -> None:
        """Update the Known, absent, and unavailable attributes.

        Args:
            indexed_results (dict[int, tuple[str, str]]): Key value indexed results for word sente eg: `{0: ('l', 'absent'), 1: ('o', 'present')}`
        """
        corrrect_present_letters = [results[0] for _, results in indexed_results.items() if results[1] in ['correct', 'present']]
        for index, results in indexed_results.items():
            letter = results[0]
            state = results[1]
            # for duplicate letters, if absent letter is also marked as present or correct skip it.
            if state == 'absent' and letter not in corrrect_present_letters and letter not in self.absent_letters:
                self.absent_letters.append(letter)
            elif state == 'correct':
                self.known_letters[letter] = index 
            elif state == 'present':
                current_present_indexes = self.present_letters.get(letter, [])
                current_present_indexes.append(index)
                self.present_letters[letter] = current_present_indexes 
        
        #  Log updated data
        logger.info(f'Correct letters: {self.known_letters}')
        logger.info(f'Present letters: {self.present_letters}')
        logger.info(f'Absent letters: {self.absent_letters}')

    def guess_a_word(self) -> str:
        """Selects a random word from wordlists based on self.count
        if count is between 1 and 2: Use Constant, optimized starting words
        else: Use available word list.

        Returns:
            str: a 5 letter word.
        """
        self.count = self.count  + 1
        logger.info(f"Word List length = {len(self.available_words)}")
        if self.count == 1:
            guess = random.choice(FIRST_GUESS_WORDS)
            self.first_word_index = FIRST_GUESS_WORDS.index(guess) 
            self.__remove_word(guess)
            return guess
        elif self.count == 2:
            guess = SECOND_GUESS_WORDS[self.first_word_index]
            self.__remove_word(guess)
            return guess
        else:
            try:
                guess = random.choice(self.available_words)
                self.__remove_word(guess)
            except IndexError:
                # either somthing went wrong with filtering, or word is not in word list.
                return None 
            else:               
                return guess
                
    @property
    def closet_word(self) -> str:
        """Build word string from known indexes"""
        word = ['?','?','?','?','?']
        for letter, index in self.known_letters.items():
            word[index] = letter
        return "".join([letter for letter in word])