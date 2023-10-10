from src.nlp.splitter import Splitter
from typing import List, Any, Optional

SRCML_LINE_COL_NUMS_XPATH = '{http://www.srcML.org/srcML/position}start'


class Class:
    """
        Represents a class in the source code.
    """

    def __init__(self, name: str, source):
        """
            Initialize a Class object.

            Args:
                name (str): The name of the class.
                source: The source code for the class.
        """
        self.name = name
        self.source = source

        self.methods: List[Method] = []
        self.attributes: List[Attribute] = []
        self.properties: List[Property] = []
        self.name_terms = Splitter().split_heuristic(name)
        self.block_comment: Optional[str] = None
        self.line_number = (
            source.attrib[SRCML_LINE_COL_NUMS_XPATH]).split(':')[0]
        self.column_number = (
            source.attrib[SRCML_LINE_COL_NUMS_XPATH]).split(':')[1]

    def set_block_comment(self, comment: Optional[str]):
        """
            Set the block comment for the class.

            Args:
                comment (str): The block comment for the class.
        """
        self.block_comment = comment


class Attribute:
    """
        Represents an attribute within a class.
    """

    def __init__(self, specifier, type, name, parent_name, is_array: bool, is_generic: bool, source):
        """
        Initialize an Attribute object.

        Args:
            specifier: The attribute specifier (e.g., public, private).
            type: The data type of the attribute.
            name: The name of the attribute.
            parent_name: The name of the parent class.
            is_array (bool): Indicates if the attribute is an array.
            is_generic (bool): Indicates if the attribute type is generic.
            source: The source code for the attribute.
        """

        self.specifier = specifier if specifier is not None else 'default'
        self.type = type
        self.name = name
        self.source = source
        self.name_terms = Splitter().split_heuristic(name)
        self.parent_name = parent_name
        self.is_array = is_array
        self.type_terms = Splitter().split_heuristic(type)
        self.block_comment = None
        self.type_is_generic = is_generic
        self.line_number = (
            source.attrib[SRCML_LINE_COL_NUMS_XPATH]).split(':')[0]
        self.column_number = (
            source.attrib[SRCML_LINE_COL_NUMS_XPATH]).split(':')[1]

    def set_block_comment(self, comment):
        """
            Set the block comment for the attribute.

            Args:
                comment (str): The block comment for the attribute.
        """

        self.block_comment = comment

    def get_fully_qualified_name(self) -> str:
        """
            Get the fully qualified name of the attribute, including the parent class.

            Returns:
                str: The fully qualified name.
        """
        return self.parent_name + '.' + self.name


class Property:
    """
        Represents a property within a class.
    """

    def __init__(self, type, name, parent_name, is_array: bool, is_generic: bool, source):
        """
            Initialize a Property object.

            Args:
                type: The data type of the property.
                name: The name of the property.
                parent_name: The name of the parent class.
                is_array (bool): Indicates if the property is an array.
                is_generic (bool): Indicates if the property type is generic.
                source: The source code for the property.
        """

        self.type = type
        self.name = name
        self.source = source
        self.name_terms = Splitter().split_heuristic(name)
        self.parent_name = parent_name
        self.is_array = is_array
        self.type_terms = Splitter().split_heuristic(type)
        self.block_comment = None
        self.type_is_generic = is_generic
        self.line_number = (
            source.attrib[SRCML_LINE_COL_NUMS_XPATH]).split(':')[0]
        self.column_number = (
            source.attrib[SRCML_LINE_COL_NUMS_XPATH]).split(':')[1]

    def set_block_comment(self, comment: str):
        """
            Set the block comment for the property.

            Args:
                comment (str): The block comment for the property.
        """
        self.block_comment = comment

    def get_fully_qualified_name(self) -> str:
        """
            Get the fully qualified name of the property, including the parent class.

            Returns:
                str: The fully qualified name.
        """
        return self.parent_name + '.' + self.name


