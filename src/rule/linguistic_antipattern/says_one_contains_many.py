from datetime import datetime

from src.common.enum import IdentifierType
from src.common.error_handler import ErrorSeverity, handle_error
from src.common.types_list import get_collection_types
from src.common.util_parsing import get_all_class_fields
from src.model.issue import Issue
from src.nlp.term_property import is_singular


class SaysOneContainsMany:

    def __init__(self):
        self.__entity = None
        self.__project = None
        self.__id = 'D.1'
        self.__issues = []
        self.__issue_category = 'Says one but contains many'
        self.__issue_description = 'The name of an attribute suggests a single instance, while its type suggests that the attribute stores a collection of objects.'

    def __process_identifier(self, identifier):
        # AntiPattern: The last term in the name is singular AND the data type is a collection
        try:
            if is_singular(self.__project, identifier.name_terms[-1]):
                if identifier.type in get_collection_types(self.__project, self.__entity.language) or identifier.is_array == True:
                    issue = Issue()
                    issue.file_path = self.__entity.path
                    issue.identifier = identifier.get_fully_qualified_name()
                    issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                    issue.category = self.__issue_category
                    issue.details = self.__issue_description
                    issue.additional_details = 'Last term: \'%s\' Data type: \'%s%s\'' % (identifier.name_terms[-1], identifier.type, '(array)' if identifier.is_array else '')
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
            handle_error('D.1', error_message, ErrorSeverity.Error, False, e)

    def analyze(self, project, entity):
        # Analyze all attributes, variables and parameters in a class
        self.__project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            fields = get_all_class_fields(class_item)
            for field_item in fields:
                self.__process_identifier(field_item)

        return self.__issues
