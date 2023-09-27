from src.common.enum import FileType, IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.testing_list import get_null_check_test_method
from src.common.util_parsing import get_all_function_calls
from src.model.issue import Issue
from src.rule.linguistic_antipattern.linguistic_antipattern import LinguisticAntipattern


# Impacted File: Test
# Impacted identifier: Method


class TestMissingNullCheck(LinguisticAntipattern):

    ID = 'P.5'
    ISSUE_CATEGORY = 'Test method missing null check'
    ISSUE_DESCRIPTION = 'Body of the test method is missing a null check even though the name contains the term \'null\' or \'not\' '

    def __init__(self):
        super.__init__()

    # Override
    def __process_identifier(self, identifier):
        # AntiPattern: Method name contains the term 'null' or 'not', but does not perform a null check
        try:
            if 'null' in map(str.lower, identifier.name_terms) or 'not' in map(str.lower, identifier.name_terms):
                method_calls = get_all_function_calls(identifier.source)
                api_null_method = get_null_check_test_method(
                    self.__project, self.__entity.language)
                if not any(x in method_calls for x in api_null_method):
                    issue = Issue(self, identifier)
                    self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(
                    type(identifier).__name__), self.__entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('P.5', error_message, ErrorSeverity.Error, False, e)

    # Override
    def analyze(self, project, entity):
        if entity.file_type == FileType.Test:
            LinguisticAntipattern.analyze(self, project, entity)

        return self.__issues
