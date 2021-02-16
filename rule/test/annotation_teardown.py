from datetime import datetime

from model.identifier_type import IdentifierType
from model.issue import Issue


class AnnotationTeardown:

    def __init__(self):
        self.__entity = None
        self.__junit = 4#None
        self.__issues = []
        self.__issue_category = '\'After\' annotation not in use'
        self.__issue_description = 'Utilize the \'After\' annotation for setup methods'

    def __get_junit_version(self):
        pass

    def __process_identifier(self, identifier):
        if self.__junit >= 4:
            if len(identifier.name_terms) == 1 and \
                    identifier.name_terms[0].lower() == 'teardown' and \
                    'After' not in identifier.annotations:
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
