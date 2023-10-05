from typing import cast
from src.common.enum import FileType, IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.model.entity import Entity
from src.model.issue import Issue
from src.model.project import Project
from src.nlp import pos_tag
from src.nlp.pos_tag import POSType
from src.common.util_parsing import get_all_class_fields

# Impacted File: Test
# Impacted identifier: Method


class TestNonVerbStarting():

    ID = 'X.4'
    ISSUE_CATEGORY = 'Starting term must be a verb'
    ISSUE_DESCRIPTION = 'The starting term (excluding \'test\') must be a verb'

    def __init__(self):
        self.__issues = []

    # Override
    def __process_identifier(self, identifier):
        self.__project = cast(Project, self.__project)
        self.__entity = cast(Entity, self.entity)

        try:
            starting_term = identifier.name_terms[0] if identifier.name_terms[0].lower(
            ) != 'test' else ''

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
                IdentifierType.get_type(
                    type(identifier).__name__), self.__entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('X.4', error_message, ErrorSeverity.Error, False, e)

    # Override
    def analyze(self, project, entity):
        if entity.file_type == FileType.Test:
            # Analyze all attributes, variables and parameters in a class
            self.project = project
            self.entity = entity
            for class_item in self.entity.classes:
                fields = get_all_class_fields(class_item)
                for field_item in fields:
                    self.__process_identifier(field_item)

            return self.__issues

        return self.__issues
