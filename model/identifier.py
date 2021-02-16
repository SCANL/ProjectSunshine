from nlp import splitter


class Class:

    def __init__(self, name, source):
        self.name = name
        self.source = source
        self.methods = []
        self.attribute = []
        self.name_terms = splitter.split_heuristic(name)


class Attribute:

    def __init__(self, type, name, name_fq, source):
        self.type = type
        self.name = name
        self.source = source
        self.name_terms = splitter.split_heuristic(name)
        self.name_fq = name_fq


class Method:

    def __init__(self, name, annotations, name_fq, source):
        self.name = name
        self.source = source
        self.annotations = annotations
        self.variables = []
        self.parameters = []
        self.name_terms = splitter.split_heuristic(name)
        self.name_fq = name_fq


class Variable:

    def __init__(self, type, name, name_fq, source):
        self.type = type
        self.name = name
        self.source = source
        self.name_terms = splitter.split_heuristic(name)
        self.name_fq = name_fq


class Parameter:

    def __init__(self, type, name, name_fq, source):
        self.type = type
        self.name = name
        self.source = source
        self.name_terms = splitter.split_heuristic(name)
        self.name_fq = name_fq
