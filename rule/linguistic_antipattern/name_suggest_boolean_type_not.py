from datetime import datetime

from common.util_parsing import get_all_class_fields
from model.identifier_type import get_type
from model.issue import Issue
from nlp import custom_terms


class NameSuggestBooleanTypeNot:

    def __init__(self):
        self.__entity = None
        self.__id = 'D.2'
        self.__issues = []
        self.__issue_category = 'Name suggests boolean but type is not'
        self.__issue_description = 'The name of an attribute suggests that its value is true or false, but its declaring type is not Boolean.'

    def __process_identifier(self, identifier):
        # Issue: The starting term in the name should be a boolean term AND the data type is not a boolean
        if identifier.name_terms[0].lower() in custom_terms.boolean_terms:
            if identifier.type != 'boolean' and identifier.type != 'Boolean':
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
