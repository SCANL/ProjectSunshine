from datetime import datetime

from typing_extensions import override
from src.common.enum import IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.util_parsing import is_test_method
from src.model.issue import Issue
from src.nlp import term_list
from src.rule.linguistic_antipattern.linguistic_antipattern import LinguisticAntipattern


class NotAnsweredQuestion(LinguisticAntipattern):

    ID = 'B.4'
    ISSUE_CATEGORY = 'Not answered question'
    ISSUE_DESCRIPTION = 'The name of a method is in the form of predicate whereas the return type is not Boolean.'

    def __init__(self):
        super.__init__()

    @override
    def __process_identifier(self, identifier):
        # AntiPattern: starting term is a boolean term, but the method return type is void
        try:
            if not is_test_method(self.__project, self.__entity, identifier):
                if identifier.name_terms[0].lower() in term_list.get_boolean_terms(self.__project) and identifier.return_type == 'void':
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
            handle_error('B.4', error_message, ErrorSeverity.Error, False, e)
