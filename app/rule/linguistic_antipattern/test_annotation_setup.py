from datetime import datetime

from app.common.enum import FileType, IdentifierType
from app.model.issue import Issue

# Impacted File: Test
# Impacted identifier: Method


class TestAnnotationSetup:

    def __init__(self):
        self.__entity = None
        self.__project = None
        self.__id = 'X.1'
        self.__junit = 4  # None
        self.__issues = []
        self.__issue_category = '\'Before\' annotation not in use'
        self.__issue_description = 'Utilize the \'Before\' annotation for setup methods'

    def __get_junit_version(self):
        pass

    def __process_identifier(self, identifier):
        if self.__junit >= 4:
            if len(identifier.name_terms) == 1 and \
                    identifier.name_terms[0].lower() == 'setup' and \
                    'Before' not in identifier.annotations:
                issue = Issue()
                issue.file_path = self.__entity.path
                issue.identifier = identifier.get_fully_qualified_name()
                issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                issue.category = self.__issue_category
                issue.details = self.__issue_description
                issue.id = self.__id
                issue.analysis_datetime = datetime.now()
                self.__issues.append(issue)

    def analyze(self, project, entity):
        if entity.file_type == FileType.Test:
            self.__project = project
            self.__entity = entity
            for class_item in self.__entity.classes:
                for method_item in class_item.methods:
                    self.__process_identifier(method_item)

        return self.__issues