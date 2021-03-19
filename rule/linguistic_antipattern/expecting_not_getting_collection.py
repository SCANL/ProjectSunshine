from datetime import datetime

from common import util
from common.enum import IdentifierType
from model.issue import Issue
from nlp.term_property import is_plural


class ExpectingNotGettingCollection:

    def __init__(self):
        self.__entity = None
        self.__id = 'B.6'
        self.__issues = []
        self.__issue_category = 'Expecting but not getting a collection'
        self.__issue_description = 'The name of a method suggests that a collection should be returned but a single object or nothing is returned.'

    def __process_identifier(self, identifier):
        # AntiPattern: if the last term is plural and the return type is not a collection
        if is_plural(identifier.name_terms[-1]):
            if identifier.return_type not in util.get_collection_types(self.__entity.language) and identifier.is_array != True:
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
