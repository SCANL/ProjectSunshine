from itertools import product

from nltk.corpus import wordnet


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
    # return set(chain.from_iterable([word.lemma_names() for word in synonyms]))


#z = are_antonyms('sleep', 'run')#get_synonyms('to', 'v')
#print(z)
