from datetime import datetime

from common.enum import IdentifierType
from common.util_parsing import get_all_return_statements
from model.issue import Issue
from nlp import custom_terms


class GetNoReturn:

    def __init__(self):
        self.__entity = None
        self.__id = 'B.3'
        self.__issues = []
        self.__issue_category = '\'Get\' method does not return'
        self.__issue_description = 'The name suggests that the method returns something (e.g., name starts with \'get\' or \'return\').'

    def __process_identifier(self, identifier):
        # AntiPattern: The name starts with a get term, but there are no return statements
        if identifier.name_terms[0].lower() in custom_terms.get_terms:
            return_statements = get_all_return_statements(identifier.source)

            if len(return_statements) == 0:
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
