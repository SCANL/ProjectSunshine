from datetime import datetime

from app.common.enum import IdentifierType
from app.common.types_list import get_collection_types
from app.common.util_parsing import get_all_class_fields
from app.model.issue import Issue
from app.nlp.term_property import is_singular


class SaysOneContainsMany:

    def __init__(self):
        self.__entity = None
        self.__project = None
        self.__id = 'D.1'
        self.__issues = []
        self.__issue_category = 'Says one but contains many'
        self.__issue_description = 'The name of an attribute suggests a single instance, while its type suggests that the attribute stores a collection of objects.'

    def __process_identifier(self, identifier):
        # AntiPattern: The last term in the name is singular AND the data type is a collection
        if is_singular(self.__project, identifier.name_terms[-1]):
            if identifier.type in get_collection_types(self.__project, self.__entity.language) or identifier.is_array == True:
                issue = Issue()
                issue.file_path = self.__entity.path
                issue.identifier = identifier.get_fully_qualified_name()
                issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                issue.category = self.__issue_category
                issue.details = self.__issue_description
                issue.additional_details = 'Last term: \'%s\' Data type: \'%s\'' % (identifier.name_terms[-1], identifier.type)
                issue.id = self.__id
                issue.analysis_datetime = datetime.now()
                issue.file_type = self.__entity.file_type
                issue.line_number = identifier.line_number
                self.__issues.append(issue)

    def analyze(self, project, entity):
        # Analyze all attributes, variables and parameters in a class
        self.__project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            fields = get_all_class_fields(class_item)
            for field_item in fields:
                self.__process_identifier(field_item)

        return self.__issues
