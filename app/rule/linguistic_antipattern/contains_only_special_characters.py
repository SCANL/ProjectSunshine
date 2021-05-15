from datetime import datetime
import re

from app.common.enum import IdentifierType
from app.common.error_handler import handle_error, ErrorSeverity
from app.common.util_parsing import get_all_items_in_class
from app.model.issue import Issue


class ContainsOnlySpecialCharacters:

    def __init__(self):
        self.__entity = None
        self.__project = None
        self.__id = 'X.6'
        self.__issues = []
        self.__issue_category = 'Name contains only special characters'
        self.__issue_description = 'The name of an identifier is composed of only special characters.'

    def __process_identifier(self, identifier):
        # AntiPattern: All characters in the name are special character
        regex = r"^[^a-zA-Z0-9]+$"
        try:
            count = 0
            for character in identifier.name:
                if re.search(regex, character):
                    count = count + 1
            if count == len(identifier.name):
                issue = Issue()
                issue.file_path = self.__entity.path
                issue.identifier = identifier.get_fully_qualified_name()
                issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                issue.category = self.__issue_category
                issue.details = self.__issue_description
                issue.additional_details = ''
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
            handle_error('X.5', error_message, ErrorSeverity.Error, False, e)

    def analyze(self, project, entity):
        # Analyze all attributes, variables and parameters in a class
        self.__project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            fields = get_all_items_in_class(class_item)
            for field_item in fields:
                self.__process_identifier(field_item)

        return self.__issues
