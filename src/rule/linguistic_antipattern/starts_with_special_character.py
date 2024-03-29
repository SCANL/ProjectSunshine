from datetime import datetime
import re

from src.common.enum import IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.util_parsing import get_all_items_in_class
from src.model.issue import Issue


class StartsWithSpecialCharacter:

    def __init__(self):
        self.__entity = None
        self.__project = None
        self.__id = 'X.5'
        self.__issues = []
        self.__issue_category = 'Name starts with special character'
        self.__issue_description = 'The name of an identifier starts with a special character.'

    def __process_identifier(self, identifier):
        # AntiPattern: The first character in the name is a special character
        regex = r"^[^a-zA-Z0-9]+$"
        try:
            matches = re.search(regex, identifier.name[0])
            if matches:
                issue = Issue()
                issue.file_path = self.__entity.path
                issue.identifier = identifier.get_fully_qualified_name()
                issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                issue.category = self.__issue_category
                issue.details = self.__issue_description
                issue.additional_details = 'Starting character: \'%s\'' % (identifier.name[0])
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
