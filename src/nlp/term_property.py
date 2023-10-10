from src.nlp import term_list
from src.nlp.pos_tag import generate_tag
from src.model.project import Project


def is_singular(project: Project, term: str) -> bool:
    """
        Check if a term is in singular form.

        Args:
            project (Project): The project context for configuration and custom plural terms.
            term (str): The term to check.

        Returns:
            bool: True if the term is in singular form, False otherwise.
    """
    custom_plural_terms = term_list.get_plural_terms(project)
    if term in custom_plural_terms:
        return False
    tag = generate_tag(project, term.lower())
    return tag == 'NN' or tag == 'NNP'


def is_plural(project: Project, term: str) -> bool:
    """
        Check if a term is in plural form.

        Args:
            project (Project): The project context for configuration and custom plural terms.
            term (str): The term to check.

        Returns:
            bool: True if the term is in plural form, False otherwise.
    """
    custom_plural_terms = term_list.get_plural_terms(project)
    if term in custom_plural_terms:
        return True
    tag = generate_tag(project, term.lower())
    return tag == 'NNS' or tag == 'NNPS'
