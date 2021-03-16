import itertools
from datetime import datetime

from model.identifier_type import get_type
from model.issue import Issue
from nlp.related_terms import are_antonyms


class MethodNameReturnOpposite:

    def __init__(self):
        self.__entity = None
        self.__id = 'C.1'
        self.__issues = []
        self.__issue_category = 'Method name and return type are opposite'
        self.__issue_description = 'The intent of the method suggested by its name is in contradiction with what it returns.'

    def __process_identifier(self, identifier):
        # Issue: The method name and return type name contain antonyms
        unique_combinations = list(itertools.product(identifier.name_terms, identifier.type_terms))
        result_antonyms = False
        for combination in unique_combinations:
            if are_antonyms(combination[0], combination[1]):
                result_antonyms = True
                break

        if result_antonyms:
            issue = Issue()
            issue.file_path = self.__entity.path
            issue.identifier = identifier.get_fully_qualified_name()
            issue.identifier_type = get_type(type(identifier).__name__)
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
