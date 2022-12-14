from ctypes import *
from pathlib import Path
import platform

if platform.system() == "Windows":
    ext = ".dll"
else:
    ext = ".so"
CFILE = Path(__file__).parent / ("gamelogic" + ext)


class CBridge:
    """
    Ensures communication between Python and C
    """
    def __init__(self):
        self.gamelogic = CDLL(str(CFILE))

        # configuring the arguments type and return type of
        # int* interpret(const char* word)
        self.gamelogic.interpret.argtypes = [c_char_p]
        self.gamelogic.interpret.restype = POINTER(c_int)
        self.gamelogic.get_secret_word.restype = c_char_p
        self.gamelogic.is_valid.argtypes = [c_char_p]
        self.gamelogic.is_valid.restype = c_bool

    def init(self):
        """
        Initializes words list in C
        """
        self.gamelogic.init()

    def interpret(self, word: str):
        """
        Checks the try of the player
        :param word: The word to check
        :return: An array of int values.
        Refer to the documentation in "gamelogic.c" for more details
        """
        result = self.gamelogic.interpret(word.lower().encode())
        return result

    def reset_word(self):
        """
        Picks up a new word randomly
        """
        self.gamelogic.reset_word()

    def get_secret_word(self):
        """
        :return: The answer that the player is trying to guess
        """
        return self.gamelogic.get_secret_word().decode("UTF-8")

    def is_word_valid(self, word):
        """
        Checks whether a word is valid grammatically speaking
        :param word: The target word
        :return: The validity of the world
        """
        return self.gamelogic.is_valid(word.lower().encode())


__all__ = ["CBridge"]
