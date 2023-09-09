from itertools import product

from nltk import word_tokenize
from nltk.corpus import wordnet, stopwords

from src.common.util import remove_list_nestings
from typing import Union, List


def remove_stopwords(term_list: List[str]) -> List[str]:
    """
        Remove stopwords from a list of terms.

        Args:
            term_list (List[str]): The list of terms from which stopwords are to be removed.

        Returns:
            List[str]: A list of terms with stopwords removed.
    """
    stop_words = stopwords.words('english')
    cleansed_terms = [i for i in term_list if not i in stop_words]
    return cleansed_terms


def clean_text(text: Union[str, List[str]], return_unique: bool = False) -> List[str]:
    """
        Clean and tokenize text.

        Args:
            text (Union[str, List[str]]): The input text as a string or a list of strings.
            return_unique (bool, optional): Whether to return unique tokens. Default is False.

        Returns:
            List[str]: A list of cleaned and tokenized words from the input text.
    """

    symbols = ['\t', '\r', '\n', '@', '?', '"', ':', '|', '<', '>', '.', ',', '\\', '/', '//', '#', '!', '$', '%', '^',
               '&', '*', ';', ':', '{',
               '}', '=', '-', '_', '`', '~', '(', ')']

    if type(text) is list:
        text = remove_list_nestings(text)  # type: ignore
        text = ' '.join(text)

    for symbol in symbols:
        text = text.replace(symbol, ' ')  # type: ignore
    text = text.strip()  # type: ignore
    tokenized_text = word_tokenize(text)
    tokenized_text = [i for i in tokenized_text if not i in symbols]
    if return_unique:
        tokenized_text = list(set(tokenized_text))
    return tokenized_text


def are_antonyms(term1: str, term2: str) -> bool:
    """
        Check if two terms are antonyms.

        Args:
            term1 (str): The first term.
            term2 (str): The second term.

        Returns:
            bool: True if the terms are antonyms, False otherwise.
    """

    match = False

    syns1 = wordnet.synsets(term1.lower())
    syns2 = wordnet.synsets(term2.lower())

    for sys1, sys2 in product(syns1, syns2):
        for lemma1, lemma2 in product(sys1.lemmas(), sys2.lemmas()):
            for antonym1, lemma2 in product(lemma1.antonyms(), sys2.lemmas()):
                if antonym1.name() == lemma2.name():
                    match = True
                    break
            for lemma1, antonym2 in product(sys1.lemmas(), lemma2.antonyms()):
                if antonym2.name() == lemma1.name():
                    match = True
                    break

    return match


def get_synonyms(term: str, pos: str) -> set[str]:
    """
        Get synonyms for a term based on its part-of-speech (POS).

        Args:
            term (str): The term for which synonyms are to be retrieved.
            pos (str): The part-of-speech (POS) of the term.

        Returns:
            set: A set of synonyms for the given term and POS.
    """
    synonym_terms = []
    synonyms = wordnet.synsets(term)
    for synonym in synonyms:
        if synonym.pos() == pos:
            synonym_terms.extend(synonym.lemma_names())

    return set(synonym_terms)
