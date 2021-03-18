import itertools
from datetime import datetime

from model.identifier_type import get_type
from model.issue import Issue
from nlp.related_terms import are_antonyms, clean_text


class MethodSignatureCommentOpposite:

    def __init__(self):
        self.__entity = None
        self.__id = 'C.2'
        self.__issues = []
        self.__issue_category = 'Method signature and comment are opposite'
        self.__issue_description = 'The documentation of a method is in contradiction with its declaration.'

    def __process_identifier(self, identifier):
        # Issue: The method name or retrun type and comment contain antonyms
        comment = identifier.block_comment
        if comment is not None:
            comment_cleansed_terms = clean_text(comment, True)
            unique_combinations_type = list(itertools.product(comment_cleansed_terms, identifier.type_terms))
            unique_combinations_name = list(itertools.product(comment_cleansed_terms, identifier.name_terms))

            result_antonyms = False
            for combination in unique_combinations_type:
                if are_antonyms(combination[0], combination[1]):
                    result_antonyms = True
                    break

            for combination in unique_combinations_name:
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
