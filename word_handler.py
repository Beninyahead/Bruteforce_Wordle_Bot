import random

FIRST_GUESS_WORDS = ['notes','resin','tares','senor']
SECOND_GUESS_WORDS = ['acrid','loath','chino','ducat']

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
        self.known_letters: dict = {}
        self.present_letters: list = []
        self.absent_letters: list = []
        self.available_words: list = []
        self.count = 0
        self.first_word_index: int = None 

        self.__read_words()

    def __read_words(self):
        """Read file to list"""
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            data = file.readlines()
            self.available_words = [word.strip().lower() for word in data] 


    def __remove_word(self, word:str):
        """Remove Word from self.available_Words
        Args:
            word (str): word to remove
        """
        try:
            self.available_words.remove(word)
        except ValueError:
            # raised if a other method has already removed the word.
            pass

    def __remove_words_containing_unavailable_letters(self, word:str):
        """Remove Words that contain letters that are not available

        Args:
            word (str): word to check
        """
        for letter in self.absent_letters:
            if letter.lower() in word.lower():
                self.__remove_word(word)

    def __remove_words_without_known_values(self, word:str):
        """Remove Words in list that do not contain a letter at the known index.
        Args:
            word (str): word to check
        """
        for letter, index in self.known_letters.items():
            if letter.lower() != word[index].lower():
                    self.__remove_word(word)

    def __remove_words_without_present_values(self, word:str):
        """Remove Words in list that do not contain a letter at the known index.
        Args:
            word (str): word to check
        """
        for letter in self.present_letters:
            if letter not in word:
                self.__remove_word(word)

    def filter_word_list(self):
        """Brute force Iterate through words, cleansing list"""
        # Repeat 10 times to ensure no words are missed,
        # this is due to a bug in my logic, where the word list does not filter completley on the first iteration
        for _ in range(10):
            for word in self.available_words:
                self.__remove_words_containing_unavailable_letters(word)
                self.__remove_words_without_known_values(word)
                self.__remove_words_without_present_values(word)
            #print(f"Word list filtered to: {len(self.available_words)}")

    def guess_a_word(self):
        """Selects a random word from wordlists based on self.count
        if count is between 1 and 2: Use Constant, optimized starting words
        else: Use available word list.

        Returns:
            str: a 5 letter word.
        """
        self.count = self.count  + 1
        print(f"Word List length = {len(self.available_words)}")
        if self.count == 1:
            guess = random.choice(FIRST_GUESS_WORDS)
            self.first_word_index = FIRST_GUESS_WORDS.index(guess) 
        elif self.count == 2:
            guess = SECOND_GUESS_WORDS[self.first_word_index]
        else:
            try:
                guess = random.choice(self.available_words)
            except IndexError:
                # Something has gone wrong with filtering. Reload the list and try again.
                self.__read_words()
                self.absent_letters.clear()
                self.known_letters.clear()
                self.present_letters.clear()
                self.guess_a_word()
        self.__remove_word(guess)
        return guess
