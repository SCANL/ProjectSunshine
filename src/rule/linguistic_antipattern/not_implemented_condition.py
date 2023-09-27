from typing import cast
from src.common.enum import IdentifierType, FileType
from src.common.error_handler import ErrorSeverity, handle_error
from src.common.util_parsing import get_all_conditional_statements, is_test_method
from src.model.entity import Entity
from src.model.issue import Issue
from src.model.project import Project
from src.nlp import term_list
from src.rule.linguistic_antipattern.linguistic_antipattern import LinguisticAntipattern


class NotImplementedCondition(LinguisticAntipattern):

    ID = 'B.1'
    ISSUE_CATEGORY = 'Not implemented condition'
    ISSUE_DESCRIPTION = 'The comments or name of a method suggest a conditional behavior that is not implemented in the code.'

    def __init__(self):
        super.__init__()  # type: ignore

    # Override
    def __process_identifier(self, identifier):
        project = cast(Project, self.project)
        entity = cast(Entity, self.__entity)

        # AntiPattern: method contains conditional-related comment or name, but no conditional statements
        try:
            if is_test_method(project, entity, identifier):
                return

            comments = identifier.get_all_comments(unique_terms=True)
            if len(comments) < 1:
                return

            contains_comments = False
            contains_name = False
            # comment contains conditional terms
            if any(item in map(str.lower, comments) for item in map(str.lower, term_list.get_conditional_terms(project))):
                contains_comments = True
            # method name contains conditional terms
            if entity.file_type == FileType.NonTest:
                if any(item in map(str.lower, identifier.name_terms) for item in map(str.lower, term_list.get_conditional_terms(project))):
                    contains_name = True

            if contains_comments or contains_name:
                _, conditional_statements_total = get_all_conditional_statements(
                    identifier.source)
                if conditional_statements_total == 0:
                    issue = Issue(self, identifier)
                    issue.additional_details = 'Comment contains terms: %s; Name contains terms: %s' % (
                        str(contains_comments), str(contains_name))
                    self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(
                    type(identifier).__name__
                ),
                entity.path,
                identifier.line_number,
                identifier.column_number
            )
            handle_error('B.1', error_message, ErrorSeverity.Error, False, e)
