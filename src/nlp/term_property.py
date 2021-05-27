from src.nlp import term_list
from src.nlp.pos_tag import generate_tag


def is_singular(project, term):
    custom_plural_terms = term_list.get_plural_terms(project)
    if term in custom_plural_terms:
        return False
    tag = generate_tag(project, term.lower())
    if tag == 'NN' or tag == 'NNP':
        return True
    else:
        return False


def is_plural(project, term):
    custom_plural_terms = term_list.get_plural_terms(project)
    if term in custom_plural_terms:
        return True
    tag = generate_tag(project, term.lower())
    if tag == 'NNS' or tag == 'NNPS':
        return True
    else:
        return False
