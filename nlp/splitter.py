from nltk.tokenize import word_tokenize
from spiral import ronin  # pip install git+https://github.com/casics/spiral.git
from spiral.simple_splitters import heuristic_split

from common.Singleton import Singleton
from nlp import term_list


class Splitter(metaclass=Singleton):

    def __init__(self):
        self.project = None

    def set_project(self, project):
        self.project = project

    @staticmethod
    def split_word_tokens(text):
        words = word_tokenize(text)
        return [w for w in words if w.isalpha()]

    @staticmethod
    def split_ronin(name):
        this = Splitter()
        custom_dictionary = term_list.get_splitter_terms(this.project)
        if name.lower() in custom_dictionary:
            return [name]
        return ronin.split(name)

    @staticmethod
    def split_heuristic(name):
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

        return split
