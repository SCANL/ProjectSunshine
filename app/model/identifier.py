from app.nlp.splitter import Splitter


class Class:

    def __init__(self, name, source):
        # splitter = Splitter()
        self.name = name
        self.source = source
        self.methods = []
        self.attributes = []
        self.properties = []
        self.name_terms = Splitter().split_heuristic(name)
        self.block_comment = None
        self.line_number = (source.attrib['{http://www.srcML.org/srcML/position}start']).split(':')[0]

    def set_block_comment(self, comment):
        self.block_comment = comment


class Attribute:

    def __init__(self, type, name, parent_name, is_array, is_generic, source):
        # splitter = Splitter()
        self.type = type
        self.name = name
        self.source = source
        self.name_terms = Splitter().split_heuristic(name)
        self.parent_name = parent_name
        self.is_array = is_array
        self.type_terms = Splitter().split_heuristic(type)
        self.block_comment = None
        self.type_is_generic = is_generic
        self.line_number = (source.attrib['{http://www.srcML.org/srcML/position}start']).split(':')[0]

    def set_block_comment(self, comment):
        self.block_comment = comment

    def get_fully_qualified_name(self):
        return self.parent_name + '.' + self.name


class Property:
    def __init__(self, type, name, parent_name, is_array, is_generic, source):
        # splitter = Splitter()
        self.type = type
        self.name = name
        self.source = source
        self.name_terms = Splitter().split_heuristic(name)
        self.parent_name = parent_name
        self.is_array = is_array
        self.type_terms = Splitter().split_heuristic(type)
        self.block_comment = None
        self.type_is_generic = is_generic
        self.line_number = (source.attrib['{http://www.srcML.org/srcML/position}start']).split(':')[0]

    def set_block_comment(self, comment):
        self.block_comment = comment

    def get_fully_qualified_name(self):
        return self.parent_name + '.' + self.name


class Method:

    def __init__(self, name, annotations, parent_name, return_type, is_array, source):
        # splitter = Splitter()
        self.name = name
        self.source = source
        self.annotations = annotations
        self.variables = []
        self.parameters = []
        self.name_terms = Splitter().split_heuristic(name)
        self.parent_name = parent_name
        self.return_type = return_type
        self.is_array = is_array
        self.type_terms = Splitter().split_heuristic(return_type)
        self.block_comment = None
        self.line_number = (source.attrib['{http://www.srcML.org/srcML/position}start']).split(':')[0]

    def set_block_comment(self, comment):
        self.block_comment = comment

    def get_inner_comments(self):
        return self.source.xpath('.//src:comment', namespaces={'src': 'http://www.srcML.org/srcML/src'})

    def get_all_comments(self, unique_terms=True):
        # splitter = Splitter()
        comments = []
        if self.block_comment is not None:
            comments.append(self.block_comment)
        for comment in self.get_inner_comments():
            comments.append(comment.text)

        if not unique_terms:
            return comments
        else:
            terms = []
            for comment in comments:
                terms.extend(Splitter().split_word_tokens(comment))
            return list(set(terms))

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
        # splitter = Splitter()
        self.type = type
        self.name = name
        self.source = source
        self.name_terms = Splitter().split_heuristic(name)
        self.parent_name = None
        self.is_array = is_array
        self.type_terms = Splitter().split_heuristic(type)
        self.block_comment = None
        self.type_is_generic = is_generic
        self.line_number = (source.attrib['{http://www.srcML.org/srcML/position}start']).split(':')[0]

    def set_block_comment(self, comment):
        self.block_comment = comment

    def set_parent_name(self, parent_name):
        self.parent_name = parent_name

    def get_fully_qualified_name(self):
        return self.parent_name + '.' + self.name


class Parameter:

    def __init__(self, type, name, is_array, is_generic, source):
        # splitter = Splitter()
        self.type = type
        self.name = name
        self.source = source
        self.name_terms = Splitter().split_heuristic(name)
        self.parent_name = None
        self.is_array = is_array
        self.type_terms = Splitter().split_heuristic(type)
        self.block_comment = None
        self.type_is_generic = is_generic
        self.line_number = (source.attrib['{http://www.srcML.org/srcML/position}start']).split(':')[0]

    def set_block_comment(self, comment):
        self.block_comment = comment

    def set_parent_name(self, parent_name):
        self.parent_name = parent_name

    def get_fully_qualified_name(self):
        return self.parent_name + '.' + self.name
