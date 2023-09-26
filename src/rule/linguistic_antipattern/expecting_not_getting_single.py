from datetime import datetime

from typing_extensions import override
from src.common.enum import IdentifierType
from src.common.error_handler import ErrorSeverity, handle_error
from src.common.types_list import get_collection_types
from src.common.util_parsing import is_test_method
from src.model.issue import Issue
from src.nlp.term_property import is_singular
from src.rule.linguistic_antipattern.linguistic_antipattern import LinguisticAntipattern


# Impacted File: All
# Impacted identifier: Method


class ExpectingNotGettingSingle(LinguisticAntipattern):

    ID = 'A.4'
    ISSUE_CATEGORY = 'Expecting but not getting single instance'
    ISSUE_DESCRIPTION = 'The name of a method indicates that a single object is returned but the return type is a collection.'

    def __init__(self):
        super.__init__()

    @override
    def __process_identifier(self, identifier):
        # AntiPattern: if the last term is singular and the name does not contain a collection term and the return type is a collection
        try:
            if not is_test_method(self.__project, self.__entity, identifier):
                if is_singular(self.__project, identifier.name_terms[-1]):
                    if not any(item in map(str.lower, identifier.name_terms) for item in map(str.lower, get_collection_types(self.__project, self.__entity.language))):
                        if identifier.return_type in get_collection_types(self.__project, self.__entity.language) or identifier.is_array == True:
                            issue = Issue(self, identifier)
                            issue.additional_details = 'Return type: %s%s' % (identifier.return_type,'(array)' if identifier.is_array else '')
                            self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(type(identifier).__name__), self.__entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('A.4', error_message, ErrorSeverity.Error, False, e)
