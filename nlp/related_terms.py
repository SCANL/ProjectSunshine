from itertools import chain

from nltk.corpus import wordnet


def get_synonyms(term, pos):
    synonym_terms = []
    synonyms = wordnet.synsets(term)
    for synonym in synonyms:
        if synonym.pos() == pos:
            synonym_terms.extend(synonym.lemma_names())

    return set(synonym_terms)
    #return set(chain.from_iterable([word.lemma_names() for word in synonyms]))


#z = get_synonyms('return','v')
#print(z)