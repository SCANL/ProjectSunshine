from datetime import datetime

from app.common.enum import FileType, IdentifierType
from app.common.testing_list import get_null_check_test_method
from app.common.util_parsing import get_all_function_calls
from app.model.issue import Issue


# Impacted File: Test
# Impacted identifier: Method


class TestMissingNullCheck:

    def __init__(self):
        self.__entity = None
        self.__project = None
        self.__id = 'P.5'
        self.__junit = 4  # None
        self.__issues = []
        self.__issue_category = 'Test method missing null check'
        self.__issue_description = 'Body of the test method is missing a null check even though the name contains the term \'null\' or \'not\' '

    def __get_junit_version(self):
        pass

    def __process_identifier(self, identifier):
        # AntiPattern: Method name contains the term 'null' or 'not', but does not perform a null check
        if 'null' in map(str.lower, identifier.name_terms) or 'not' in map(str.lower, identifier.name_terms):
            method_calls = get_all_function_calls(identifier.source)
            api_null_method = get_null_check_test_method(self.__project, self.__entity.language)
            if not any(x in method_calls for x in api_null_method):
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

    def analyze(self, project, entity):
        if entity.file_type == FileType.Test:
            self.__project = project
            self.__entity = entity
            for class_item in self.__entity.classes:
                for method_item in class_item.methods:
                    self.__process_identifier(method_item)

        return self.__issues
