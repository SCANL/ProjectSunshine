import itertools
from typing import List, cast

from src.common.enum import IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.util_parsing import is_test_method
from src.model.entity import Entity
from src.model.issue import Issue
from src.model.project import Project
from src.nlp.related_terms import are_antonyms, clean_text


class MethodSignatureCommentOpposite:

    ID = 'C.2'
    ISSUE_CATEGORY = 'Method signature and comment are opposite'
    ISSUE_DESCRIPTION = 'The documentation of a method is in contradiction with its declaration.'

    def __init__(self):
        self.__issues = []

    def __find_antonyms(self, comment_terms: List[str], name_terms: List[str], type_terms: List[str]):
        for combination in itertools.product(comment_terms, type_terms):
            if combination[0].isalpha() and combination[1].isalpha() and are_antonyms(combination[0], combination[1]):
                return f"Antonyms: '{combination[0]}' and '{combination[1]}'"

        for combination in itertools.product(comment_terms, name_terms):
            if not combination[0].isalpha() or not combination[1].isalpha():
                continue

            if combination[0].lower() == combination[1].lower() and not are_antonyms(combination[0], combination[1]):
                continue

            return f"Antonyms: '{combination[0]}' and '{combination[1]}'"

        return None

    # Override
    def __process_identifier(self, identifier):

        # AntiPattern: The method name or return type and comment contain antonyms
        try:
            if is_test_method(self.__project, self.entity, identifier):
                return

            comment = identifier.block_comment
            if comment is None:
                return

            return_type = identifier.return_type
            is_array = '(array)' if identifier.is_array else ''
            matched_terms = f'Return Type: {return_type}{is_array};'

            comment_cleansed_terms = clean_text(comment, True)
            name_terms = identifier.name_terms[1:] if identifier.name_terms[0] == 'get' else identifier.name_terms
            type_terms = identifier.type_terms

            antonyms = self.__find_antonyms(
                comment_cleansed_terms, name_terms, type_terms
            )
            if not antonyms:
                return

            issue = Issue(self, identifier)
            issue.additional_details = matched_terms+antonyms
            self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(
                    type(identifier).__name__), self.entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('C.2', error_message, ErrorSeverity.Error, False, e)

    def analyze(self, project, entity: Entity):
        # Analyze all methods in a class
        self.__project = project
        self.entity = entity
        for class_item in self.entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
