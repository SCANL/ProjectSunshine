from datetime import datetime

from typing_extensions import override
from src.common.enum import FileType, IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.model.issue import Issue
from src.nlp import pos_tag
from src.nlp.pos_tag import POSType
from src.rule.linguistic_antipattern.linguistic_antipattern import LinguisticAntipattern

# Impacted File: Test
# Impacted identifier: Method


class TestNonVerbStarting(LinguisticAntipattern):

    ID = 'X.4'
    ISSUE_CATEGORY = 'Starting term must be a verb'
    ISSUE_DESCRIPTION = 'The starting term (excluding \'test\') must be a verb'

    def __init__(self):
        super.__init__()
        self.__junit = None

    def __get_junit_version(self):
        pass

    @override
    def __process_identifier(self, identifier):
        try:
            starting_term = identifier.name_terms[0] if identifier.name_terms[0].lower() != 'test' else ''

            if len(identifier.name_terms) > 1:
                if identifier.name_terms[0].lower() == 'test':
                    starting_term = identifier.name_terms[1]

            if starting_term != '':
                tag = pos_tag.generate_tag(self.__project, starting_term)
                if pos_tag.get_tag_text(tag) != POSType.Verb:
                    issue = Issue(self, identifier)
                    self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(type(identifier).__name__), self.__entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('X.4', error_message, ErrorSeverity.Error, False, e)

    @override
    def analyze(self, project, entity):
        if entity.file_type == FileType.Test:
            self.__junit = project.junit_version
            LinguisticAntipattern.analyze(self, project, entity)
            
        return self.__issues
