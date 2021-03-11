from datetime import datetime

from common.util_parsing import get_all_return_statements
from model.identifier_type import IdentifierType
from model.issue import Issue


class GetNoReturn:
    custom_terms = ['find',
                    'fetch',
                    'query',
                    'generate',
                    'produce',
                    'obtain',
                    'acquire',
                    'develop',
                    'return',
                    'recall',
                    'render',
                    'yield',
                    'deliver',
                    'give']

    def __init__(self):
        self.__entity = None
        self.__id = 'B.3'
        self.__issues = []
        self.__issue_category = '\'Get\' method does not return'
        self.__issue_description = 'The name suggests that the method returns something (e.g., name starts with \'get\' or \'return\')'

    def __process_identifier(self, identifier):

        if identifier.name_terms[0].lower() in self.custom_terms:
            return_statements = get_all_return_statements(identifier.source)

            if len(return_statements) == 0:
                issue = Issue()
                issue.file_path = self.__entity.path
                issue.identifier = identifier.get_fully_qualified_name()
                issue.identifier_type = IdentifierType.Method
                issue.category = self.__issue_category
                issue.details = self.__issue_description
                issue.analysis_datetime = datetime.now()
                self.__issues.append(issue)

    def analyze(self, entity):
        self.__entity = entity
        for class_item in self.__entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
