from datetime import datetime

from typing_extensions import override
from src.common.enum import FileType, IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.model.issue import Issue
from src.rule.linguistic_antipattern.linguistic_antipattern import LinguisticAntipattern

# Impacted File: Test
# Impacted identifier: Method


class TestAnnotationTest(LinguisticAntipattern):

    ID = 'G.2'
    ISSUE_CATEGORY = 'Redundant use of \'test\' in method name'
    ISSUE_DESCRIPTION = 'Replace the term \'test\' in the method name with the \'Test\' annotation'

    def __init__(self):
        self.__init__()
        self.__junit = None

    def __get_junit_version(self):
        pass

    @override
    def __process_identifier(self, identifier):
        try:
            if self.__junit is not None:
                if self.__junit < 4:
                    return

            if identifier.name_terms[0].lower() == 'test':
                issue = Issue(self, identifier)
                self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(type(identifier).__name__), self.__entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('G.2', error_message, ErrorSeverity.Error, False, e)

    @override
    def analyze(self, project, entity):
        if entity.file_type == FileType.Test:
            self.__junit = project.junit_version
            LinguisticAntipattern.analyze(self, project, entity)
            
        return self.__issues
