from datetime import datetime

from app.common.enum import FileType, IdentifierType, LanguageType
from app.common.error_handler import handle_error, ErrorSeverity
from app.model.issue import Issue

# Impacted File: Test
# Impacted identifier: Method


class TestAnnotationTest:

    def __init__(self):
        self.__entity = None
        self.__project = None
        self.__id = 'X.3'
        self.__junit = 4#None
        self.__issues = []
        self.__issue_category = 'Redundant use of \'test\' in method name'
        self.__issue_description = 'Replace the term \'test\' in the method name with the \'Test\' annotation'

    def __get_junit_version(self):
        pass

    def __process_identifier(self, identifier):
        if self.__entity.language == LanguageType.Java and self.__junit >= 4:
            try:
                if identifier.name_terms[0].lower() == 'test':
                    issue = Issue()
                    issue.file_path = self.__entity.path
                    issue.identifier = identifier.get_fully_qualified_name()
                    issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                    issue.category = self.__issue_category
                    issue.details = self.__issue_description
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
                handle_error('X.3', error_message, ErrorSeverity.Error, False, e)

    def analyze(self, project, entity):
        if entity.file_type == FileType.Test:
            self.__project = project
            self.__entity = entity
            for class_item in self.__entity.classes:
                for method_item in class_item.methods:
                    self.__process_identifier(method_item)

        return self.__issues