from datetime import datetime

from model.identifier_type import IdentifierType
from model.issue import Issue


class AnnotationTest:

    def __init__(self):
        self.__entity = None
        self.__junit = 4#None
        self.__issues = []
        self.__issue_category = 'Redundant use of \'test\' in method name'
        self.__issue_description = 'Replace the term \'test\' in the method name with the \'Test\' annotation'

    def __get_junit_version(self):
        pass

    def __process_identifier(self, identifier):
        if self.__junit >= 4:
            if identifier.name_terms[0].lower() == 'test':
                issue = Issue()
                issue.file_path = self.__entity.path
                issue.identifier = identifier.name_fq
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
