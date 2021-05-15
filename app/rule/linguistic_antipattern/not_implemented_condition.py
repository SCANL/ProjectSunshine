from datetime import datetime

from app.common.enum import IdentifierType
from app.common.error_handler import ErrorSeverity, handle_error
from app.common.util_parsing import get_all_conditional_statements
from app.model.issue import Issue
from app.nlp import term_list


class NotImplementedCondition:

    def __init__(self):
        self.__entity = None
        self.__project = None
        self.__id = 'B.1'
        self.__issues = []
        self.__issue_category = 'Not implemented condition'
        self.__issue_description = 'The comments of a method suggest a conditional behavior that is not implemented in the code.'

    def __process_identifier(self, identifier):
        # AntiPattern: method contains conditional-related comment, but no conditional statements
        try:
            comments = identifier.get_all_comments(unique_terms=True)
            if len(comments) >= 1:
                contains = False
                if any(item in map(str.lower, comments) for item in map(str.lower, term_list.get_conditional_terms(self.__project))):
                    contains = True
                if contains:
                    conditional_statements, conditional_statements_total = get_all_conditional_statements(identifier.source)
                    if conditional_statements_total == 0:
                        issue = Issue()
                        issue.file_path = self.__entity.path
                        issue.identifier = identifier.get_fully_qualified_name()
                        issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                        issue.category = self.__issue_category
                        issue.details = self.__issue_description
                        issue.additional_details = 'Count of conditional statements: %s' % conditional_statements_total
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
            handle_error('B.1', error_message, ErrorSeverity.Critical, False, e)

    def analyze(self, project, entity):
        # Analyze all methods in a class
        self.__project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
