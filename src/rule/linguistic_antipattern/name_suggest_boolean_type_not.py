from datetime import datetime

from src.common.enum import IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.util_parsing import get_all_class_fields, is_boolean_type
from src.model.issue import Issue
from src.nlp import term_list


class NameSuggestBooleanTypeNot:

    def __init__(self):
        self.__entity = None
        self.__project = None
        self.__id = 'D.2'
        self.__issues = []
        self.__issue_category = 'Name suggests boolean but type is not'
        self.__issue_description = 'The name of an attribute suggests that its value is true or false, but its declaring type is not Boolean.'

    def __process_identifier(self, identifier):
        # AntiPattern: The starting term in the name should be a boolean term AND the data type is not a boolean
        try:
            if identifier.name_terms[0].lower() in term_list.get_boolean_terms(self.__project):
                if not is_boolean_type(self.__entity, identifier):
                    issue = Issue()
                    issue.file_path = self.__entity.path
                    issue.identifier = identifier.get_fully_qualified_name()
                    issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                    issue.category = self.__issue_category
                    issue.details = self.__issue_description
                    issue.additional_details = 'Starting term: \'%s\' Data type: \'%s%s\'' % (identifier.name_terms[0], identifier.type, '(array)' if identifier.is_array else '')
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
            handle_error('D.2', error_message, ErrorSeverity.Error, False, e)

    def analyze(self, project, entity):
        # Analyze all attributes, variables and parameters in a class
        self.__project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            fields = get_all_class_fields(class_item)
            for field_item in fields:
                self.__process_identifier(field_item)

        return self.__issues