class Method:
    """
        Represents a method within a class.
    """

    def __init__(self, specifier, name, annotations, parent_name, return_type, is_array: bool, source):
        """
            Initialize a Method object.

            Args:
                specifier: The method specifier (e.g., public, private).
                name: The name of the method.
                annotations: List of method annotations.
                parent_name: The name of the parent class.
                return_type: The return type of the method.
                is_array (bool): Indicates if the return type is an array.
                source: The source code for the method.
        """

        self.specifier = self.specifier = specifier if specifier is not None else 'default'
        self.name = name
        self.source = source
        self.annotations = annotations
        self.variables: List[Variable] = []
        self.parameters: List[Parameter] = []
        self.name_terms = Splitter().split_heuristic(name)
        self.parent_name = parent_name
        self.return_type = return_type
        self.is_array = is_array
        self.type_terms = Splitter().split_heuristic(return_type)
        self.block_comment = None
        self.line_number = (
            source.attrib[SRCML_LINE_COL_NUMS_XPATH]).split(':')[0]
        self.column_number = (
            source.attrib[SRCML_LINE_COL_NUMS_XPATH]).split(':')[1]

    def set_block_comment(self, comment: Optional[str]):
        """
            Set the block comment for the method.

            Args:
                comment (str): The block comment for the method.
            """
        self.block_comment = comment

    def get_inner_comments(self) -> List[Any]:
        """
            Get inner comments within the method.

            Returns:
                Unknown: List of inner comments.
        """
        return self.source.xpath('.//src:comment', namespaces={'src': 'http://www.srcML.org/srcML/src'})

    def get_all_comments(self, unique_terms=True) -> List[str]:
        """
            Get all comments associated with the method.

            Args:
                unique_terms (bool): Whether to return unique comment terms.

            Returns:
                List[str]: List of comments.
        """

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
        """
            Get the method parameters as a string.

            Returns:
                str: A string representation of method parameters.
        """

        string_list = []
        for parameter in self.parameters:
            string_list.append(
                parameter.type if parameter.type is not None else '' + ' ' + parameter.name)
        string = ','.join(string_list)
        return '(' + string + ')'

    def get_fully_qualified_name(self) -> str:
        """
            Get the fully qualified name of the method, including the parent class.

            Returns:
                str: The fully qualified name.
        """
        return self.parent_name + '.' + self.name + self.get_parameters_as_string()


class Variable:
    """
        Represents a variable within a method.
    """

    def __init__(self, specifier, type, name, is_array: bool, is_generic: bool, source):
        """
            Initialize a Variable object.

            Args:
                specifier: The variable specifier (e.g., public, private).
                type: The data type of the variable.
                name: The name of the variable.
                is_array (bool): Indicates if the variable is an array.
                is_generic (bool): Indicates if the variable type is generic.
                source: The source code for the variable.
        """

        self.specifier = self.specifier = specifier if specifier is not None else 'default'
        self.type = type
        self.name = name
        self.source = source
        self.name_terms = Splitter().split_heuristic(name)
        self.parent_name = None
        self.is_array = is_array
        self.type_terms = Splitter().split_heuristic(type)
        self.block_comment = None
        self.type_is_generic = is_generic
        self.line_number = (
            source.attrib[SRCML_LINE_COL_NUMS_XPATH]).split(':')[0]
        self.column_number = (
            source.attrib[SRCML_LINE_COL_NUMS_XPATH]).split(':')[1]

    def set_block_comment(self, comment):
        """
            Set the block comment for the variable.

            Args:
                comment (str): The block comment for the variable.
        """
        self.block_comment = comment

    def set_parent_name(self, parent_name: str):
        """
            Set the parent name (method or class) to which the variable belongs.

            Args:
                parent_name (str): The name of the parent method or class.
        """
        self.parent_name = parent_name

    def get_fully_qualified_name(self) -> str | None:
        """
            Get the fully qualified name of the variable, including the parent method or class.

            Returns:
                str: The fully qualified name.
        """
        if self.parent_name is not None:
            return self.parent_name + '.' + self.name


class Parameter:
    """
        Represents a parameter passed to a method.
    """

    def __init__(self, type, name, is_array: bool, is_generic: bool, source):
        self.type = type
        self.name = name
        self.source = source
        self.name_terms = Splitter().split_heuristic(name)
        self.parent_name = None
        self.is_array = is_array
        self.type_terms = Splitter().split_heuristic(type)
        self.block_comment = None
        self.type_is_generic = is_generic
        self.line_number = (
            source.attrib[SRCML_LINE_COL_NUMS_XPATH]).split(':')[0]
        self.column_number = (
            source.attrib[SRCML_LINE_COL_NUMS_XPATH]).split(':')[1]

    def set_block_comment(self, comment: str):
        """
            Set the block comment for the parameter.

            Args:
                comment (str): The block comment for the parameter.
        """
        self.block_comment = comment

    def set_parent_name(self, parent_name: str):
        """
            Set the parent name (method or class) to which the parameter belongs.

            Args:
                parent_name (str): The name of the parent method or class.
        """
        self.parent_name = parent_name

    def get_fully_qualified_name(self) -> str | None:
        """
            Get the fully qualified name of the parameter, including the parent method or class.

            Returns:
                str: The fully qualified name.
        """
        if self.parent_name is not None:
            return self.parent_name + '.' + self.name
