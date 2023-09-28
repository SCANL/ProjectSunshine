from datetime import datetime
from typing import List, cast

from src.common.enum import IdentifierType, LanguageType
from src.common.error_handler import ErrorSeverity, handle_error
from src.common.types_list import get_collection_types
from src.common.util_parsing import is_test_method
from src.model.entity import Entity
from src.model.issue import Issue
from src.model.project import Project
from src.nlp.term_property import is_singular


# Impacted File: All
# Impacted identifier: Method


class ExpectingNotGettingSingle:

    ID = 'A.4'
    ISSUE_CATEGORY = 'Expecting but not getting single instance'
    ISSUE_DESCRIPTION = 'The name of a method indicates that a single object is returned but the return type is a collection.'

    def __init__(self):
        self.__issues = []

    # Override
    def __process_identifier(self, identifier):
        # AntiPattern: if the last term is singular and the name does not contain a collection term and the return type is a collection

        try:
            if not is_test_method(self.__project, self.entity, identifier) and is_singular(self.__project, identifier.name_terms[-1]):
                if not any(item in map(str.lower, identifier.name_terms) for item in map(str.lower, cast(List[str], get_collection_types(self.__project, self.entity.language)))):
                    if identifier.return_type in get_collection_types(self.__project, self.entity.language) or identifier.is_array == True:
                        issue = Issue(self, identifier)
                        issue.additional_details = 'Return type: %s%s' % (
                            identifier.return_type, '(array)' if identifier.is_array else '')
                        self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(
                    type(identifier).__name__), self.entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('A.4', error_message, ErrorSeverity.Error, False, e)

    def analyze(self, project, entity):
        # Analyze all methods in a class
        self.__project = project
        self.entity = entity
        for class_item in self.entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
