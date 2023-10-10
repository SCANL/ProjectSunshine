from typing import List, Union
from src.common.enum import FileType, IdentifierType, LanguageType
from src.common.testing_list import get_test_method_annotations
from src.common.types_list import get_bool_types
from src.model.entity import Entity
from src.model.identifier import Class, Attribute, Property, Parameter, Method, Variable

SRCML_URL = 'http://www.srcML.org/srcML/src'


def get_class_attribute_names(entity_class: Class) -> List[str]:
    """
        Get the names of attributes for a given entity class.

        Args:
            entity_class (Entity): The entity class for which attribute names are retrieved.

        Returns:
            List[str]: A list of attribute names.
    """
    names = []
    for attribute_item in entity_class.attributes:
        names.append(attribute_item.name)
    return names


def get_all_items_in_class(entity_class: Class) -> List[str]:
    """
        Get all items (class, attributes, methods, variables, and parameters) in a given entity class.

        Args:
            entity_class (Entity): The entity class for which items are retrieved.

        Returns:
            List[str]: A list of all items in the entity class, including the class itself, attributes, methods, variables, and parameters.
    """
    items = []
    items.append(entity_class)
    for attribute_item in entity_class.attributes:
        items.append(attribute_item)
    for method_item in entity_class.methods:
        items.append(method_item)
        for variable_item in method_item.variables:
            items.append(variable_item)
        for parameter_item in method_item.parameters:
            items.append(parameter_item)

    return items


def get_all_class_fields(entity_class: Class):
    """
        Get all class fields (attributes, method variables, and method parameters) in a given entity class.

        Args:
            entity_class (Entity): The entity class for which class fields are retrieved.

        Returns:
            List[str]: A list of all class fields in the entity class, including attributes, method variables, and method parameters.
    """
    items = []
    for attribute_item in entity_class.attributes:
        items.append(attribute_item)
    for method_item in entity_class.methods:
        for variable_item in method_item.variables:
            items.append(variable_item)
        for parameter_item in method_item.parameters:
            items.append(parameter_item)

    return items


def get_all_exception_throws(method):
    return method.xpath('.//src:throw', namespaces={'src': SRCML_URL})


def get_all_return_statements(method):
    return method.xpath('.//src:return', namespaces={'src': SRCML_URL})


def get_all_function_calls(method):
    return method.xpath('.//src:call/src:name/text()', namespaces={'src': SRCML_URL})


def get_all_conditional_statements(method):
    statements = {}
    statements_total = 0

    statement_while = method.xpath(
        './/src:while', namespaces={'src': SRCML_URL})
    statements['while'] = statement_while
    statements_total += len(statement_while)

    statement_do = method.xpath(
        './/src:do', namespaces={'src': SRCML_URL})
    statements['do'] = statement_do
    statements_total += len(statement_do)

    statement_for = method.xpath(
        './/src:for', namespaces={'src': SRCML_URL})
    statements['for'] = statement_for
    statements_total += len(statement_for)

    statement_if2 = method.xpath(
        './/src:if_stmt', namespaces={'src': SRCML_URL})
    statements['if_stmt'] = statement_if2
    statements_total += len(statement_if2)

    statement_switch = method.xpath(
        './/src:switch', namespaces={'src': SRCML_URL})
    statements['switch'] = statement_switch
    statements_total += len(statement_switch)

    statement_ternary = method.xpath(
        './/src:ternary', namespaces={'src': SRCML_URL})
    statements['ternary'] = statement_ternary
    statements_total += len(statement_ternary)

    return statements, statements_total


def is_test_method(project, entity: Entity, identifier: Union[Class, Attribute, Property, Method, Variable, Parameter]) -> bool:
    """
        Check if an identifier is a test method within a given project and entity.

        Args:
            project: The project to which the entity belongs.
            entity (Entity): The entity to which the identifier belongs.
            identifier (Union[Class, Attribute, Property, Method, Variable, Parameter]): The identifier being checked.

        Returns:
            bool: True if the identifier is a test method; False otherwise.
    """
    if entity.file_type != FileType.Test:
        return False
    if IdentifierType.get_type(type(identifier).__name__) != IdentifierType.Method:
        return False

    annotation_list = get_test_method_annotations(
        project, entity.language)
    if any(item in annotation_list for item in identifier.annotations):
        return True
    if identifier.name_terms[0].lower() == 'test':
        return True
    return False


def is_boolean_type(entity: Entity, identifier: Union[Class, Attribute, Property, Method, Variable, Parameter]) -> bool:
    """
    Check if an identifier has a boolean data type in the context of a given entity.

    Args:
        entity (Entity): The entity in which the identifier is defined.
        identifier (Union[Class, Attribute, Property, Method, Variable, Parameter]): The identifier being checked.

    Returns:
        bool: True if the identifier has a boolean data type; False otherwise.
    """
    if entity.language == LanguageType.Java:
        types = get_bool_types(LanguageType.Java)
        if IdentifierType.get_type(type(identifier).__name__) == IdentifierType.Method:
            return identifier.return_type in types
        else:
            return identifier.type in types
    elif entity.language == LanguageType.CSharp:
        types = get_bool_types(LanguageType.CSharp)
        if IdentifierType.get_type(type(identifier).__name__) == IdentifierType.Method:
            return identifier.return_type in types
        else:
            return identifier.type in types

    return False
