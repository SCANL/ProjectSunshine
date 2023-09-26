from datetime import datetime

from typing_extensions import override
from src.common.enum import IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.util_parsing import get_all_return_statements, is_boolean_type, is_test_method
from src.model.issue import Issue
from src.nlp import term_list
from src.rule.linguistic_antipattern.linguistic_antipattern import LinguisticAntipattern


class IsNoReturnBool(LinguisticAntipattern):

    ID = 'A.2'
    ISSUE_CATEGORY = '\'Is\' returns more than a Boolean'
    ISSUE_DESCRIPTION = 'The name of a method is a predicate suggesting a true/false value in return. However the return type is not Boolean but rather a more complex type.'

    def __init__(self):
        super.__init__()

    @override
    def __process_identifier(self, identifier):
        # AntiPattern: starting term is a boolean term, but the method does not have a boolean return statement (i.e., true/false not returned)
        try:
            if not is_test_method(self.__project, self.__entity, identifier):
                if identifier.name_terms[0].lower() in term_list.get_boolean_terms(self.__project):
                    if not is_boolean_type(self.__entity, identifier):
                        issue = Issue()
                        issue.file_path = self.__entity.path
                        issue.identifier = identifier.get_fully_qualified_name()
                        issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                        issue.category = self.__issue_category
                        issue.details = self.__issue_description
                        issue.additional_details = 'Starting term: %s; Return type: %s%s' % (identifier.name_terms[0], identifier.return_type, '(array)' if identifier.is_array else '')
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
            handle_error('A.2', error_message, ErrorSeverity.Error, False, e)
