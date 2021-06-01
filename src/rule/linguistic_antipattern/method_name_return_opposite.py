import itertools
from datetime import datetime

from src.common.enum import IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.util_parsing import is_test_method
from src.model.issue import Issue
from src.nlp.related_terms import are_antonyms


class MethodNameReturnOpposite:

    def __init__(self):
        self.__entity = None
        self.__project = None
        self.__id = 'C.1'
        self.__issues = []
        self.__issue_category = 'Method name and return type are opposite'
        self.__issue_description = 'The intent of the method suggested by its name is in contradiction with what it returns.'

    def __process_identifier(self, identifier):
        # AntiPattern: The method name and return type name contain antonyms
        try:
            if not is_test_method(self.__project, self.__entity, identifier):
                matched_terms = 'Return Type: %s%s;' % (identifier.return_type, '(array)' if identifier.is_array else '')
                if identifier.name_terms[0] == 'get':
                    unique_combinations = list(itertools.product(identifier.name_terms[1:], identifier.type_terms))
                else:
                    unique_combinations = list(itertools.product(identifier.name_terms, identifier.type_terms))

                result_antonyms = False
                for combination in unique_combinations:
                    if combination[0].isalpha() and combination[1].isalpha():
                        if combination[0].lower() != combination[1].lower():
                            if are_antonyms(combination[0], combination[1]):
                                result_antonyms = True
                                matched_terms = matched_terms + 'Antonyms: \'%s\' and \'%s\'' % (combination[0], combination[1])
                                break

                if result_antonyms:
                    issue = Issue()
                    issue.file_path = self.__entity.path
                    issue.identifier = identifier.get_fully_qualified_name()
                    issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                    issue.category = self.__issue_category
                    issue.details = self.__issue_description
                    issue.additional_details = matched_terms
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
            handle_error('C.1', error_message, ErrorSeverity.Error, False, e)

    def analyze(self, project, entity):
        # Analyze all methods in a class
        self.__project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
