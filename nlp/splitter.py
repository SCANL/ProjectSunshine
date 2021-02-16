from spiral import ronin  # pip install git+https://github.com/casics/spiral.git
from spiral.simple_splitters import heuristic_split

custom_dictionary = ['AtLeast', 'AllOf', 'setup', 'teardown', 'cleanup', 'shutdown', 'noop', 'Exp4j', 'Neo4j', 'Dom4j',
                     'SVN', 'JSON', 'HEAD', 'Hash', 'API'
                      'PDF', 'TTL', 'Thread', 'ASCII', 'Boolean', 'Number', 'Value',
                     'Set', 'Get', 'Endpoint', 'Expiry', 'BOS', 'Url', 'When', 'With', 'TLS', 'delete', 'SUT', 'XML',
                     'Format', 'Pojo', 'List', 'IP', 'M3', 'IO', 'Bag', 'KO', 'IGNORE', 'TRACE', 'DNC', 'Compress',
                     'SLA', 'H5', 'PATCH', 'Mail', 'URL']

custom_dictionary = list(dict.fromkeys(custom_dictionary))


def split_ronin(name):
    if name.lower() in custom_dictionary:
        return [name]
    return ronin.split(name)


def split_heuristic(name):
    if name.lower() in custom_dictionary:
        return [name]

    replaced = {}
    for index, term in enumerate(custom_dictionary):
        if term in name:
            formatted_index = "{0:0>5}".format(index)
            replaced[str(formatted_index)] = term
            name = name.replace(term, '_' + str(formatted_index) + '_')

    split = heuristic_split(name)
    for index, term in enumerate(split):
        if term in replaced:
            split[index] = replaced.get(term)

    return split
