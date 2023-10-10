import itertools
from typing import cast

from src.common.enum import IdentifierType, LanguageType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.util_parsing import is_test_method
from src.model.entity import Entity
from src.model.issue import Issue
from src.model.project import Project
from src.nlp.related_terms import are_antonyms


class MethodNameReturnOpposite:

    ID = 'C.1'
    ISSUE_CATEGORY = 'Method name and return type are opposite'
    ISSUE_DESCRIPTION = 'The intent of the method suggested by its name is in contradiction with what it returns.'

    def __init__(self):
        self.__issues = []

    # Override
    def __process_identifier(self, identifier):

        # AntiPattern: The method name and return type name contain antonyms
        try:
            if not is_test_method(self.__project, self.entity, identifier):
                matched_terms = 'Return Type: %s%s;' % (
                    identifier.return_type, '(array)' if identifier.is_array else '')
                if identifier.name_terms[0] == 'get':
                    unique_combinations = list(itertools.product(
                        identifier.name_terms[1:], identifier.type_terms))
                else:
                    unique_combinations = list(itertools.product(
                        identifier.name_terms, identifier.type_terms))

                result_antonyms = False
                for combination in unique_combinations:
                    if combination[0].isalpha() and combination[1].isalpha() and combination[0].lower() != combination[1].lower() and are_antonyms(combination[0], combination[1]):
                        result_antonyms = True
                        matched_terms = matched_terms + \
                            'Antonyms: \'%s\' and \'%s\'' % (
                                combination[0], combination[1])
                        break

                if result_antonyms:
                    issue = Issue(self, identifier)
                    issue.additional_details = matched_terms
                    self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(
                    type(identifier).__name__), self.entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('C.1', error_message, ErrorSeverity.Error, False, e)

    def analyze(self, project, entity):
        # Analyze all methods in a class
        self.__project = project
        self.entity = entity
        for class_item in self.entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
