from datetime import datetime

from app.common.enum import IdentifierType
from app.model.issue import Issue

# Impacted identifier: All
# Impacted identifier: Method


class SetReturns:

    def __init__(self):
        self.__entity = None
        self.__project = None
        self.__id = 'A.3'
        self.__issues = []
        self.__issue_category = '\'Set\' method returns'
        self.__issue_description = 'A set method having a return type different than \'void\'.'

    def __process_identifier(self, identifier):
        # AntiPattern: The name starts with a set, but the method return type is not void
        if identifier.name_terms[0].lower() == 'set':
            if identifier.return_type != 'void':
                issue = Issue()
                issue.file_path = self.__entity.path
                issue.identifier = identifier.get_fully_qualified_name()
                issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                issue.category = self.__issue_category
                issue.details = self.__issue_description
                issue.additional_details = 'Return type: %s' % identifier.return_type
                issue.id = self.__id
                issue.analysis_datetime = datetime.now()
                issue.file_type = self.__entity.file_type
                issue.line_number = identifier.line_number
                issue.column_number = identifier.column_number
                self.__issues.append(issue)

    def analyze(self, project, entity):
        # Analyze all methods in a class
        self.__project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
