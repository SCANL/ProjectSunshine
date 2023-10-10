from typing import List, Dict
from src.model.project import ConfigCustomFileType, Project

splitter_terms = [
    'setup',
    'teardown',
    'cleanup',
    'shutdown',
    'SVN',
    'JSON',
    'API',
    'PDF',
    'TTL',
    'ASCII',
    'Endpoint',
    'TLS',
    'SUT',
    'XML',
    'Pojo',
    "Urls",
    "Url",
    "URL"
]

pos_terms = {
    'setup': 'VB',
    'teardown': 'VB',
    'tabs': 'NNS'
}

plural_terms = [
    'apps',
    'columns',
    'tabs']

transform_terms_staring = ['to',
                           'convert',
                           'change',
                           'transform',
                           'translate',
                           'transmute',
                           'cast',
                           'recast',
                           'turn']

transform_terms_inner = ['2',
                         'to',
                         'into']

conditional_terms = ['if',
                     'condition',
                     'check',
                     'compare',
                     'equate']

validate_terms = ['validate',
                  'ensure',
                  'check',
                  'test',
                  'guarantee',
                  'assert',
                  'verify',
                  'affirm',
                  'confirm']

boolean_terms = ['is',
                 'has',
                 'have',
                 'can',
                 'are',
                 'did']

get_terms = ['get',
             'find',
             'fetch',
             'query',
             'generate',
             'produce',
             'obtain',
             'acquire',
             'develop',
             'return',
             'recall',
             'render',
             'yield',
             'deliver',
             'give',
             'lookup']

set_terms = ['set']


def get_splitter_terms(project: Project) -> List[str]:
    """
        Get the splitter terms for a project.

        Args:
            project: The project for which to retrieve splitter terms.

        Returns:
            list: A list of splitter terms.
    """
    terms: List[str] = []
    terms.extend(splitter_terms)
    custom_terms = project.get_config_value(
        ConfigCustomFileType.Terms, 'Splitter', 'splitter_terms')
    if custom_terms is not None:
        terms.extend(custom_terms)
    return terms


def get_pos_terms(project: Project) -> Dict[str, str]:
    """
        Get the part-of-speech (POS) terms for a project.

        Args:
            project: The project for which to retrieve POS terms.

        Returns:
            dict: A dictionary of POS terms where keys are terms, and values are their POS labels.
    """
    terms: Dict[str, str] = {}
    terms.update(pos_terms)
    custom_terms = project.get_config_value(
        ConfigCustomFileType.Terms, 'POS', 'pos_terms')
    if custom_terms is not None:
        terms.update(custom_terms)
    return terms


def get_plural_terms(project: Project) -> List[str]:
    """
        Get plural terms for a project.

        Args:
            project: The project for which to retrieve plural terms.

        Returns:
            list: A list of plural terms.
    """
    terms = []
    terms.extend(plural_terms)
    custom_terms = project.get_config_value(
        ConfigCustomFileType.Terms, 'Plural', 'plural_terms')
    if custom_terms is not None:
        terms.extend(custom_terms)
    return terms


def get_transform_terms_staring(project: Project) -> List[str]:
    """
        Get terms used to start transformations for a project.

        Args:
            project: The project for which to retrieve starting transformation terms.

        Returns:
            list: A list of starting transformation terms. 
    """

    terms = []
    terms.extend(transform_terms_staring)
    custom_terms = project.get_config_value(
        ConfigCustomFileType.Terms, 'Terms', 'transform_terms_staring')
    if custom_terms is not None:
        terms.extend(custom_terms)
    return terms


def get_transform_terms_inner(project: Project) -> List[str]:
    """
        Get terms used within transformations for a project.

        Args:
            project: The project for which to retrieve inner transformation terms.

        Returns:
            list: A list of inner transformation terms.

        Note:
            This function retrieves inner transform terms, which differ from starting transform terms
            (see `get_transform_terms_starting`). Inner transform terms are words that describe the
            transformation process within sentences, while starting transform terms often indicate the
            beginning of a transformation action.     
    """
    terms = []
    terms.extend(transform_terms_inner)
    custom_terms = project.get_config_value(
        ConfigCustomFileType.Terms, 'Terms', 'transform_terms_inner')
    if custom_terms is not None:
        terms.extend(custom_terms)
    return terms


def get_conditional_terms(project: Project) -> List[str]:
    """
        Get conditional terms for a project.

        Args:
            project: The project for which to retrieve conditional terms.

        Returns:
            list: A list of conditional terms.
    """
    terms = []
    terms.extend(conditional_terms)
    custom_terms = project.get_config_value(
        ConfigCustomFileType.Terms, 'Terms', 'conditional_terms')
    if custom_terms is not None:
        terms.extend(custom_terms)
    return terms


def get_validate_terms(project: Project) -> List[str]:
    """
        Get validation terms for a project.

        Args:
            project: The project for which to retrieve validation terms.

        Returns:
            list: A list of validation terms.
    """
    terms = []
    terms.extend(validate_terms)
    custom_terms = project.get_config_value(
        ConfigCustomFileType.Terms, 'Terms', 'validate_terms')
    if custom_terms is not None:
        terms.extend(custom_terms)
    return terms


def get_boolean_terms(project: Project) -> List[str]:
    """
        Get boolean terms for a project.

        Args:
            project: The project for which to retrieve boolean terms.

        Returns:
            list: A list of boolean terms.
    """
    terms = []
    terms.extend(boolean_terms)
    custom_terms = project.get_config_value(
        ConfigCustomFileType.Terms, 'Terms', 'boolean_terms')
    if custom_terms is not None:
        terms.extend(custom_terms)
    return terms


def get_get_terms(project: Project) -> List[str]:
    """
        Get terms related to retrieving data for a project.

        Args:
            project: The project for which to retrieve data retrieval terms.

        Returns:
            list: A list of data retrieval terms.
    """
    terms = []
    terms.extend(get_terms)
    custom_terms = project.get_config_value(
        ConfigCustomFileType.Terms, 'Terms', 'get_terms')
    if custom_terms is not None:
        terms.extend(custom_terms)
    return terms


def get_set_terms(project: Project) -> List[str]:
    """
        Get terms related to setting data for a project.

        Args:
            project: The project for which to retrieve data setting terms.

        Returns:
            list: A list of data setting terms.
    """
    terms = []
    terms.extend(set_terms)
    custom_terms = project.get_config_value(
        ConfigCustomFileType.Terms, 'Terms', 'set_terms')
    if custom_terms is not None:
        terms.extend(custom_terms)
    return terms
