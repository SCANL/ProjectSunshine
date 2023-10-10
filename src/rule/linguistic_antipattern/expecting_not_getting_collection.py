from datetime import datetime
from typing import List, cast

from src.common.enum import IdentifierType, LanguageType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.types_list import get_collection_types, get_numeric_types
from src.common.util_parsing import is_test_method
from src.model.entity import Entity
from src.model.issue import Issue
from src.model.project import Project
from src.nlp import term_list
from src.nlp.term_property import is_plural


# Impacted File: All
# Impacted identifier: Method


class ExpectingNotGettingCollection:

    ID = 'B.6'
    ISSUE_CATEGORY = 'Expecting but not getting a collection'
    ISSUE_DESCRIPTION = 'The name of a method suggests that a collection should be returned but a single object or nothing is returned.'

    def __init__(self):
        self.__issues = []

    # Override
    def __process_identifier(self, identifier):

        # AntiPattern: if the fist term is a get related term AND [(any term is plural or contains collection term)] and the return type is not a collection
        test_method = is_test_method(
            self.__project, self.entity, identifier)
        name_in_get_terms = identifier.name_terms[0].lower(
        ) in term_list.get_get_terms(self.__project)
        coll_name_no_array = identifier.return_type not in get_collection_types(
            self.__project, self.entity.language) and not identifier.is_array

        try:
            if not test_method and name_in_get_terms:
                if any(is_plural(self.__project, c) for c in identifier.name_terms[1:]) or any(item in map(str.lower, identifier.name_terms[1:]) for item in map(str.lower, cast(List[str], get_collection_types(self.__project, self.entity.language)))) and coll_name_no_array:
                    message = 'Return type: %s%s' % (
                        identifier.return_type, '(array)' if identifier.is_array else '')
                    if identifier.return_type in get_numeric_types(cast(LanguageType, cast(Entity, self.entity).language)):
                        message = message + '; Return type is numeric, this might be a false-positive'
                    issue = Issue(self, identifier)
                    issue.additional_details = message
                    self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(
                    type(identifier).__name__), self.entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('B.6', error_message, ErrorSeverity.Error, False, e)

    def analyze(self, project, entity):
        # Analyze all methods in a class
        self.__project = project
        self.entity = entity
        for class_item in self.entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
