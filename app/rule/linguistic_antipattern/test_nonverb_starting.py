from datetime import datetime

from app.common.enum import FileType, IdentifierType
from app.common.error_handler import handle_error, ErrorSeverity
from app.model.issue import Issue
from app.nlp import pos_tag
from app.nlp.pos_tag import POSType

# Impacted File: Test
# Impacted identifier: Method


class TestNonVerbStarting:

    def __init__(self):
        self.__entity = None
        self.__project = None
        self.__id = 'X.4'
        self.__junit = None
        self.__issues = []
        self.__issue_category = 'Starting term must be a verb'
        self.__issue_description = 'The starting term (excluding \'test\') must be a verb'

    def __process_identifier(self, identifier):
        try:
            if self.__junit is not None:
                if self.__junit < 4:
                    return

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

    def analyze(self, project, entity):
        if entity.file_type == FileType.Test:
            self.__project = project
            self.__junit = project.junit_version
            self.__entity = entity
            for class_item in self.__entity.classes:
                for method_item in class_item.methods:
                    self.__process_identifier(method_item)

        return self.__issues
