from src.common.enum import IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.types_list import get_collection_types, get_numeric_types, get_bool_types
from src.common.util_parsing import get_all_class_fields
from src.model.entity import Entity
from src.model.issue import Issue
from src.nlp import term_list
from src.nlp.term_property import is_plural


class SaysManyContainsOne:

    ID = 'E.1'
    ISSUE_CATEGORY = 'Says many but contains one'
    ISSUE_DESCRIPTION = 'The name of an attribute suggests multiple instances, but its type suggests a single one.'

    def __init__(self):
        self.__issues = []

    # Override
    def __process_identifier(self, identifier):
        # AntiPattern: The last term in the name is plural AND the data type is not a collection
        try:
            if not is_plural(self.__project, identifier.name_terms[-1]):
                return

            if identifier.type not in get_collection_types(self.__project, self.entity.language) and identifier.is_array != True:
                message = 'Last term: \'%s\' Data type: \'%s%s\'' % (
                    identifier.name_terms[-1], identifier.type, '(array)' if identifier.is_array else '')
                if identifier.type in get_numeric_types(self.entity.language):
                    message = message + '; Data type is numeric, this might be a false-positive'
                if identifier.type in get_bool_types(self.entity.language) and (identifier.name_terms[0].lower() in term_list.get_boolean_terms(self.__project) or identifier.name_terms[0].lower() in term_list.get_validate_terms(self.__project)):
                    message = message + \
                        '; Data type is boolean and starting term is boolean-based, this might be a false-positive'
                issue = Issue(self, identifier)
                issue.additional_details = message
                self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(
                    type(identifier).__name__), self.entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('E.1', error_message, ErrorSeverity.Error, False, e)

    # Override
    def analyze(self, project, entity: Entity):
        # Analyze all attributes, variables and parameters in a class
        self.__project = project
        self.entity = entity
        for class_item in self.entity.classes:
            fields = get_all_class_fields(class_item)
            for field_item in fields:
                self.__process_identifier(field_item)

        return self.__issues
