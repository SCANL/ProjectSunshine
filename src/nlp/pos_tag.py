import enum
from src.model.project import Project
from src.nlp import term_list

from src.nlp.pos_tagger_stanford import POSTaggerStanford


def generate_tag(project: Project, term: str) -> str:
    """
        Generate a part-of-speech (POS) tag for a given term in a specific project.

        This function first checks if the term is present in a custom dictionary specific to the project.
        If the term is found in the custom dictionary, the corresponding POS tag is returned.
        If the term is not in the custom dictionary, it uses the Stanford Part-of-Speech Tagger to generate the POS tag.

        Args:
            project (str): The name of the project or context in which the term is being analyzed.
            term (str): The input term for which the POS tag is to be generated.

        Returns:
            str: The POS tag for the input term.
    """
    custom_dictionary = term_list.get_pos_terms(project)
    if term.lower() in custom_dictionary.keys():
        return custom_dictionary[term.lower()]
    else:
        stanford = POSTaggerStanford()
        return stanford.get_pos(term)


class POSType(enum.Enum):
    Verb = 1
    Noun = 2
    Preposition = 3
    Conjunction = 4
    Unknown = 0


def get_tag_text(tag: str) -> POSType:
    """
        Returns the part of speech type of a given tag.

        Args:
            tag (str): The tag to be analyzed.

        Returns:
            POSType: The part of speech type of the tag.
    """
    verbs = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'MD']
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
