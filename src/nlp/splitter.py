from nltk.tokenize import word_tokenize
from spiral import ronin
from spiral.simple_splitters import heuristic_split

from src.common.Singleton import Singleton
from src.nlp import term_list
from src.model.project import Project
from typing import List


class Splitter(metaclass=Singleton):
    """
        Singleton class for splitting text.

        This class provides methods for splitting text into word tokens, splitting names using ronin, and using a heuristic
        approach for splitting names based on a custom dictionary.

        Attributes:
            project (Project): The Project instance with all necessary configurations in it.
    """

    def __init__(self):
        self.project: Project = None  # type: ignore

    def set_project(self, project: Project):
        self.project: Project = project

    @staticmethod
    def split_word_tokens(text: str) -> List[str]:
        """
            Split text into word tokens.

            Args:
                text (str): The input text to split.

            Returns:
                list: A list of word tokens.
        """
        words = word_tokenize(text)
        return [w for w in words if w.isalpha()]

    @staticmethod
    def split_ronin(name):
        """
            Split a name using the 'ronin' splitting method.

            'ronin' is a specific splitting method used to split names.

            Args:
                name (str): The name to split.

            Returns:
                list: A list containing the split parts of the name.

            Note: Find out more about ronin here -> https://github.com/casics/spiral/blob/master/README.md
        """

        this = Splitter()
        custom_dictionary = term_list.get_splitter_terms(this.project)
        if name.lower() in custom_dictionary:
            return [name]
        return ronin.split(name)

    @staticmethod
    def split_heuristic(name: str) -> List[str]:
        """
            Split a name using a heuristic approach based on a custom dictionary.

            Unlike other methods in this class, 'split_heuristic' uses a heuristic approach that relies on a custom dictionary
            to split names. It replaces terms in the name with placeholders, performs the split, and then restores the original terms.

            Args:
                name (str): The name to split.

            Returns:
                list: A list containing the split parts of the name.
        """
        this = Splitter()
        custom_dictionary = term_list.get_splitter_terms(this.project)
        if name.lower() in custom_dictionary:
            return [name]

        replaced = {}
        for index, term in enumerate(custom_dictionary):
            if term in name:
                formatted_index = "{0:0>5}".format(index)
                replaced[str(formatted_index)] = term
                name = name.replace(term, '_' + str(formatted_index) + '_')

        split = heuristic_split(name)
        for index, term in enumerate(split):
            if term in replaced:
                split[index] = replaced.get(term)

        return split  # type: ignore
