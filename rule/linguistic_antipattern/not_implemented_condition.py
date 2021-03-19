from datetime import datetime

from common.enum import IdentifierType
from common.util_parsing import get_all_conditional_statements
from model.issue import Issue
from nlp.custom_terms import conditional_terms


class NotImplementedCondition:

    def __init__(self):
        self.__entity = None
        self.__id = 'B.1'
        self.__issues = []
        self.__issue_category = 'Not implemented condition'
        self.__issue_description = 'The comments of a method suggest a conditional behavior that is not implemented in the code.'

    def __process_identifier(self, identifier):
        # AntiPattern: method contains conditional-related comment, but no conditional statements
        comments = identifier.get_all_comments()
        if len(comments) >= 1:
            contains = False
            for comment in comments:
                if any(item in comment for item in conditional_terms):
                    contains = True
                    break
            if contains:
                conditional_statements, conditional_statements_total = get_all_conditional_statements(identifier.source)
                if conditional_statements_total == 0:
                    issue = Issue()
                    issue.file_path = self.__entity.path
                    issue.identifier = identifier.get_fully_qualified_name()
                    issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                    issue.category = self.__issue_category
                    issue.details = self.__issue_description
                    issue.analysis_datetime = datetime.now()
                    self.__issues.append(issue)

    def analyze(self, entity):
        # Analyze all methods in a class
        self.__entity = entity
        for class_item in self.__entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
