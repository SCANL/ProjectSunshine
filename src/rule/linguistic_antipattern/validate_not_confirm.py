from src.common.enum import IdentifierType
from src.common.error_handler import ErrorSeverity, handle_error
from src.common.util_parsing import get_all_exception_throws, is_test_method, is_boolean_type
from src.model.issue import Issue
# Impacted identifier: All
# Impacted identifier: Method
from src.nlp import term_list
from src.rule.linguistic_antipattern.linguistic_antipattern import LinguisticAntipattern


class ValidateNotConfirm(LinguisticAntipattern):

    ID = 'B.2'
    ISSUE_CATEGORY = 'Validation method does not confirm'
    ISSUE_DESCRIPTION = 'A validation method does not provide a return value informing whether the validation was successful.'

    def __init__(self):
        super.__init__()

    #Override
    def __process_identifier(self, identifier):
        # AntiPattern: The name starts with validate and return type is not void and no exception thrown. Not applicable to test methods
        try:
            if not is_test_method(self.__project, self.__entity, identifier):
                if identifier.name_terms[0].lower() in term_list.get_validate_terms(self.__project):
                    if (identifier.return_type == 'void') and (len(get_all_exception_throws(identifier.source)) == 0):
                        issue = Issue(self, identifier)
                        self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(type(identifier).__name__), self.__entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('B.2', error_message, ErrorSeverity.Error, False, e)
