from datetime import datetime

from common import util
from common.enum import IdentifierType
from common.util_parsing import get_all_class_fields
from model.issue import Issue
from nlp.term_property import is_singular, is_plural


class SaysManyContainsOne:

    def __init__(self):
        self.__entity = None
        self.__id = 'E.1'
        self.__issues = []
        self.__issue_category = 'Says many but contains one'
        self.__issue_description = 'The name of an attribute suggests multiple instances, but its type suggests a single one.'

    def __process_identifier(self, identifier):
        # AntiPattern: The last term in the name is plural AND the data type is not a collection
        if is_plural(identifier.name_terms[-1]):
            if identifier.type not in util.get_collection_types(self.__entity.language) and identifier.is_array != True:
                issue = Issue()
                issue.file_path = self.__entity.path
                issue.identifier = identifier.get_fully_qualified_name()
                issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                issue.category = self.__issue_category
                issue.details = self.__issue_description
                issue.additional_details = 'Last term: \'%s\' Data type: \'%s\'' % (identifier.name_terms[-1], identifier.type)
                issue.id = self.__id
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
