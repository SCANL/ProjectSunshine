from itertools import product

from nltk import word_tokenize
from nltk.corpus import wordnet, stopwords

from app.common.util import remove_list_nestings


def remove_stopwords(term_list):
    stop_words = stopwords.words('english')
    cleansed_terms = [i for i in term_list if not i in stop_words]
    return cleansed_terms


def clean_text(text, return_unique=False):
    symbols = ['\t', '\r', '\n', '@', '?', '"', ':', '|', '<', '>', '.', ',', '\\', '/', '//', '#', '!', '$', '%', '^',
               '&', '*', ';', ':', '{',
               '}', '=', '-', '_', '`', '~', '(', ')']

    if type(text) is list:
        text = remove_list_nestings(text)
        text = ' '.join(text)

    for symbol in symbols:
        text = text.replace(symbol, ' ')
    text = text.strip()
    tokenized_text = word_tokenize(text)
    tokenized_text = [i for i in tokenized_text if not i in symbols]
    if return_unique:
        tokenized_text = list(set(tokenized_text))
    return tokenized_text


def are_antonyms(term1, term2):
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


def get_synonyms(term, pos):
    synonym_terms = []
    synonyms = wordnet.synsets(term)
    for synonym in synonyms:
        if synonym.pos() == pos:
            synonym_terms.extend(synonym.lemma_names())

    return set(synonym_terms)
