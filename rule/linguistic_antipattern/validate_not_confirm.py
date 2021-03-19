from datetime import datetime

from common.enum import IdentifierType
from common.util_parsing import get_all_exception_throws
from model.issue import Issue
from nlp import custom_terms


class ValidateNotConfirm:

    def __init__(self):
        self.__entity = None
        self.__id = 'B.2'
        self.__issues = []
        self.__issue_category = 'Validation method does not confirm'
        self.__issue_description = 'A validation method does not provide a return value informing whether the validation was successful.'

    def __process_identifier(self, identifier):
        # AntiPattern: The name starts with validate and return type is not boolean and no exception thrown
        if identifier.name_terms[0].lower() in custom_terms.validate_terms:
            if (identifier.return_type != 'boolean' or identifier.return_type != 'Boolean') and \
                    (len(get_all_exception_throws(identifier.source)) == 0):
                issue = Issue()
                issue.file_path = self.__entity.path
                issue.identifier = identifier.get_fully_qualified_name()
                issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                issue.category = self.__issue_category
                issue.details = self.__issue_description
                issue.id = self.__id
                issue.analysis_datetime = datetime.now()
                self.__issues.append(issue)

    def analyze(self, entity):
        # Analyze all methods in a class
        self.__entity = entity
        for class_item in self.__entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
