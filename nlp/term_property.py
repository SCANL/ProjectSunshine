from nlp.pos_tag import generate_tag

custom_plural_terms = ['apps']

def is_singular(term):
    if term in custom_plural_terms:
        return False
    tag = generate_tag(term)
    if tag == 'NN' or tag == 'NNP':
        return True
    else:
        return False


def is_plural(term):
    if term in custom_plural_terms:
        return True
    tag = generate_tag(term)
    if tag == 'NNS' or tag == 'NNPS':
        return True
    else:
        return False
