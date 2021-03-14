from datetime import datetime

from common.util import java_collection_data_types
from common.util_parsing import get_all_class_fields
from model.identifier_type import get_type
from model.issue import Issue
from nlp.term_property import is_singular


class SaysOneContainsMany:

    def __init__(self):
        self.__entity = None
        self.__id = 'D.1'
        self.__issues = []
        self.__issue_category = 'Says one but contains many'
        self.__issue_description = 'The name of an attribute suggests a single instance, while its type suggests that the attribute stores a collection of objects.'

    def __process_identifier(self, identifier):
        # Issue: The last term in the name is singular AND the data type is a collection
        if is_singular(identifier.name_terms[-1]):
            if identifier.type in java_collection_data_types or identifier.is_array == True:
                issue = Issue()
                issue.file_path = self.__entity.path
                issue.identifier = identifier.get_fully_qualified_name()
                issue.identifier_type = get_type(type(identifier).__name__)
                issue.category = self.__issue_category
                issue.details = self.__issue_description
                issue.analysis_datetime = datetime.now()
                self.__issues.append(issue)

    def analyze(self, entity):
        # Analyze all attributes, variables and parameters in a class
        self.__entity = entity
        for class_item in self.__entity.classes:
            fields = get_all_class_fields(class_item)
            for field_item in fields:
                self.__process_identifier(field_item)

        return self.__issues
