from nlp import splitter


class Class:

    def __init__(self, name, source):
        self.name = name
        self.source = source
        self.methods = []
        self.attributes = []
        self.name_terms = splitter.split_heuristic(name)
        self.block_comment = None

    def set_block_comment(self, comment):
        self.block_comment = comment

class Attribute:

    def __init__(self, type, name, parent_name, is_array, is_generic, source):
        self.type = type
        self.name = name
        self.source = source
        self.name_terms = splitter.split_heuristic(name)
        self.parent_name = parent_name
        self.is_array = is_array
        self.type_terms = splitter.split_heuristic(type)
        self.block_comment = None
        self.type_is_generic = is_generic

    def set_block_comment(self, comment):
        self.block_comment = comment

    def get_fully_qualified_name(self):
        return self.parent_name + '.' + self.name


class Method:

    def __init__(self, name, annotations, parent_name, return_type, is_array, source):
        self.name = name
        self.source = source
        self.annotations = annotations
        self.variables = []
        self.parameters = []
        self.name_terms = splitter.split_heuristic(name)
        self.parent_name = parent_name
        self.return_type = return_type
        self.is_array = is_array
        self.type_terms = splitter.split_heuristic(return_type)
        self.block_comment = None

    def set_block_comment(self, comment):
        self.block_comment = comment

    def get_parameters_as_string(self):
        string_list = []
        for parameter in self.parameters:
            string_list.append(parameter.type if parameter.type is not None else '' + ' ' + parameter.name)
        string = ','.join(string_list)
        return '(' + string + ')'

    def get_fully_qualified_name(self):
        return self.parent_name + '.' + self.name + self.get_parameters_as_string()


class Variable:

    def __init__(self, type, name, is_array, is_generic, source):
        self.type = type
        self.name = name
        self.source = source
        self.name_terms = splitter.split_heuristic(name)
        self.parent_name = None
        self.is_array = is_array
        self.type_terms = splitter.split_heuristic(type)
        self.block_comment = None
        self.type_is_generic = is_generic

    def set_block_comment(self, comment):
            self.block_comment = comment

    def set_parent_name(self, parent_name):
        self.parent_name = parent_name

    def get_fully_qualified_name(self):
        return self.parent_name + '.' + self.name


class Parameter:

    def __init__(self, type, name, is_array, is_generic, source):
        self.type = type
        self.name = name
        self.source = source
        self.name_terms = splitter.split_heuristic(name)
        self.parent_name = None
        self.is_array = is_array
        self.type_terms = splitter.split_heuristic(type)
        self.block_comment = None
        self.type_is_generic = is_generic

    def set_block_comment(self, comment):
        self.block_comment = comment

    def set_parent_name(self, parent_name):
        self.parent_name = parent_name

    def get_fully_qualified_name(self):
        return self.parent_name + '.' + self.name
