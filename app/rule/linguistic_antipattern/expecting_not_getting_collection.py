from datetime import datetime

from app.common.enum import IdentifierType
from app.common.error_handler import handle_error, ErrorSeverity
from app.common.types_list import get_collection_types
from app.common.util_parsing import is_test_method
from app.model.issue import Issue
from app.nlp.term_property import is_plural


# Impacted File: All
# Impacted identifier: Method


class ExpectingNotGettingCollection:

    def __init__(self):
        self.__entity = None
        self.__project = None
        self.__id = 'B.6'
        self.__issues = []
        self.__issue_category = 'Expecting but not getting a collection'
        self.__issue_description = 'The name of a method suggests that a collection should be returned but a single object or nothing is returned.'

    def __process_identifier(self, identifier):
        # AntiPattern: if the last term is plural and the return type is not a collection
        try:
            if not is_test_method(self.__project, self.__entity, identifier):
                if is_plural(self.__project, identifier.name_terms[-1]):
                    if identifier.return_type not in get_collection_types(self.__project, self.__entity.language) and identifier.is_array != True:
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
            handle_error('B.6', error_message, ErrorSeverity.Error, False, e)


    def analyze(self, project, entity):
        # Analyze all methods in a class
        self.__project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
