import enum

from src.nlp import term_list


# def initialize_stanford_tagger():
#     path_to_model = util.get_config_setting('stanford', 'path_to_model')
#     path_to_jar = util.get_config_setting('stanford', 'path_to_jar')
#     path_to_java = util.get_config_setting('general', 'path_to_java')
#     os.environ['JAVAHOME'] = path_to_java
#     return StanfordPOSTagger(path_to_model, path_to_jar)
from ..nlp.pos_tagger_stanford import POSTaggerStanford


def generate_tag(project, term):
    custom_dictionary = term_list.get_pos_terms(project)
    if term.lower() in custom_dictionary.keys():
        return custom_dictionary[term.lower()]
    else:
        stanford = POSTaggerStanford()
        return stanford.get_pos(term)
        #tagger = stanford.tagger #initialize_stanford_tagger()
        #tagger.tag([term])[0][1]


# def generate_tags(term_list, append_I=False):
#     terms = term_list.copy()
#     if append_I:
#         terms.insert(0, 'I')
#     tagger = initialize_stanford_tagger()
#     return tagger.tag(terms)


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
