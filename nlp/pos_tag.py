import enum

import nltk

custom_dictionary = {
    'setup': 'VB',
    'teardown': 'VB'
}


def generate_tag(term):
    if term.lower() in custom_dictionary.keys():
        return custom_dictionary[term.lower()]
    else:
        return (nltk.pos_tag([term])[0][1])


def generate_tags(term_list, append_I=False):
    terms = term_list.copy()
    if append_I:
        terms.insert(0, 'I')
    return (nltk.pos_tag(terms))


def get_tag_text(tag):
    verbs = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    if tag in verbs:
        return POSType.Verb

    nouns = ['NN', 'NNS', 'NNP']
    if tag in nouns:
        return POSType.Noun

    if tag == 'CC':
        return POSType.Conjunction

    if tag == 'IN':
        return POSType.Preposition

    return POSType.Unknown


class POSType(enum.Enum):
    Verb = 1
    Noun = 2
    Preposition = 3
    Conjunction = 4
    Unknown = 0
