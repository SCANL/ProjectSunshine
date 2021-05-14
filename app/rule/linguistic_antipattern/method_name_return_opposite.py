import itertools
from datetime import datetime

from app.common.enum import IdentifierType
from app.model.issue import Issue
from app.nlp.related_terms import are_antonyms


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
            issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
            issue.category = self.__issue_category
            issue.details = self.__issue_description
            issue.id = self.__id
            issue.analysis_datetime = datetime.now()
            issue.file_type = self.__entity.file_type
            self.__issues.append(issue)

    def analyze(self, project, entity):
        # Analyze all methods in a class
        self.__project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
