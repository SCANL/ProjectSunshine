from app.model.project import ConfigCustomFileType

splitter_terms = [
    'setup',
    'teardown',
    'cleanup',
    'shutdown',
    'SVN',
    'JSON',
    'API'
    'PDF',
    'TTL',
    'ASCII',
    'Endpoint',
    'TLS',
    'SUT',
    'XML',
    'Pojo',
    'URL'
]

pos_terms = {
    "setup": "VB",
    "teardown": "VB"
}

plural_terms = ["apps"
                ]

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
             'give']

set_terms = ['set']


def get_splitter_terms(project):
    terms = []
    terms.extend(splitter_terms)
    custom_terms = project.get_config_value(ConfigCustomFileType.Terms, 'Splitter', 'splitter_terms')
    if custom_terms is not None:
        terms.extend(custom_terms)
    return terms


def get_pos_terms(project):
    terms = {}
    terms.update(pos_terms)
    custom_terms = project.get_config_value(ConfigCustomFileType.Terms, 'POS', 'pos_terms')
    if custom_terms is not None:
        terms.update(custom_terms)
    return terms


def get_plural_terms(project):
    terms = []
    terms.extend(plural_terms)
    custom_terms = project.get_config_value(ConfigCustomFileType.Terms, 'Plural', 'plural_terms')
    if custom_terms is not None:
        terms.extend(custom_terms)
    return terms


def get_transform_terms_staring(project):
    terms = []
    terms.extend(transform_terms_staring)
    custom_terms = project.get_config_value(ConfigCustomFileType.Terms, 'Terms', 'transform_terms_staring')
    if custom_terms is not None:
        terms.extend(custom_terms)
    return terms


def get_transform_terms_inner(project):
    terms = []
    terms.extend(transform_terms_inner)
    custom_terms = project.get_config_value(ConfigCustomFileType.Terms, 'Terms', 'transform_terms_inner')
    if custom_terms is not None:
        terms.extend(custom_terms)
    return terms


def get_conditional_terms(project):
    terms = []
    terms.extend(conditional_terms)
    custom_terms = project.get_config_value(ConfigCustomFileType.Terms, 'Terms', 'conditional_terms')
    if custom_terms is not None:
        terms.extend(custom_terms)
    return terms


def get_validate_terms(project):
    terms = []
    terms.extend(validate_terms)
    custom_terms = project.get_config_value(ConfigCustomFileType.Terms, 'Terms', 'validate_terms')
    if custom_terms is not None:
        terms.extend(custom_terms)
    return terms


def get_boolean_terms(project):
    terms = []
    terms.extend(boolean_terms)
    custom_terms = project.get_config_value(ConfigCustomFileType.Terms, 'Terms', 'boolean_terms')
    if custom_terms is not None:
        terms.extend(custom_terms)
    return terms


def get_get_terms(project):
    terms = []
    terms.extend(get_terms)
    custom_terms = project.get_config_value(ConfigCustomFileType.Terms, 'Terms', 'get_terms')
    if custom_terms is not None:
        terms.extend(custom_terms)
    return terms


def get_set_terms(project):
    terms = []
    terms.extend(set_terms)
    custom_terms = project.get_config_value(ConfigCustomFileType.Terms, 'Terms', 'set_terms')
    if custom_terms is not None:
        terms.extend(custom_terms)
    return terms