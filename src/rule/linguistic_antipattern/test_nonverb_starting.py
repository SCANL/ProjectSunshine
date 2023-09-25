from datetime import datetime

from typing_extensions import override
from src.common.enum import FileType, IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.model.issue import Issue
from src.nlp import pos_tag
from src.nlp.pos_tag import POSType
from linguistic_antipattern import LinguisticAntipattern

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
            handle_error('X.4', error_message, ErrorSeverity.Error, False, e)

    @override
    def analyze(self, project, entity):
        if entity.file_type == FileType.Test:
            self.__project = project
            self.__junit = project.junit_version
            self.__entity = entity
            for class_item in self.__entity.classes:
                for method_item in class_item.methods:
                    self.__process_identifier(method_item)

        return self.__issues
