from datetime import datetime

from common.util import java_collection_data_types
from model.identifier_type import get_type
from model.issue import Issue
from nlp.term_property import is_singular


class ExpectingNotGettingSingle:

    def __init__(self):
        self.__entity = None
        self.__id = 'A.4'
        self.__issues = []
        self.__issue_category = 'Expecting but not getting single instance'
        self.__issue_description = 'The name of a method indicates that a single object is returned but the return type is a collection.'

    def __process_identifier(self, identifier):
        # Issue: if the last term is singular and the return type is a collection
        if identifier.return_type in java_collection_data_types or identifier.is_array == True:
            if is_singular(identifier.name_terms[-1]):
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
