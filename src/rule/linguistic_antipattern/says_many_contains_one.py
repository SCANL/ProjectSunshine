from datetime import datetime

from typing_extensions import override
from src.common.enum import IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.types_list import get_collection_types, get_numeric_types, get_bool_types
from src.common.util_parsing import get_all_class_fields
from src.model.issue import Issue
from src.nlp import term_list
from src.nlp.term_property import is_plural
from linguistic_antipattern import LinguisticAntipattern

class SaysManyContainsOne(LinguisticAntipattern):

    ID = 'E.1'
    ISSUE_CATEGORY = 'Says many but contains one'
    ISSUE_DESCRIPTION = 'The name of an attribute suggests multiple instances, but its type suggests a single one.'

    def __init__(self):
        super.__init__()

    @override
    def __process_identifier(self, identifier):
        # AntiPattern: The last term in the name is plural AND the data type is not a collection
        try:
            if is_plural(self.__project, identifier.name_terms[-1]):
                if identifier.type not in get_collection_types(self.__project, self.__entity.language) and identifier.is_array != True:
                    message = 'Last term: \'%s\' Data type: \'%s%s\'' % (identifier.name_terms[-1], identifier.type, '(array)' if identifier.is_array else '')
                    if identifier.type in get_numeric_types(self.__entity.language):
                        message = message + '; Data type is numeric, this might be a false-positive'
                    if identifier.type in get_bool_types(self.__entity.language) and (identifier.name_terms[0].lower() in term_list.get_boolean_terms(self.__project) or identifier.name_terms[0].lower() in term_list.get_validate_terms(self.__project)):
                        message = message + '; Data type is boolean and starting term is boolean-based, this might be a false-positive'
                    issue = Issue()
                    issue.file_path = self.__entity.path
                    issue.identifier = identifier.get_fully_qualified_name()
                    issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                    issue.category = self.__issue_category
                    issue.details = self.__issue_description
                    issue.additional_details = message
                    issue.id = self.__id
                    issue.analysis_datetime = datetime.now()
                    issue.file_type = self.__entity.file_type
                    issue.line_number = identifier.line_number
                    issue.column_number = identifier.column_number
                    self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(type(identifier).__name__), self.__entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('E.1', error_message, ErrorSeverity.Error, False, e)

    @override
    def analyze(self, project, entity):
        # Analyze all attributes, variables and parameters in a class
        self.__project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            fields = get_all_class_fields(class_item)
            for field_item in fields:
                self.__process_identifier(field_item)

        return self.__issues
