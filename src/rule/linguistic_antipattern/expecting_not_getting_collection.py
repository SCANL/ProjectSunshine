from datetime import datetime
from typing import List, cast

from typing_extensions import override
from src.common.enum import IdentifierType, LanguageType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.types_list import get_collection_types, get_numeric_types
from src.common.util_parsing import is_test_method
from src.model.entity import Entity
from src.model.issue import Issue
from src.model.project import Project
from src.nlp import term_list
from src.nlp.term_property import is_plural
from src.rule.linguistic_antipattern.linguistic_antipattern import LinguisticAntipattern


# Impacted File: All
# Impacted identifier: Method


class ExpectingNotGettingCollection(LinguisticAntipattern):

    ID = 'B.6'
    ISSUE_CATEGORY = 'Expecting but not getting a collection'
    ISSUE_DESCRIPTION = 'The name of a method suggests that a collection should be returned but a single object or nothing is returned.'

    def __init__(self):
        super.__init__()  # type: ignore

    # Override
    def __process_identifier(self, identifier):
        project = cast(Project, self.project)
        entity = cast(Entity, self.__entity)
        language = cast(LanguageType, cast(Entity, self.__entity).language)
        path = cast(str, cast(Entity, self.__entity).path)

        # AntiPattern: if the fist term is a get related term AND [(any term is plural or contains collection term)] and the return type is not a collection
        test_method = is_test_method(
            self.__project, entity, identifier)
        name_in_get_terms = identifier.name_terms[0].lower(
        ) in term_list.get_get_terms(project)
        coll_name_no_array = identifier.return_type not in get_collection_types(
            project, language) and not identifier.is_array

        try:
            if not test_method and name_in_get_terms:
                if any(is_plural(project, c) for c in identifier.name_terms[1:]) or any(item in map(str.lower, identifier.name_terms[1:]) for item in map(str.lower, cast(List[str], get_collection_types(project, language)))) and coll_name_no_array:
                    message = 'Return type: %s%s' % (
                        identifier.return_type, '(array)' if identifier.is_array else '')
                    if identifier.return_type in get_numeric_types(cast(LanguageType, cast(Entity, self.__entity).language)):
                        message = message + '; Return type is numeric, this might be a false-positive'
                    issue = Issue(self, identifier)
                    issue.additional_details = message
                    self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(
                    type(identifier).__name__), path, identifier.line_number,
                identifier.column_number)
            handle_error('B.6', error_message, ErrorSeverity.Error, False, e)
